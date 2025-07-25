from django.test import TestCase
from django.urls import reverse
from .models import URLMapping

class URLShortenerAPITests(TestCase):

    def test_shorten_url_success(self):
        """Test that a URL can be shortened successfully."""
        response = self.client.post(reverse('shorten_url'), {'url': 'https://www.example.com'}, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('short_code', data)
        self.assertTrue(URLMapping.objects.filter(short_code=data['short_code']).exists())

    def test_redirect_url_success(self):
        """Test that a short code redirects to the original URL and increments the click count."""
        mapping = URLMapping.objects.create(original_url='https://www.example.com')
        response = self.client.get(reverse('redirect_url', args=[mapping.short_code]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://www.example.com')
        mapping.refresh_from_db()
        self.assertEqual(mapping.clicks, 1)

    def test_get_stats_success(self):
        """Test that the stats endpoint returns the correct data."""
        mapping = URLMapping.objects.create(original_url='https://www.example.com', clicks=5)
        response = self.client.get(reverse('get_stats', args=[mapping.short_code]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['url'], 'https://www.example.com')
        self.assertEqual(data['clicks'], 5)
        self.assertIn('created_at', data)

    def test_redirect_url_not_found(self):
        """Test that a non-existent short code returns a 404 error."""
        response = self.client.get(reverse('redirect_url', args=['nonexistent']))
        self.assertEqual(response.status_code, 404)

    def test_shorten_url_invalid_url(self):
        """Test that submitting an invalid URL returns a 400 error."""
        response = self.client.post(reverse('shorten_url'), {'url': 'not-a-url'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)