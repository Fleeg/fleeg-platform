import requests

from unittest.mock import patch
from django.test import TestCase
from django.core.urlresolvers import reverse

from account.factories import AccountFactory, DEFAULT_PASSWORD
from link.factories import PostFactory, ReactionFactory


class TestLink(TestCase):
    def setUp(self):
        self.other_user = AccountFactory.create()
        self.other_user_post = PostFactory.create(owner=self.other_user, publisher=self.other_user)
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

    @patch('link.utils.requests.head')
    @patch('link.utils.Article')
    def test_post_new_link_success(self, mock_article, mock_req):
        mock_req.return_value.headers = {'Content-Type': 'text/plain'}

        mock_article.return_value.html = ''
        mock_article.return_value.text = 'text mock page'
        mock_article.return_value.title = 'title mock page'
        mock_article.return_value.meta_img = 'http://url-to-image/img.jpg'
        mock_article.return_value.meta_description = None
        mock_article.return_value.publish_date = None

        url_post = 'https://test.fleeg/valid-link'
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

    @patch('link.utils.requests.head')
    @patch('link.utils.Article')
    def test_post_new_link_news_success(self, mock_article, mock_req):
        html = '''
            <html>
            <head>
            <meta content="2015-04-09T10:25:24Z" property="og:pubdate"/>
            <meta content="http://www.cnn.com/2015/04/09/entertainment/
            feat-monty-python-holy-grail-40-years/index.html" property="og:url"/>
            <meta content="40 years of 'Holy Grail': The best of Monty Python - CNN"
            property="og:title"/><meta content='"Monty Python and the Holy Grail,"
            premiered 40 years ago. The timing was right for the
            British comedians (along with their token American, Terry Gilliam). '
            property="og:description"/>
            <meta property="og:empty_tag"/>
            <meta content="CNN" property="og:site_name"/>
            <meta content="article" property="og:type"/>
            <meta content="http://i2.cdn.cnn.com/cnnnext/dam/assets/
            150407084310-01-monty-python-super-169.jpg" property="og:image"/>
            <meta content="1100" property="og:image:width"/>
            <meta content="619" property="og:image:height"/>
            </head>
            </html>
        '''

        mock_req.return_value.headers = {'Content-Type': 'text/html'}
        mock_article.return_value.html = html
        mock_article.return_value.text = html
        mock_article.return_value.publish_date = None

        url_post = 'http://test.fleeg/valid-og-link'
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(reverse('link_new'), data={'url': url_post})
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(self.account.posts.all().count(), 3)

    def test_add_as_my_link_from_post(self):
        url = '{0}?next={1}'.format(reverse('link_add', args=[self.other_user_post.id]),
                                    reverse('home'))
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(url)
        self.assertRedirects(response, reverse('home'))

    def test_react_on_post(self):
        url = '{0}?next={1}'.format(reverse('link_react', args=[self.other_user_post.id]),
                                    reverse('home'))
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(url)
        self.assertRedirects(response, reverse('home'))

    def test_unreact_on_post(self):
        post_with_reaction = PostFactory.create(owner=self.other_user, publisher=self.other_user,)
        ReactionFactory.create(owner=self.account, post=post_with_reaction)
        url = '{0}?next={1}'.format(reverse('link_unreact', args=[post_with_reaction.id]),
                                    reverse('home'))
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(url)
        self.assertRedirects(response, reverse('home'))

    def test_comment_post_with_no_message(self):
        url = '{0}?next={1}'.format(reverse('link_comment', args=[self.other_user_post.id]),
                                    reverse('home'))
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(url)
        self.assertRedirects(response, reverse('home'))

    def test_comment_post(self):
        url = '{0}?next={1}'.format(reverse('link_comment', args=[self.other_user_post.id]),
                                    reverse('home'))
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.post(url, data={'text': 'my comment'})
        self.assertRedirects(response, reverse('home'))
