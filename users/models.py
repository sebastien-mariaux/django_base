from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


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
