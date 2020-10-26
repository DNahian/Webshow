from django.urls import path
from .views import HomeView, WebsiteDetailView, save_to_profile, \
    remove_from_profile, about
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('website/<slug>/', WebsiteDetailView.as_view(), name='website'),
    path('save-to-profile/<slug>/', save_to_profile, name='save_to_profile'),
    path('remove-from-profile/<slug>/', remove_from_profile, name='remove_from_profile'),
    path('about/', about, name='about'),
]
