from django.test import TestCase
from .test_data import create_inactive_user


class UserTest(TestCase):

    def test_validate(self):
        inactive_user = create_inactive_user()
        self.assertFalse(inactive_user.is_active)
        inactive_user.generate_validation_token()
        self.assertIsNotNone(inactive_user.validation_token)
        inactive_user.validate()
        self.assertIsNone(inactive_user.validation_token)
        self.assertTrue(inactive_user.is_active)
