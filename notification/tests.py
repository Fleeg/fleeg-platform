from django.test import TestCase
from django.core.urlresolvers import reverse

from account.factories import AccountFactory, DEFAULT_PASSWORD


class TestNotification(TestCase):
    def setUp(self):
        account = AccountFactory.create()
        self.user = account.user

    def test_access_notification_list(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notification/list.html')
