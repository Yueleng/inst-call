from .base import *  # noqa: F403

DEBUG = True

# overrides the two secure-cookie flags to False so HTTP localhost works.
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
