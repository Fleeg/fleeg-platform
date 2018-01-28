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
        [PostFactory.create(owner=account0, publisher=account0, title='Search A') for _ in range(2)]
        [PostFactory.create(owner=account1, publisher=account1, title='Search B') for _ in range(2)]
        [PostFactory.create(owner=account2, publisher=account2, title='Search C') for _ in range(2)]
        [PostFactory.create(title='Search D') for _ in range(2)]
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
