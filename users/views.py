import jwt
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import reverse, redirect, render

from .forms import LoginForm, RegisterForm

UserModel = get_user_model()


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


class EmailValidationView(generic.View):
    def get(self, request, validation_token, *args, **kwargs):
        user = self.user(validation_token)
        if user:
            self.validate_user(user)
            return render(request, 'users/email_confirmed.html', {'user': user})
        return render(request, 'users/validation_failure.html')

    @staticmethod
    def user(validation_token):
        body = jwt.decode(validation_token, settings.SECRET_KEY, algorithms="HS256")
        try:
            return UserModel.objects.get(
                id=body['user_id'], email=body['user_email'],
                validation_token=validation_token
            )
        except UserModel.DoesNotExist:
            return None

    @staticmethod
    def validate_user(user):
        user.is_active = True
        user.validation_token = None
        user.save()


class LogoutView(auth_views.LogoutView):
    pass


class ProfileView(LoginRequiredMixin, generic.DetailView):
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class UpdateProfileView(LoginRequiredMixin, generic.UpdateView):
    model = UserModel
    fields = ['username', 'first_name', 'last_name']
    context_object_name = 'user'
    template_name = 'users/edit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile')
