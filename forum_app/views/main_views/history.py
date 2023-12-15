from django.views.generic import ListView

from forum_app.models import CustomUser, UserActivity


class ProfileHistoryView(ListView):
    paginate_by = 10
    model = CustomUser
    template_name = 'forum_app/history.html'
    context_object_name = 'activity'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(username=self.kwargs['username'])
        context['user_obj'] = user

        return context

    def get_queryset(self):
        activity_filter = {}
        ordered = '-created_at'
        get_params = self.request.GET.dict()
        if get_params.get('action'):
            activity_filter['action_name__name__in'] = get_params.get('action').split()
        if get_params.get('date') == 'up':
            ordered = ordered.replace('-', '')
        user = CustomUser.objects.get(username=self.kwargs['username'])

        return UserActivity.objects.filter(user__id=user.id, **activity_filter).order_by(ordered)
