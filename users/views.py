from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import reverse, render, redirect
from .auth_token import user_from_token
from .mailer import UpdateEmailMailer
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


class UpdateEmailView(UpdateProfileView):
    fields = ['next_email']
    template_name = 'users/edit_email.html'
    mailer_class = UpdateEmailMailer

    def form_valid(self, form):
        user = form.save()
        self.send_mail(user)
        self.success_messages()
        return redirect(reverse('profile'))

    def success_messages(self) -> None:
        messages.add_message(
            self.request,
            messages.INFO,
            _('Please check your mailbox to confirm your new email'))

    def send_mail(self, user):
        # todo: move this to a form?
        mailer = self.mailer_class(user)
        mailer.send()


class NewEmailValidationView(generic.View):
    def get(self, request, validation_token):  # pylint: disable=R0201
        if user := user_from_token(validation_token):
            user.replace_email()
            self.success_messages()
            return redirect(reverse('profile'))
        return render(request, 'users/confirmation_failure.html')

    def success_messages(self) -> None:
        messages.add_message(
            self.request,
            messages.INFO,
            _('Your email has been successfully updated'))
