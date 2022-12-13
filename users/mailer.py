from urllib.parse import urljoin
from django.shortcuts import reverse
from django.conf import settings
from django.utils.translation import gettext as _
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class UserMailer:
    from_email = None
    subject = _(f"Message from {settings.SITE_TITLE}")
    template = ""

    def __init__(self, user):
        self.user = user

    def send(self) -> None:
        msg = EmailMultiAlternatives(
            subject=self.subject,
            body=self.message(),
            from_email=self.from_email,
            to=[self.user.email],
        )
        msg.attach_alternative(self.html_message(), "text/html")
        msg.send()

    def message(self):
        raise NotImplementedError

    def html_message(self) -> str:
        return render_to_string(self.template, self.get_context())

    def get_context(self) -> dict:
        return {'link': self.email_link(), 'subject': self.subject}

    def email_link(self) -> str:    # pylint: disable=no-self-use
        return ""


class UpdateEmailMailer(UserMailer):
    subject = _(f'Confirm your new email for {settings.SITE_TITLE}')
    template = "users/email/update_email.html"

    def message(self):
        return _(f"To confirm your new email please copy the following link "
                 f"in your browser : {self.email_link()}")

    def email_link(self) -> str:
        url = reverse('validate_new_email',
                      kwargs={
                          'validation_token': self.user.new_email_validation_token()
                      })
        return urljoin(settings.BASE_URL, url)


class ValidateAccountMailer(UserMailer):
    subject = _('Email address validation')
    template = "users/email/validate_account.html"

    def message(self):
        return _(f"To confirm your account please copy the following link "
                 f"in your browser {self.email_link()}:")

    def email_link(self) -> str:
        url = reverse('validate_email',
                      kwargs={'validation_token': self.user.validation_token})
        return urljoin(settings.BASE_URL, url)
