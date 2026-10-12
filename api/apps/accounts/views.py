from django.contrib.auth import logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import CurrentUserSerializer


# returns whether the current browser session is authenticated, 
# a CSRF token, 
# and user JSON if logged in.
@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def me(request):
    """Return the current session's user, or a clear anonymous response."""
    csrf_token = get_token(request)
    if not request.user.is_authenticated:
        return Response({"authenticated": False, "csrf_token": csrf_token})
    return Response({"authenticated": True, "user": CurrentUserSerializer(request.user).data, "csrf_token": csrf_token})

# clears the current Django session and returns 204 No Content.
@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)
