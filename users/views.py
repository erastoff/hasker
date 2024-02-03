# from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from users.forms import RegistrationForm, UserAuthenticationForm


class RegistrationView(CreateView):
    model = User
    # fields = ('username', 'email', 'password')
    form_class = RegistrationForm
    success_url = reverse_lazy("users:login")
    success_message = "Поздравляем! Вы успешно зарегистрированы!"
    template_name = "users/user_form.html"


class UserLoginView(LoginView):
    template_name = "users/login_form.html"
    form_class = UserAuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("index")


class UserLogoutView(LogoutView):
    pass
    # template_name = "users/login_form.html"
    # success_url = reverse_lazy("index")


class UserTemplateView(TemplateView):
    template_name = "users/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.request.user
        return context
