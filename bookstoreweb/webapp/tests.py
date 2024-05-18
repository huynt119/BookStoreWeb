from django.test import TestCase, Client
from django.urls import reverse

class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)