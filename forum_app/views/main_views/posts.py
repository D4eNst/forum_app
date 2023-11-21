from django.http import Http404
from django.views.generic import ListView
from forum_app.models import Post, Category


class PostListView(ListView):
    paginate_by = 20
    model = Post
    template_name = 'forum_app/posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        cat = Category.objects.get(slug=self.kwargs.get('slug'))
        queryset = Post.objects.filter(category=cat, is_active=True).order_by('title')
        if queryset.count() == 0:
            raise Http404
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs.get('slug'))
        print(context['category'])
        return context
