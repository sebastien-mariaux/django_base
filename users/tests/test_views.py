
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

UserModel = get_user_model()


def create_user_jake():
    user = UserModel.objects.create_user(
        email="jake.peralta@b99.com", username='baracuda',
        first_name="Jake", last_name="Peralta", password='rosa1234'
    )
    return user


def create_user_amy():
    user = UserModel.objects.create_user(
        email="amy.santiago@b99.com", username='Aby',
        first_name="Amy", last_name="Santiago", password='philatelie'
    )
    return user


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
        create_user_jake()

    def test_register_page(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual('users/register.html', response.template_name[0])

    def test_success(self):
        response = self.client.post(
            self.url,
            {'email': 'rosa.diaz@b99.com', 'username': 'Rosa',
             'password1': 'badass101', 'password2': 'badass101'},
            follow=True
        )
        self.assertEqual(200, response.status_code)
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
