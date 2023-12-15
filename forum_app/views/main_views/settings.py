from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse
from django.views.generic import UpdateView

from forum_app.forms import SettingsForm
from forum_app.models import CustomUser


class ProfileSettingsView(UpdateView, AccessMixin):
    model = CustomUser
    form_class = SettingsForm
    template_name = 'forum_app/settings.html'
    context_object_name = 'user_obj'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit'] = True
        return context

    def get_success_url(self):
        return reverse('settings', args=[self.object.username])

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        profile_user = self.get_object()
        test = user == profile_user or user.is_superuser
        if not test:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
