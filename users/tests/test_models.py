from django.test import TestCase
from django.core import mail
from users.models import EmailUser
from .test_data import create_user_jake, create_inactive_user


class UserTest(TestCase):
        # def test_init_email_validation(self):
        #     jake = create_user_jake()
        #     self.assertIsNone(jake.validation_token)
        #     jake.init_email_validation()
        #     self.assertIsNotNone(jake.validation_token)
        #     self.assertEqual(len(mail.outbox), 1)

    def test_validate(self):
        inactive_user = create_inactive_user()
        self.assertFalse(inactive_user.is_active)
        inactive_user.generate_validation_token()
        self.assertIsNotNone(inactive_user.validation_token)
        inactive_user.validate()
        self.assertIsNone(inactive_user.validation_token)
        self.assertTrue(inactive_user.is_active)
