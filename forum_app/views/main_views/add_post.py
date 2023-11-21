from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView

from forum_app.models import Post, UserActivity, ActivityName, Category
from forum_app.forms import AddPostForm


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = AddPostForm
    template_name = 'forum_app/add_post.html'

    def get_form(self, form_class=None):
        form = super(CreatePost, self).get_form(form_class)
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

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        if form.instance.is_active:
            UserActivity.objects.create(
                user=self.request.user,
                action_type="Пользователь написал новый пост",
                action_name=ActivityName.objects.get(name="new_post"),
                post=form.instance
            )

        return HttpResponseRedirect(self.get_success_url())
