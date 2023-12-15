from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView

from forum_app.forms import AddPostForm
from forum_app.models import Post
from .utils import create_activity, filter_category_form


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = AddPostForm
    template_name = 'forum_app/add_post.html'

    def get_form(self, form_class=None):
        form = super(CreatePost, self).get_form(form_class)

        return filter_category_form(form, self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        if form.instance.is_active:
            create_activity(user=self.request.user,
                            post=form.instance,
                            action_type="Пользователь написал новый пост",
                            action_name="new_post")

        return HttpResponseRedirect(self.get_success_url())
