import uuid

from shared.cache import CacheService

from .models import User
from .tasks import send_activation_mail, send_email_activation_success


class Activator:
    def __init__(self, email: str) -> None:
        self.email = email

    def create_activation_key(self):
        return uuid.uuid3(namespace=uuid.uuid4(), name=self.email)

    def create_activation_link(self, activation_key: uuid.UUID):
        return f"https://frontend.com/users/activate/{activation_key}"

    def send_user_activation_email(self, activation_key: uuid.UUID):

        activation_link = self.create_activation_link(activation_key)

        send_activation_mail.delay(
            recipient=self.email,
            activation_link=activation_link,
        )

    def save_activation_information(
        self, internal_user_id: int, activation_key: uuid.UUID
    ):
        cache = CacheService()
        payload = {"user_id": internal_user_id}
        cache.save(
            namespace="activation",
            key=str(activation_key),
            instance=payload,
            ttl=2_000,
        )

    def validate_activation(self, key: str):
        cache = CacheService()
        activation_data = cache.get(namespace="activation", key=key)
        user_id = activation_data.get("user_id")
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        cache.delete(namespace="activation", key=str(key))
        send_email_activation_success.delay(recipient=self.email)
