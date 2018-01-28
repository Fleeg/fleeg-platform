from django.test import TestCase
from django.core.urlresolvers import reverse

from account.factories import AccountFactory, RelationshipFactory, DEFAULT_PASSWORD
from link.factories import PostFactory


class TestSearch(TestCase):
    def setUp(self):
        account0 = AccountFactory.create(user__first_name='Search 0')
        account1 = AccountFactory.create(user__first_name='Search 1')
        account2 = AccountFactory.create(user__first_name='Search 2')
        RelationshipFactory.create(owner=account0, follow=account1)
        RelationshipFactory.create(owner=account1, follow=account2)
        [PostFactory.create(owner=account0, publisher=account0,
                            title='Search A', tags='search') for _ in range(2)]
        [PostFactory.create(owner=account1, publisher=account1,
                            title='Search B', tags='search') for _ in range(2)]
        [PostFactory.create(owner=account2, publisher=account2,
                            title='Search C', tags='search') for _ in range(2)]
        [PostFactory.create(title='Search D', tags='search') for _ in range(2)]
        self.user = account0.user

    def test_standard_search_anonymous(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('search'), {'q': 'search', 'anonymous': 1})
        search = response.context['search']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/list.html')
        self.assertEqual(len(search.results), 11)

    def test_standard_search(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('search'), {'q': 'search'})
        search = response.context['search']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/list.html')
        self.assertEqual(len(search.results), 11)

    def test_advanced_search_anonymous_by_user(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('search'), {'q': 'user:search', 'anonymous': 1})
        search = response.context['search']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/list.html')
        self.assertEqual(len(search.results), 3)

    def test_advanced_search_anonymous_by_title(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('search'), {'q': 'title:search', 'anonymous': 1})
        search = response.context['search']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/list.html')
        self.assertEqual(len(search.results), 8)

    def test_advanced_search_anonymous_by_tag(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('search'), {'q': 'tag:search', 'anonymous': 1})
        search = response.context['search']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/list.html')
        self.assertEqual(len(search.results), 8)

    def test_advanced_search_by_user(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('search'), {'q': 'user:search'})
        search = response.context['search']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/list.html')
        self.assertEqual(len(search.results), 3)

    def test_advanced_search_by_title(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('search'), {'q': 'title:search'})
        search = response.context['search']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/list.html')
        self.assertEqual(len(search.results), 8)

    def test_advanced_search_by_tag(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('search'), {'q': 'tag:search'})
        search = response.context['search']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/list.html')
        self.assertEqual(len(search.results), 8)

    def test_advanced_search_by_not_supported_key(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('search'), {'q': 'type:search'})
        search = response.context['search']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search/list.html')
        self.assertEqual(len(search.results), 0)
