from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.views.generic import ListView
from forum_app.models import Post, CustomUser


class ProfilePostListView(ListView):
    paginate_by = 10
    model = Post
    template_name = 'forum_app/profile_posts.html'
    context_object_name = 'posts'
    slug_url_kwarg = 'username'

    def get_posts_for_user(self, is_active: bool):
        search = self.request.GET.get('q', '')
        order_by = "-created_at"
        if self.request.GET.get('date', 'down') == 'up':
            order_by = order_by.replace("-", "")

        queryset = Post.objects.filter(
            user__username=self.kwargs.get('username'),
            is_active=is_active,
            title__icontains=search).order_by(order_by)
        return queryset

    def get_queryset(self):
        return self.get_posts_for_user(is_active=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        user_obj = CustomUser.objects.filter(username=self.kwargs.get('username'))
        if not user_obj:
            raise Http404
        context['user_obj'] = user_obj.first()
        context['users_post_title'] = f"Посты пользователя {context['user_obj']}"
        return context


class ProfileDraftsListView(UserPassesTestMixin, ProfilePostListView):
    def get_queryset(self):
        return self.get_posts_for_user(is_active=False)

    def test_func(self):
        user = CustomUser.objects.filter(username=self.kwargs.get('username'))
        if not user:
            raise Http404
        user = user.first()
        return self.request.user.is_superuser or user == self.request.user

