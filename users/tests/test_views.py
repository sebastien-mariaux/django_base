from django.core import mail
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.http import HttpResponse
from django.shortcuts import reverse
from .test_data import create_user_amy, create_user_jake, create_inactive_user

UserModel = get_user_model()


class LoginTest(TestCase):
    url = reverse('login')

    def setUp(self):
        create_user_jake()

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


class RegisterTest(TestCase):
    url = reverse('register')

    def setUp(self):
        self.user = create_user_jake()

    def test_register_page(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/register.html', response.template_name[0])

    def test_success(self):
        response = self.register_valid_user()
        self.assertEqual('users/login.html', response.template_name[0])

    def test_failure_invalid_email_or_username(self):
        response = self.client.post(
            self.url,
            {'email': 'jake.peralta@b99.com', 'username': 'baracuda',
             'password1': 'badass101', 'password2': 'badass101'},
            follow=True
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/register.html', response.template_name[0])
        self.assertIn('A user with that email already exists',
                      response.context['form'].errors['email'][0])
        self.assertIn('Un utilisateur avec ce nom existe déjà.',
                      response.context['form'].errors['username'][0])

    def test_failure_invalid_password(self):
        response = self.client.post(
            self.url,
            {'email': 'rosa.diaz@b99.com', 'username': 'Rosa',
             'password1': '123', 'password2': '123'},
            follow=True
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/register.html', response.template_name[0])
        self.assertIn('doit contenir au minimum 8 caractères.',
                      response.context['form'].errors['password2'][0])

    def test_user_inactive_after_registration(self):
        self.register_valid_user()
        user = UserModel.objects.get(email='rosa.diaz@b99.com')
        self.assertFalse(user.is_active)

    def test_generate_auth_token(self):
        self.register_valid_user()
        user = UserModel.objects.get(email='rosa.diaz@b99.com')
        self.assertIsNotNone(user.validation_token)

    def test_confirmation_email_sent(self):
        self.register_valid_user()
        user = UserModel.objects.get(email='rosa.diaz@b99.com')
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(user.validation_token, mail.outbox[0].body)
        expected_url = f"localhost:8000/account/activation/{user.validation_token}"
        self.assertIn(expected_url, mail.outbox[0].body)

    def test_user_confirmation_success(self):
        user = create_inactive_user()
        url = user.validation_url()
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        expected = "Thank you! Your account is now active."
        self.assertIn(expected, response.content.decode())

    def test_user_confirmation_failure_invalid_token(self):
        active_before = UserModel.objects.filter(is_active=True).count()
        url = 'http://localhost:8000/account/activation/1234/'
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        expected = "Invalid activation link. Please contact an administrator"
        self.assertIn(expected, response.content.decode())
        active_after = UserModel.objects.filter(is_active=True).count()
        self.assertEqual(active_after, active_before)

    def test_user_confirmation_failure_user_not_found(self):
        url = self.deleted_user_token_url()
        active_before = UserModel.objects.filter(is_active=True).count()
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        expected = "Invalid activation link. Please contact an administrator"
        self.assertIn(expected, response.content.decode())
        active_after = UserModel.objects.filter(is_active=True).count()
        self.assertEqual(active_after, active_before)

    def register_valid_user(self) -> HttpResponse:
        response = self.client.post(
            self.url,
            {'email': 'rosa.diaz@b99.com', 'username': 'Rosa',
             'password1': 'badass101', 'password2': 'badass101'},
            follow=True
        )
        self.assertEqual(200, response.status_code)
        return response

    def deleted_user_token_url(self):
        self.user.generate_validation_token()
        url = self.user.validation_url()
        self.user.delete()
        return url


class AccountTest(TestCase):
    url = reverse('profile')

    def setUp(self):
        create_user_amy()
        self.user = create_user_jake()
        self.client.force_login(self.user)

    def test_get_profile_page(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/profile.html', response.template_name[0])
        self.assertIn(self.user.first_name, response.content.decode('utf-8'))
        self.assertIn(self.user.last_name, response.content.decode('utf-8'))
        self.assertIn(self.user.email, response.content.decode('utf-8'))
        self.assertIn(self.user.username, response.content.decode('utf-8'))
        self.assertIn('Edit', response.content.decode('utf-8'))

    def test_get_edit_page(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/edit.html', response.template_name[0])
        self.assertIn("Nom d’utilisateur", response.content.decode('utf-8'))
        self.assertIn(self.user.username, response.content.decode('utf-8'))
        self.assertIn('Prénom', response.content.decode('utf-8'))
        self.assertIn('Nom', response.content.decode('utf-8'))
        self.assertIn('Edit profile', response.content.decode('utf-8'))
        self.assertNotIn('Adresse électronique', response.content.decode('utf-8'))

    def test_update_profile(self):
        data = {'username': 'jajake'}
        response = self.client.post(reverse('edit_profile'), data, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/profile.html', response.template_name[0])
        self.user.refresh_from_db()
        self.assertEqual('jajake', self.user.username)

    def test_update_profile_fail_username_taken(self):
        data = {'username': 'Aby'}
        response = self.client.post(reverse('edit_profile'), data)
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/edit.html', response.template_name[0])
        self.user.refresh_from_db()
        self.assertEqual('baracuda', self.user.username)

    def test_cannot_update_email(self):
        data = {'email': 'jperalta@gmail.com'}
        response = self.client.post(reverse('edit_profile'), data)
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/edit.html', response.template_name[0])
        self.user.refresh_from_db()
        self.assertEqual('jake.peralta@b99.com', self.user.email)


class AuthenticatedOnlyPages(TestCase):
    def test_account_page(self):
        self.assert_redirected_to_login('profile')

    def assert_redirected_to_login(self, url_name):
        url = reverse(url_name)
        response = self.client.get(url, follow=True)
        self.assertEqual('users/login.html', response.template_name[0])
