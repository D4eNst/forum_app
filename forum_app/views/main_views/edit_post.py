from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import UpdateView

from forum_app.models import Post, Category
from forum_app.forms import AddPostForm


class EditPost(UpdateView, UserPassesTestMixin):
    model = Post
    form_class = AddPostForm
    template_name = 'forum_app/add_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit'] = True
        return context

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.slug])

    def get_form(self, form_class=None):
        form = super(EditPost, self).get_form(form_class)
        is_admin = self.request.user.is_staff

        if not is_admin:
            not_empty_cat = Category.objects.filter(post__isnull=False, post__is_active=True)
            users_empty_cat = Category.objects.filter(post__isnull=True, user=self.request.user)
            users_draft_cat = Category.objects.filter(post__is_active=False, user=self.request.user)

            category_queryset = (not_empty_cat | users_empty_cat | users_draft_cat).distinct()
            form.fields['category'].queryset = category_queryset
        else:
            form.fields['category'].queryset = Category.objects.all()

        return form

    def test_func(self):
        user = self.request.user
        post = self.get_object()

        return user == post.user or user.is_superuser


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_superuser or post.user == request.user:
        post.delete()

    return redirect('forum')
