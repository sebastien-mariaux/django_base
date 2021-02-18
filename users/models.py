import jwt
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
from .mailer import ValidateAccountMailer


class DatedModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"),
        auto_now=True
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class EmailUser(AbstractUser):
    email = models.EmailField(
        _('email address'),
        blank=False,
        null=False,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    next_email = models.EmailField(
        _('next email address'),
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"),
        auto_now=True
    )
    validation_token = models.CharField(
        verbose_name=_('validation token'),
        max_length=255,
        null=True, blank=True,
    )

    def generate_validation_token(self):
        self.validation_token = jwt.encode(
            {"user_id": self.id, "user_email": self.email},
            settings.SECRET_KEY, algorithm="HS256"
        )
        self.save()

    def send_email_activation_email(self) -> None:
        mailer = ValidateAccountMailer(self)
        mailer.send()

    def new_email_validation_token(self) -> str:
        return jwt.encode(
            {"user_id": self.id, "user_email": self.email,
             "next_email": self.next_email},
            settings.SECRET_KEY, algorithm="HS256"
        )

    def validate(self):
        self.is_active = True
        self.validation_token = None
        self.save()

    def replace_email(self):
        self.email = self.next_email
        self.next_email = None
        self.full_clean()
        self.save()
