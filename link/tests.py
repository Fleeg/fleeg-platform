import unittest
from django.test import TestCase
from django.core.urlresolvers import reverse

@unittest.skip('Skip until coverage process to be added to project')
class TestCalls(TestCase):
    def test_call_view_denies_anonymous(self):
        response = self.client.get('/url/to/view', follow=True)
        self.assertRedirects(response, '/login/')
        response = self.client.post('/url/to/view', follow=True)
        self.assertRedirects(response, '/login/')  # check what is the best for these three options...
        self.assertRedirects(response, reverse('login'))
        self.assertRedirects(response, 'link.views.login')

    def test_call_view_loads(self):
        self.client.login(username='user', password='test')  # defined in fixture or with factory in setUp()
        response = self.client.get('/url/to/view')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conversation.html')

    def test_call_view_fails_blank(self):
        self.client.login(username='user', password='test')
        response = self.client.post('/url/to/view', {})  # blank data dictionary
        self.assertFormError(response, 'form', 'some_field', 'This field is required.')
        # etc. ...

    def test_call_view_fails_invalid(self):
        # as above, but with invalid rather than blank data in dictionary
        self.assertTrue(True)

    def test_call_view_success_valid(self):
        self.client.login(username='user', password='test')
        response = self.client.post('/url/to/view', {})  # same again, but with valid data, then
        self.assertRedirects(response, '/contact/1/calls/')
