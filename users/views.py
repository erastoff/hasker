from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import RegistrationForm, UserAuthenticationForm, UserProfileForm

User = get_user_model()


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy("users:login")
    success_message = "Поздравляем! Вы успешно зарегистрированы!"
    template_name = "users/user_form.html"


class UserLoginView(LoginView):
    template_name = "users/login_form.html"
    form_class = UserAuthenticationForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    pass


class UserTemplateView(UpdateView):
    model = User
    template_name = "users/user_detail.html"
    form_class = UserProfileForm

    def get_success_url(self):
        # Получаем текущий pk пользователя
        user_pk = self.request.user.pk
        # Формируем URL для перенаправления с передачей pk в качестве аргумента
        return reverse_lazy("users:user-profile", kwargs={"pk": user_pk})
