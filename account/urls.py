from django.urls import path, reverse_lazy
from .views import register, profile, edit_profile, change_password
from django.contrib.auth.views import (
    LoginView, LogoutView)
app_name = 'account'

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/change-password/', change_password, name='change_password'),
    path('login/', LoginView.as_view(
        template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(
        template_name='account/logout.html'), name='logout'),
]
