from django.urls import path
from .views import (LoginView, RegisterView, LogoutView, ProfileView,
                    UpdateProfileView, EmailValidationView)


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', ProfileView.as_view(), name='profile'),
    path('edit/', UpdateProfileView.as_view(), name='edit_profile'),
    path('activation/<str:validation_token>/', EmailValidationView.as_view(), name='validate-email')
]
