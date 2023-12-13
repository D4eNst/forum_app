from django.views.generic import ListView
from forum_app.models import Category


class ForumListView(ListView):
    paginate_by = 8
    model = Category
    template_name = 'forum_app/forum.html'
    context_object_name = 'categories'

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        queryset = Category.objects.filter(post__isnull=False, post__is_active=True, name__icontains=search).distinct()
        return queryset


