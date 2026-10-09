import os
from pathlib import Path

# base.py is the shared Django configuratin
# local.py imports it and changes a few development-specific values

# parents = [
#  '[absolute-path]/api/config/settings/'
#  '[absolute-path]/api/config/,
#  '[absolute-path]/api/',
# ]
# Absolute path to the `api/` directory. Used when a setting needs a project relative path.
BASE_DIR = Path(__file__).resolve().parents[2]

# TODO: what does this do?
# Cryptographic key Django uses for sessions, password-reset tokens, etc.
# It must be supplied by DJANGO_SECRET_KEY in real deployments; the fallback is unsafe.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-development-key-change-me")

# enables verbose Django errors only when set to "true"
DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() == "true"

# hostnames Django will accept. Defaults to localhost and 127.0.0.1; 
# configure DJANGO_ALLOWED_HOSTS as comma-separated values in deployment.
ALLOWED_HOSTS = [host for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if host]

# INSTALLED_APPS loads Django features and third-party/project apps

INSTALLED_APPS = [
    # Django admin
    "django.contrib.admin",
    # authentication 
    "django.contrib.auth", 
    # The Content Types Framework is a built-in Django feature that 
    # allows you to create relationships between models in a more flexible way. 
    # It helps you deal with polymorphic relationships, 
    # where one model can relate to many different models, 
    # even if they are of different types.
    "django.contrib.contenttypes",
    # django.contrib.sessions is the built-in application that handles session management. 
    # It allows you to store and retrieve arbitrary data on a per-site-visitor basis, 
    # enabling stateless HTTP requests to behave like a stateful, continuous experience.
    "django.contrib.sessions",
    # The django.contrib.messages framework is Django's built-in application for handling 
    # "flash messages"—temporary, one-time notifications sent to users after an action 
    # (like logging in, submitting a form, or encountering an error). 
    # Once a message is displayed to the user, it is automatically cleared from the storage backend.
    # Handled entirely by Django's template engine
    "django.contrib.messages",
    "django.contrib.staticfiles", # static file supprt 
    # allows the frontend on a different origin to call this API.
    "corsheaders",
    # Django REST Framework for API endpoints.
    "rest_framework",
    # allauth and its Google provider: authentication, signup, and Google OAuth.
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # the project’s accounts app, including its custom user model.
    "apps.accounts",
]

# MIDDLEWARE runs on every request, in order
MIDDLEWARE = [
    # Security headers and session support.
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # CORS handling before Django’s common/CSRF behavior.
    "corsheaders.middleware.CorsMiddleware",
    # Normal Django request handling and CSRF enforcement.
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # Authentication, including Allauth’s account middleware.
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    # Flash messages and clickjacking protection.
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# routes begin in api/config/urls.py.
ROOT_URLCONF = "config.urls"

# enables Django templates, searches templates supplied by installed apps, 
# and exposes request/auth/messages helpers to templates.
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

# identifies the server entry point for traditional WSGI deployments such as Gunicorn.
WSGI_APPLICATION = "config.wsgi.application"

# DATABASES["default"] configures PostgreSQL. 
# Every part can be overridden with environment variables:
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DJANGO_DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("POSTGRES_DB", "inst_call"),
        "USER": os.environ.get("POSTGRES_USER", "inst_call"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "inst_call"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

# uses custom user model instead of Django’s built-in User
AUTH_USER_MODEL = "accounts.User"

# allows regular Django authentication plus Allauth authentication.
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# email is the login identity.
ACCOUNT_LOGIN_METHODS = {"email"}

# signup requires email and display_name; * means required.
ACCOUNT_SIGNUP_FIELDS = ["email*", "display_name*"]

# users do not need to verify their email. Convenient locally, usually not ideal for production.
ACCOUNT_EMAIL_VERIFICATION = "none"

# The username field is disabled; email is the user’s identity field.
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"

# sends a completed login to APP_ORIGIN, defaulting to http://localhost:3000.
LOGIN_REDIRECT_URL = os.environ.get("APP_ORIGIN", "http://localhost:3000")

# begins social login from a GET request
# convenient but worth reviewing for production flows.
SOCIALACCOUNT_LOGIN_ON_GET = True

# project-specific logic for social-login behavior,
SOCIALACCOUNT_ADAPTER = "apps.accounts.adapters.AccountAdapter"

# gets the Google OAuth client ID and secret from environment variables and requests only profile/email access.
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APPS": [{
            "client_id": os.environ.get("GOOGLE_OAUTH_CLIENT_ID", ""),
            "secret": os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET", ""),
            "key": "",
        }],
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

# makes the API session-authenticated by default
REST_FRAMEWORK = {
    # browser sessions/cookies authenticate API requests.
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"],
    # every API view is private unless it explicitly overrides this permission.
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
}

# canonical frontend URL, such as http://localhost:3000.
APP_ORIGIN = os.environ.get("APP_ORIGIN", "http://localhost:3000")

# frontend origins allowed to make cross-origin API calls.
CORS_ALLOWED_ORIGINS = [origin for origin in os.environ.get("CORS_ALLOWED_ORIGINS", APP_ORIGIN).split(",") if origin]
# permits cookies/session credentials on those calls.
CORS_ALLOW_CREDENTIALS = True
# origins permitted to send unsafe cookie-authenticated requests, such as POST/PATCH/DELETE.
CSRF_TRUSTED_ORIGINS = [origin for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", APP_ORIGIN).split(",") if origin]

# JavaScript cannot read the session cookie.
SESSION_COOKIE_HTTPONLY = True

# cookies are restricted on many cross-site requests.
SESSION_COOKIE_SAMESITE = "Lax"

# cookies require HTTPS outside debug mode.
SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = not DEBUG

# stores/handles datetimes as time-zone-aware UTC values.
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_TZ = True

# enables translation infrastructure
USE_I18N = True

# URL prefix for static assets.
STATIC_URL = "static/"

# new models use 64-bit integer primary keys by default.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
