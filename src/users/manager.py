from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager

from .enums import Role


class UserManager(BaseUserManager):
    def create_user(
        self, email: str, password: str | None = None, **extra_field
    ):
        user = self.model(email=self.normalize_email(email), **extra_field)
        setattr(user, "password", make_password(password))
        user.save()

        return user

    def create_superuser(
        self, email: str, password: str | None = None, **extra_field
    ):
        return self.create_user(
            email=email,
            password=password,
            role=Role.SENIOR,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
