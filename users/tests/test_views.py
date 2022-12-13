from django.core import mail
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.http import HttpResponse
from django.shortcuts import reverse
from django_base.test_helpers import TestHelpers
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
        self.assertIn('Please enter a correct username and password',
                      response.context['form'].errors['__all__'][0])

    def test_failure_wrong_password(self):
        response = self.client.post(
            self.url,
            {'username': 'jake.peralta@b99.com', 'password': 'invalid'},
            follow=True
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/login.html', response.template_name[0])
        self.assertIn('Please enter a correct username and password',
                      response.context['form'].errors['__all__'][0])


class RegisterTest(TestCase, TestHelpers):
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
        self.assertIn('A user with that username already exists',
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
        self.assertIn('It must contain at least 8 characters.',
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
        url = reverse('validate_email',
                      kwargs={'validation_token': user.validation_token})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        expected = "Thank you! Your account is now active."
        self.assert_content(response, expected)

    def test_user_confirmation_failure_invalid_token(self):
        active_before = UserModel.objects.filter(is_active=True).count()
        url = 'http://localhost:8000/account/activation/1234/'
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        expected = "Invalid activation link. Please contact an administrator"
        self.assert_content(response, expected)
        active_after = UserModel.objects.filter(is_active=True).count()
        self.assertEqual(active_after, active_before)

    def test_user_confirmation_failure_user_not_found(self):
        url = self.deleted_user_token_url()
        active_before = UserModel.objects.filter(is_active=True).count()
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        expected = "Invalid activation link. Please contact an administrator"
        self.assert_content(response, expected)
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
        url = reverse('validate_email',
                      kwargs={'validation_token': self.user.validation_token})
        self.user.delete()
        return url


class AccountTest(TestCase, TestHelpers):
    url = reverse('profile')

    def setUp(self):
        create_user_amy()
        self.user = create_user_jake()
        self.client.force_login(self.user)

    def test_get_profile_page(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/profile.html', response.template_name[0])
        self.assert_content(response, self.user.first_name)
        self.assert_content(response, self.user.last_name)
        self.assert_content(response, self.user.email)
        self.assert_content(response, self.user.username)
        self.assert_content(response, 'Edit')

    def test_get_edit_page(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/edit.html', response.template_name[0])
        self.assert_content(response, "Username")
        self.assert_content(response, self.user.username)
        self.assert_content(response, 'First name')
        self.assert_content(response, 'Last name')
        self.assert_content(response, 'Edit profile')
        self.assert_no_content(response, 'Email')

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


class UpdateEmailTest(TestCase, TestHelpers):
    def setUp(self) -> None:
        self.user = create_user_jake()
        self.client.force_login(self.user)

    def test_update_email_view(self):
        response = self.client.get(reverse('update_email'), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/edit_email.html', response.template_name[0])

    def test_require_update(self):
        data = {'next_email': 'jackie_baracuda@b99.com'}
        response = self.client.post(reverse('update_email'), data, follow=True)
        self.user.refresh_from_db()
        self.assertEqual('jackie_baracuda@b99.com', self.user.next_email)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual('users/profile.html', response.template_name[0])
        self.assert_message(response,
                            'Please check your mailbox to confirm your new email')

    def test_validate_new_email(self):
        self.user.next_email = 'jackie_baracuda@b99.com'
        self.user.save()
        url = reverse('validate_new_email',
                      kwargs={
                          'validation_token': self.user.new_email_validation_token()
                      })
        response = self.client.get(url, follow=True)
        self.assertEqual(200, response.status_code)
        self.user.refresh_from_db()
        self.assertEqual('jackie_baracuda@b99.com', self.user.email)
        self.assertIsNone(self.user.next_email)
        self.assertEqual('users/profile.html', response.template_name[0])
        self.assert_message(response,
                            'Your email has been successfully updated')

    def test_available_next_email(self):
        amy = create_user_amy()
        data = {'next_email': amy.email}
        response = self.client.post(reverse('update_email'), data, follow=True)
        self.user.refresh_from_db()
        self.assertIsNone(self.user.next_email)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual('users/edit_email.html', response.template_name[0])
        self.assert_content(response, 'This email is already used')

    def test_validation_failure_email_taken(self):
        amy = create_user_amy()
        self.user.next_email = amy.email
        self.user.save()
        url = reverse('validate_new_email',
                      kwargs={
                          'validation_token': self.user.new_email_validation_token()
                      })
        response = self.client.get(url, follow=True)
        self.assertEqual(200, response.status_code)
        self.user.refresh_from_db()
        self.assertEqual('jake.peralta@b99.com', self.user.email)
        self.assertEqual('users/profile.html', response.template_name[0])
        self.assert_message(response, 'A user with that email already exists.')


class ChangePasswordTest(TestCase, TestHelpers):
    def setUp(self) -> None:
        self.user = create_user_jake()
        self.client.force_login(self.user)

    def test_password_change_success(self):
        url = reverse('change_password')
        data = {'old_password': 'rosa1234', 'new_password1': 'nouveau1234',
                'new_password2': 'nouveau1234'}
        response = self.client.post(url, data, follow=True)
        self.assertEqual(200, response.status_code)
        self.assert_message(response, 'Your password has been modified')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('nouveau1234'))
        self.assertEqual('users/profile.html', response.template_name[0])

    def test_password_change_failure(self):
        url = reverse('change_password')
        data = {'old_password': 'rosa1234', 'new_password1': 'aa',
                'new_password2': 'aa'}
        response = self.client.post(url, data, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/change_password.html', response.template_name[0])
        self.assertFalse(self.user.check_password('nouveau1234'))
        self.assert_content(response,
                            'It must contain at least 8 characters.')
