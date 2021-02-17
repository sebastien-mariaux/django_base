from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

UserModel = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.set_password(self.cleaned_data["password1"])
        user.save()
        self.send_email(user)
        return user

    def send_email(self, user):
        user.generate_validation_token()
        user.send_email_activation_email()


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
