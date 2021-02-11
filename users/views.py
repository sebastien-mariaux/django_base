from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import reverse, render
from .auth_token import user_from_token

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
    def get(self, request, validation_token):   # pylint: disable=R0201
        if user := user_from_token(validation_token):
            user.validate()
            return render(request, 'users/email_confirmed.html', {'user': user})
        return render(request, 'users/confirmation_failure.html')


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
