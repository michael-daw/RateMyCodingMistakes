from django.test import SimpleTestCase
from django.urls import reverse, resolve
from RateMyCodingMistakes.views import home, about, sitemap, contact, account, user_login, user_logout, new_post, register, hot, alltime, new, show_category, show_categories, get_server_side_cookie, visitor_cookie_handler

class TestUrls(SimpleTestCase):
    def test_main_urls(self):
        url = reverse('main')
        self.assertEquals(resolve(url).func, home)
