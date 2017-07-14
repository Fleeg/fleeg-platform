from django.test import TestCase
from django.core.urlresolvers import reverse

from account.factories import AccountFactory, DEFAULT_PASSWORD


class TestLink(TestCase):
    def setUp(self):
        account = AccountFactory.create()
        new_link = {
            'url': '',
        }
        self.user = account.user

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

    def test_post_new_link_fails_url_empty(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('link_new'), data={})
        self.assertFormError(response, 'form', 'url', 'This field is required.')

    # test a private link

    def test_post_new_link_success(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('link_new'), data={'url': 'https://google.com'})
        self.assertRedirects(response, reverse('home'))

    def test_post_new_link_image_success(self):
        img_url = 'http://pudim.com.br/pudim.jpg'
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('link_new'), data={'url': img_url})
        self.assertRedirects(response, reverse('home'))

    def test_post_new_link_image_success(self):
        url_post = 'https://medium.com/@lucasboscaini/share-data-between-modules-and-components'
        url_post + '-with-angularjs-56d320a19b6f'
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('link_new'), data={'url': url_post})
        self.assertRedirects(response, reverse('home'))
