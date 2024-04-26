from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self, email: str, password: str | None = None, **extra_field
    ):
        user = self.model(email=self.normalize_email(email), **extra_field)
        setattr(user, "password", make_password(password))
        user.save()

        return user

    def creat_superuser(
        self, email: str, password: str | None = None, **extra_field
    ):
        pass
