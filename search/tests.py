from django.test import TestCase
from django.core.urlresolvers import reverse

from account.factories import AccountFactory, DEFAULT_PASSWORD
from link.factories import PostFactory


class TestSearch(TestCase):
    def setUp(self):
        self.account = AccountFactory.create()
        self.user = self.account.user
        [PostFactory.create(owner=self.account, publisher=self.account) for _ in range(2)]

    def test_standard_search_anonymous(self):
        print('qqqq')
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('search'), {'q': 'test', 'anonymous': 1})
        search = response.context['search']
        print(len(search.results))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/list.html')

    def test_standard_search(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('search'), {'q': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/list.html')
