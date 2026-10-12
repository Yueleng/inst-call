from allauth.socialaccount.providers.google.views import oauth2_callback, oauth2_login
from django.urls import path

from .views import logout_view, me

urlpatterns = [
    path("me", me, name="auth-me"),
    path("logout", logout_view, name="auth-logout"),
    path("google/login", oauth2_login, name="google-login"),
    path("google/callback", oauth2_callback, name="google-callback"),
]
