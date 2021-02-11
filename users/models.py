from urllib.parse import urljoin
import jwt
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
from django.core.mail import send_mail


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

    def init_email_validation(self) -> None:
        self.generate_validation_token()
        self.send_email_activation_email()

    def generate_validation_token(self):
        self.validation_token = jwt.encode(
            {"user_id": self.id, "user_email": self.email},
            settings.SECRET_KEY, algorithm="HS256"
        )
        self.save()

    def send_email_activation_email(self) -> None:
        link = self.validation_url()
        send_mail(
            subject='Validation de votre adresse email',
            from_email='test@test.fr',
            message=f"Pour valider votre email, veuillez cliquer sur "
                    f"le lien suivant : {link}",
            recipient_list=[self.email],
            fail_silently=False,
        )

    def validation_url(self) -> str:
        url = reverse('validate_email',
                      kwargs={'validation_token': self.validation_token})
        return urljoin(settings.BASE_URL, url)

    def new_email_validation_url(self) -> str:
        url = reverse('validate_new_email',
                      kwargs={'validation_token': self.new_email_validation_token})

    def new_email_validation_token(self):
        return jwt.encode(
            {"user_id": self.id, "user_email": self.email,
             "next_email": self.next_email},
            settings.SECRET_KEY, algorithm="HS256"
        )

    def validate(self):
        self.is_active = True
        self.validation_token = None
        self.save()
