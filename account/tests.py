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

    def test_login_fail_user_not_exists(self):
        response = self.client.post(reverse('account_login'), data={'identity': 'invaliduser',
                                                                    'password': 'invalidpassword'})
        self.assertTemplateUsed(response, 'index.html', 'Authentication failed.')

    @unittest.skip('Skip until coverage process to be added to project')
    def test_call_view_loads(self):
        self.client.login(username='user', password='test')
        response = self.client.get('/url/to/view')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversation.html')

    @unittest.skip('Skip until coverage process to be added to project')
    def test_call_view_fails_blank(self):
        self.client.login(username='user', password='test')
        response = self.client.post('/url/to/view', {})  # blank data dictionary
        self.assertFormError(response, 'form', 'some_field', 'This field is required.')
        # etc. ...

    @unittest.skip('Skip until coverage process to be added to project')
    def test_call_view_fails_invalid(self):
        # as above, but with invalid rather than blank data in dictionary
        self.assertTrue(True)

    @unittest.skip('Skip until coverage process to be added to project')
    def test_call_view_success_valid(self):
        self.client.login(username='user', password='test')
        response = self.client.post('/url/to/view', {})  # same again, but with valid data, then
        self.assertRedirects(response, '/contact/1/calls/')
