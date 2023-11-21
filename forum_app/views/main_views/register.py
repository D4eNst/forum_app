from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView
# from forum_app.models import CustomUser
from forum_app.forms import RegisterForm


class RegisterView(CreateView):
    # def get(self, request):
    #     form = RegisterForm()
    #     return render(request, 'forum_app/register.html', context={"form": form})
    #
    # def post(self, request):
    #     form = RegisterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('main-page')
    #
    #     return render(request, 'forum_app/register.html', context={"form": form})

    form_class = RegisterForm
    template_name = 'forum_app/register.html'

    def get_success_url(self):
        next_page = self.request.GET.get('next')
        if next_page:
            return reverse_lazy('login') + '?next=' + next_page
        return reverse_lazy('login')
