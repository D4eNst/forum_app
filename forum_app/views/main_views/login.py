from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from forum_app.forms import LoginForm


class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'forum_app/login.html'
    redirect_authenticated_user = True

    # def get_success_url(self):
    #     current_path = self.request.GET.get('next')
    #     if current_path:
    #         return reverse_lazy('main-page')


def logout_user(request):
    logout(request)
    return redirect('login')
