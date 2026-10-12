import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager["User"]):
    """Manager for the email-only user model."""

    use_in_migrations = True

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        if not email:
            raise ValueError("The email address must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# database model definitions
# User replaces Django’s built-in user model
class User(AbstractUser):
    """The application identity; Google identities live in allauth's tables."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=150, blank=True)
    avatar_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # AbstractUser's username-based manager type is not compatible with this
    # email-only manager, despite Django supporting custom managers here.
    objects: UserManager = UserManager()  # pyright: ignore[reportIncompatibleVariableOverride]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    def __str__(self) -> str:
        return self.email
