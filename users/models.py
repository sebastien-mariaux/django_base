import jwt
from urllib.parse import urljoin
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

    def init_email_validation(self):
        self.generate_validation_token()
        self.send_email_activation_email()

    def generate_validation_token(self):
        self.validation_token = jwt.encode(
            {"user_id": self.id, "user_email": self.email},
            settings.SECRET_KEY, algorithm="HS256"
        )
        self.save()

    def send_email_activation_email(self):
        link = self.validation_url()
        send_mail(
            subject='Validation de votre adresse email',
            from_email='test@test.fr',
            message=f"Pour valider votre email, veuillez cliquer sur le lien suivant : {link}",
            recipient_list=[self.email],
            fail_silently=False,
        )

    def validation_url(self):
        url = reverse('validate-email',
                      kwargs={'validation_token': self.validation_token})
        return urljoin(settings.BASE_URL, url)
