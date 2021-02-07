from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import reverse

from .forms import LoginForm, RegisterForm

UserModel = get_user_model()


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')


class LogoutView(auth_views.LogoutView):
    pass


class ProfileView(generic.DetailView):
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class UpdateProfileView(generic.UpdateView):
    model = UserModel
    fields = ['username', 'first_name', 'last_name']
    context_object_name = 'user'
    template_name = 'users/edit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile')