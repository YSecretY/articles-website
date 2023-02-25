from django.test import TestCase
from django.urls import reverse


class SignUpTests(TestCase):
    name = 'New'
    email = 'new@email.com'

    def setUp(self):
        url = reverse('sign_up')
        self.response = self.client.get(url)

