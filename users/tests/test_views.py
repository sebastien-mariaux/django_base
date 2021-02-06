
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

UserModel = get_user_model()


class LoginTest(TestCase):
    url = reverse('login')

    def setUp(self):
        UserModel.objects.create_user(
            email="jake.peralta@b99.com", username='baracuda',
            first_name="Jake", last_name="Peralta", password='rosa1234'
        )

    def test_login_page(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/login.html', response.template_name[0])

    def test_success_with_username(self):
        response = self.client.post(
            self.url,
            {'username': 'baracuda', 'password': 'rosa1234'},
            follow=True
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual('home.html', response.template_name[0])

    def test_success_with_email(self):
        response = self.client.post(
            self.url,
            {'username': 'jake.peralta@b99.com', 'password': 'rosa1234'},
            follow=True
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual('home.html', response.template_name[0])

    def test_failure_unknown_user(self):
        response = self.client.post(
            self.url,
            {'username': 'invalid', 'password': 'rosa1234'},
            follow=True
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/login.html', response.template_name[0])
        self.assertIn('Saisissez un nom d’utilisateur et un mot de passe valides',
                      response.context['form'].errors['__all__'][0])

    def test_failure_wrong_password(self):
        response = self.client.post(
            self.url,
            {'username': 'jake.peralta@b99.com', 'password': 'invalid'},
            follow=True
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/login.html', response.template_name[0])
        self.assertIn('Saisissez un nom d’utilisateur et un mot de passe valides',
                      response.context['form'].errors['__all__'][0])
