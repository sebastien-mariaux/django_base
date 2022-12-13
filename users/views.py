from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import reverse, render, redirect
from .auth_token import user_from_token
from .forms import LoginForm, RegisterForm, UpdateEmailForm
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


class UpdateEmailView(LoginRequiredMixin, generic.UpdateView):
    form_class = UpdateEmailForm
    template_name = 'users/edit_email.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile')

    def form_valid(self, form):
        form.save()
        self.success_messages()
        return redirect(reverse('profile'))

    def success_messages(self) -> None:
        messages.add_message(
            self.request,
            messages.INFO,
            _('Please check your mailbox to confirm your new email'))


class NewEmailValidationView(generic.View):
    def get(self, request, validation_token):  # pylint: disable=R0201
        if user := user_from_token(validation_token):
            try:
                user.replace_email()
                self.success_messages()
            except ValidationError as err:
                self.error_messages(err)
            return redirect(reverse('profile'))

        return render(request, 'users/confirmation_failure.html')

    def success_messages(self) -> None:
        messages.add_message(
            self.request,
            messages.INFO,
            _('Your email has been successfully updated'))

    def error_messages(self, error):
        messages.add_message(
            self.request,
            messages.ERROR,
            ', '.join(error.messages)
        )


class ChangePasswordView(LoginRequiredMixin, auth_views.PasswordChangeView):
    success_url = reverse_lazy('profile')
    template_name = 'users/change_password.html'

    def form_valid(self, form):
        self.success_messages()
        return super(ChangePasswordView, self).form_valid(form)

    def success_messages(self) -> None:
        messages.add_message(
            self.request,
            messages.INFO,
            _('Your password has been modified'))


class ResetPasswordView(auth_views.PasswordResetView):
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        self.success_messages()
        return super(ResetPasswordView, self).form_valid(form)

    def success_messages(self) -> None:
        messages.add_message(
            self.request,
            messages.INFO,
            _('Please check your emails. We will send you a link to reset your password'))


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy('login')
    template_name = 'users/password_reset_confirm.html'

    def form_valid(self, form):
        self.success_messages()
        return super(PasswordResetConfirmView, self).form_valid(form)

    def success_messages(self) -> None:
        messages.add_message(
            self.request,
            messages.INFO,
            _('Your password has been updated'))
