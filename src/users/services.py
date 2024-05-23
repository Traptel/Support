import uuid

from .models import ActivationKey, User
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
        self,
        internal_user_id: int,
        activation_key: uuid.UUID,
    ):
        ActivationKey.objects.create(
            user_id=internal_user_id,
            key=activation_key,
        )

    def validate_activation(self, user: User, activation: ActivationKey):
        user.is_active = True
        user.save()
        activation.delete()
        send_email_activation_success.delay(recipient=self.email)
