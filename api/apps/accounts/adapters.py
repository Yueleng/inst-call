from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpRequest

from .models import User

if TYPE_CHECKING:
    from allauth.socialaccount.models import SocialLogin


class AccountAdapter(DefaultSocialAccountAdapter):
    """Copy only the profile data required by the application from Google."""

    def populate_user(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
        data: dict[str, Any],
    ) -> User:
        # django-allauth supports arbitrary custom user models, so its return
        # type cannot describe the application-specific fields used below.
        user = cast(User, super().populate_user(request, sociallogin, data))
        user.email = data.get("email", "").lower()
        user.display_name = data.get("name", "")
        user.avatar_url = data.get("picture", "")
        return user
