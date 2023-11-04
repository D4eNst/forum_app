from django.db.models import Count
from django.views.generic import DetailView

import forum_app.models
from forum_app.models import Post, Comment, CustomUser, UserActivity


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'forum_app/profile.html'
    context_object_name = 'user_obj'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_likes_cnt'] = Post.objects.filter(likes__id=self.object.id).aggregate(total_likes=Count('likes'))['total_likes']
        context['com_likes_cnt'] = Comment.objects.filter(likes__id=self.object.id).aggregate(total_likes=Count('likes'))['total_likes']
        context['activity'] = UserActivity.objects.filter(user__id=self.object.id).order_by('-created_at')[:5]
        context['post_cnt'] = Post.objects.filter(user=self.object, is_active=True).count()
        return context
