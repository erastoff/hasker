from django.urls import path

from users.views import (
    RegistrationView,
    UserLoginView,
    UserLogoutView,
    UserTemplateView,
)

app_name = "users"

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("user_profile/<int:pk>/", UserTemplateView.as_view(), name="user-profile"),
]
