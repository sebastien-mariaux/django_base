from typing import Optional
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import EmailUser

UserModel = get_user_model()


def user_from_token(token) -> Optional[EmailUser]:
    if body := decode_token(token):
        return token_user(body)     # type: ignore
    return None


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY,
                          algorithms="HS256")  # type: ignore
    except jwt.exceptions.DecodeError:
        return None


def token_user(body: dict) -> Optional[EmailUser]:
    try:
        return UserModel.objects.get(
            id=body['user_id'], email=body['user_email']
        )
    except UserModel.DoesNotExist:
        return None
