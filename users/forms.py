from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from .mailer import UpdateEmailMailer

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

    @staticmethod
    def send_email(user):
        user.generate_validation_token()
        user.send_email_activation_email()


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')


class UpdateEmailForm(forms.ModelForm):
    def clean_next_email(self):
        next_email = self.cleaned_data['next_email']
        if UserModel.objects.filter(email=next_email).count() > 0:
            raise ValidationError("This email is already used")
        return next_email

    def save(self, commit=True):
        user = super(UpdateEmailForm, self).save()
        UpdateEmailMailer(user).send()

    class Meta:
        model = UserModel
        fields = ('next_email',)
