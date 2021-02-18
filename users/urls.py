from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    LoginView, RegisterView, ProfileView, UpdateProfileView, EmailValidationView,
    UpdateEmailView, NewEmailValidationView, ChangePasswordView, ResetPasswordView,
    PasswordResetConfirmView
)


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', ProfileView.as_view(), name='profile'),
    path('edit/', UpdateProfileView.as_view(), name='edit_profile'),
    path('activation/<str:validation_token>/', EmailValidationView.as_view(),
         name='validate_email'),
    path('email/edit/', UpdateEmailView.as_view(), name='update_email'),
    path('validate_email/<str:validation_token>/', NewEmailValidationView.as_view(),
         name='validate_new_email'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
]
