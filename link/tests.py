import requests

from unittest.mock import patch
from django.test import TestCase
from django.core.urlresolvers import reverse

from account.factories import AccountFactory, DEFAULT_PASSWORD
from link.factories import PostFactory


class TestLink(TestCase):
    def setUp(self):
        self.account = AccountFactory.create()
        self.user = self.account.user
        [PostFactory.create(owner=self.account, publisher=self.account) for _ in range(2)]

    def test_access_links_anonymous(self):
        response = self.client.get(reverse('links', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'link/link.html')

    def test_access_profile_logged_in(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('links', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'link/link.html')

    def test_access_home_logged_in(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTrue(response.context['posts'].count())

    def test_post_new_link_fails_url_empty(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('link_new'), data={})
        self.assertFormError(response, 'form', 'url', 'This field is required.')

    @patch('link.utils.requests.head')
    def test_post_new_fails_invalid_link(self, mock_req):
        mock_req.side_effect = requests.exceptions.RequestException
        url_post = 'http://test.fleeg/invalid-link'
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('link_new'), data={'url': url_post})
        self.assertFormError(response, 'form', None, 'Failed to read link.')

    def test_post_new_link_success(self):
        url_post = 'https://google.com'
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('link_new'), data={'url': url_post})
        self.assertRedirects(response, reverse('home'))

    @patch('link.utils.requests.head')
    def test_post_new_link_image_success(self, mock_req):
        mock_req.return_value.headers = {'Content-Type': 'image/jpg'}
        img_url = 'https://test.fleeg/valid-image-link'
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('link_new'), data={'url': img_url})
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(self.account.posts.all().count(), 3)

    def test_post_new_link_news_success(self):
        url_post = 'http://edition.cnn.com/2015/04/09/entertainment/'
        url_post += 'feat-monty-python-holy-grail-40-years/index.html'
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('link_new'), data={'url': url_post})
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(self.account.posts.all().count(), 3)
