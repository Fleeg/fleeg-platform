from django.test import TestCase
from django.core.urlresolvers import reverse


class TestError(TestCase):
    def test_bad_request(self):
        response = self.client.get(reverse('bad_request'))
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'error/error.html')

    def test_permission_denied(self):
        response = self.client.get(reverse('permission_denied'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'error/error.html')

    def test_not_found_page(self):
        response = self.client.get(reverse('page_not_found'))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'error/error.html')

    def test_server_error(self):
        response = self.client.get(reverse('server_error'))
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'error/error.html')
