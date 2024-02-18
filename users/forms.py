from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import Widget

from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "image")

    username = forms.CharField(help_text="Enter your desired username")
    password1 = forms.CharField(
        help_text="Enter your passsword", widget=forms.PasswordInput(), label="Password"
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "custom-file-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.items():
            widget: Widget = field[1].widget
            widget.attrs["class"] = "form-control"


class UserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

    username = forms.CharField(help_text="")
    # password1 = forms.CharField(help_text='', widget=forms.PasswordInput(), label='Password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.items():
            widget: Widget = field[1].widget
            widget.attrs["class"] = "form-control"


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["readonly"] = True
        for field in self.fields.items():
            widget: Widget = field[1].widget
            widget.attrs["class"] = "form-control"
