from django.shortcuts import render
from django.utils.timezone import now
from django.views import View

from forum_app.models import Category, Post


class MainView(View):
    def get(self, request):
        main_categories = Category.objects.filter(post__isnull=False, post__is_active=True).distinct()[:5]
        active_posts = Post.objects.filter(is_active=True)
        latest_posts = active_posts.order_by('-created_at')[:5]
        popular_posts = active_posts.order_by('-views_cnt')[:5]
        context = {
            'categories': main_categories,
            'latest_posts': latest_posts,
            'popular_posts': popular_posts,
        }
        return render(request, 'forum_app/index.html', context=context)
