import unittest

from django.test import TestCase
from django.core.urlresolvers import reverse

from account.factories import AccountFactory, DEFAULT_PASSWORD


class TestAccounts(TestCase):
    def setUp(self):
        self.account = AccountFactory.create()
        self.user = self.account.user

    def test_logout_without_logged_in(self):
        response = self.client.get(reverse('account_logout'))
        self.assertRedirects(response, '{0}?next={1}'.format(reverse('account_login'),
                                                             reverse('account_logout')))

    def test_logout_with_logged_in(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('account_logout'))
        self.assertRedirects(response, reverse('index'))

    def test_redirect_home_logged_in(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('home'))

    def test_login_with_username_success(self):
        response = self.client.post(reverse('account_login'), data={'identity': self.user.username,
                                                                    'password': DEFAULT_PASSWORD})
        self.assertRedirects(response, reverse('home'))

    def test_login_with_email_success(self):
        response = self.client.post(reverse('account_login'), data={'identity': self.user.email,
                                                                    'password': DEFAULT_PASSWORD})
        self.assertRedirects(response, reverse('home'))

    def test_login_with_keep_connected(self):
        response = self.client.post(reverse('account_login'), data={'identity': self.user.username,
                                                                    'password': DEFAULT_PASSWORD,
                                                                    'keep_connected': True})
        self.assertRedirects(response, reverse('home'))

    def test_login_fails_user_not_exists(self):
        response = self.client.post(reverse('account_login'), data={'identity': 'invaliduser',
                                                                    'password': 'invalidpassword'})
        self.assertTemplateUsed(response, 'index.html', 'Authentication failed.')
    
    def test_login_fails_user_and_password_required(self):
        response = self.client.post(reverse('account_login'), data={})
        self.assertFormError(response, 'form', 'identity', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')
    
    def test_signup_with_success(self):
        new_user = AccountFactory.build().user
        
        form_data = {
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'username': new_user.username,
            'email': new_user.email,
            'password': DEFAULT_PASSWORD,
        }

        response = self.client.post(reverse('account_signup'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['formSignUp'].is_valid())
    
    def test_signup_fails_username_with_special_character(self):
        new_user = AccountFactory.build().user
        username_special_char = new_user.username + '/'
        
        form_data = {
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'username': username_special_char,
            'email': new_user.email,
            'password': DEFAULT_PASSWORD,
        }

        response = self.client.post(reverse('account_signup'), data=form_data)
        self.assertFormError(response, 'formSignUp', 'username', 'Username does not allow special characters.')
