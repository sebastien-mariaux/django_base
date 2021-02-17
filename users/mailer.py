from urllib.parse import urljoin
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.conf import settings
from django.utils.translation import gettext as _


class UserMailer:
    from_email = None
    subject = _(f"Message from {settings.SITE_TITLE}")

    def __init__(self, user):
        self.user = user

    def send(self) -> None:
        send_mail(
            subject=self.subject,
            from_email=self.from_email,
            message=self.message(),
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def message(self):
        raise NotImplemented


class UpdateEmailMailer(UserMailer):
    subject = _(f'Confirm your new email for {settings.SITE_TITLE}')

    def message(self):
        return _(f"To confirm your new email please copy the following link "
                 f"in your browser : {self.email_link()}")

    def email_link(self):
        url = reverse('validate_new_email',
                      kwargs={
                          'validation_token': self.user.new_email_validation_token()
                      })
        return urljoin(settings.BASE_URL, url)


class ValidateAccountMailer(UserMailer):
    subject = _('Validation de votre adresse email')

    def message(self):
        return _(f"To confirm your account please copy the following link "
                 f"in your browser {self.email_link()}:")

    def email_link(self):
        url = reverse('validate_email',
                      kwargs={'validation_token': self.user.validation_token})
        return urljoin(settings.BASE_URL, url)
