from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


from account.factories import AccountFactory, RelationshipFactory, DEFAULT_PASSWORD


class TestAccount(TestCase):
    def setUp(self):
        new_user = AccountFactory.build().user
        self.account = AccountFactory.create()
        self.user = self.account.user
        self.form_login = {
            'identity': self.user.username,
            'password': DEFAULT_PASSWORD,
            #'keep_connected': False,
        }
        self.form_user = {
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'username': new_user.username,
            'email': new_user.email,
            'password': DEFAULT_PASSWORD,
        }

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

    def test_login_with_redirect_next_page(self):
        response = self.client.post('{0}?next={1}'.format(reverse('account_login'),
                                                          reverse('account_settings')),
                                    data=self.form_login)
        self.assertRedirects(response, reverse('account_settings'))

    def test_login_with_username_success(self):
        response = self.client.post(reverse('account_login'), data=self.form_login)
        self.assertRedirects(response, reverse('home'))

    def test_login_with_email_success(self):
        self.form_login['identity'] = self.user.email.upper()
        response = self.client.post(reverse('account_login'), data=self.form_login)
        self.assertRedirects(response, reverse('home'))

    def test_login_with_keep_connected(self):
        self.form_login['keep_connected'] = True
        response = self.client.post(reverse('account_login'), data=self.form_login)
        self.assertRedirects(response, reverse('home'))

    def test_login_fails_user_not_exists(self):
        invalid_login = {
            'identity': 'invalid',
            'password': 'invalid',
        }
        response = self.client.post(reverse('account_login'), data=invalid_login)
        self.assertTemplateUsed(response, 'index.html', 'Authentication failed.')

    def test_login_fails_password_not_valid(self):
        invalid_login = {
            'identity': self.form_login['identity'],
            'password': 'invalid',
        }
        response = self.client.post(reverse('account_login'), data=invalid_login)
        self.assertFormError(response, 'form', None, errors=None)

    def test_login_fails_identity_and_password_empty(self):
        response = self.client.post(reverse('account_login'), data={})
        self.assertFormError(response, 'form', 'identity', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_signup_with_success(self):
        response = self.client.post(reverse('account_signup'), data=self.form_user)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['formSignUp'].is_valid())

    def test_signup_fails_username_with_special_character(self):
        username_special_char = self.form_user['username'] + '/'
        self.form_user['username'] = username_special_char
        response = self.client.post(reverse('account_signup'), data=self.form_user)
        self.assertFormError(response, 'formSignUp', 'username',
                             'Username does not allow special characters.')

    def test_signup_fails_with_empty_form(self):
        response = self.client.post(reverse('account_signup'), data={})
        self.assertFormError(response, 'formSignUp', 'email', 'This field is required.')
        self.assertFormError(response, 'formSignUp', 'password', 'This field is required.')
        self.assertFormError(response, 'formSignUp', 'username', 'This field is required.')
        self.assertFormError(response, 'formSignUp', 'first_name', 'This field is required.')
        self.assertFormError(response, 'formSignUp', 'last_name', 'This field is required.')

    def test_access_profile_anonymous(self):
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_access_profile_logged_in(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_access_profile_user_not_found(self):
        response = self.client.get(reverse('profile', args=['notfound']))
        self.assertEqual(response.status_code, 404)

    def test_get_following_anonymous(self):
        response = self.client.get(reverse('following', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/user.html')

    def test_get_following_logged_in(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('following', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/user.html')

    def test_get_followers_anonymous(self):
        response = self.client.get(reverse('followers', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/user.html')

    def test_get_followers_logged_in(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('followers', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/user.html')

    def test_follow_other_user(self):
        user2 = AccountFactory.create().user
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('account_follow', args=[user2.username]))
        self.assertRedirects(response, reverse('profile', args=[user2.username]))

    def test_follow_following_user(self):
        account2 = AccountFactory.create()
        RelationshipFactory.create(owner=self.account, follow=account2)
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('account_follow', args=[account2.user.username]))
        self.assertRedirects(response, reverse('profile', args=[account2.user.username]))

    def test_unfollow_following_user(self):
        account2 = AccountFactory.create()
        RelationshipFactory.create(owner=self.account, follow=account2)
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('account_unfollow', args=[account2.user.username]))
        self.assertRedirects(response, reverse('profile', args=[account2.user.username]))

    def test_settings_update_info(self):
        settings_info = {'first_name': self.user.first_name, 'last_name': self.user.last_name,
                         'password': '', 'confirm_password': ''}
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('account_settings'), data=settings_info)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].is_valid())

    def test_settings_update_info_fails_with_empty_form(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('account_settings'), data={})
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')
        self.assertFormError(response, 'form', 'last_name', 'This field is required.')

    def test_settings_update_password(self):
        settings_info = {'first_name': self.user.first_name, 'last_name': self.user.last_name,
                         'password': 'new', 'confirm_password': 'new'}
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('account_settings'), data=settings_info)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].is_valid())

    def test_settings_update_password_fails_confirmation(self):
        settings_info = {'first_name': self.user.first_name, 'last_name': self.user.last_name,
                         'password': 'new', 'confirm_password': 'old'}
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('account_settings'), data=settings_info)
        self.assertFormError(response, 'form', None,
                             'Password confirmation does not equal with password.')

    @patch('account.views.FileSystemStorage')
    @patch('account.models.FileSystemStorage')
    def test_settings_new_upload_image(self, mock_views_fs, mock_models_fs):
        mock_views_fs.return_value.exists = MagicMock(return_value=False)
        mock_models_fs.return_value.exists = MagicMock(return_value=False)

        file = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('account_settings_upload'), data={'user_avatar': file})
        self.assertRedirects(response, reverse('account_settings'))

    @patch('account.views.FileSystemStorage')
    @patch('account.models.FileSystemStorage')
    def test_settings_change_upload_image(self, mock_views_fs, mock_models_fs):
        mock_views_fs.return_value.exists = MagicMock(return_value=True)
        mock_models_fs.return_value.exists = MagicMock(return_value=True)

        file = SimpleUploadedFile('image.jpg', content=None, content_type='image/jpg')
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('account_settings_upload'), data={'user_avatar': file})
        self.assertRedirects(response, reverse('account_settings'))

    def test_settings_upload_no_image(self):
        file = SimpleUploadedFile('image.gif', content=None, content_type='image/gif')
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('account_settings_upload'), data={'user_avatar': file})
        self.assertRedirects(response, reverse('account_settings'))
