from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import UpdateView

from forum_app.forms import AddPostForm
from forum_app.models import Post
from .utils import filter_category


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

        return filter_category(form, self.request.user)

    def test_func(self):
        user = self.request.user
        post = self.get_object()

        return user == post.user or user.is_superuser


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_superuser or post.user == request.user:
        post.delete()

    return redirect('forum')
