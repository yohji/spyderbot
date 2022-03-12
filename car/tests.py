from django.test import TestCase
from car.crawler import as24
from .models import Market


class CrawlerTestCase(TestCase):

    def setUp(self):

        Market('IT', 'Italy', 'I').save()
        Market('DE', 'Germany', 'D').save()

    def test_as24(self):

        cars = as24('triumph', 'spitfire', 1965, 1980, sleep = True)

        self.assertIsNotNone(cars, 'cars is None')
        self.assertNotEqual(len(cars), 0, 'cars is empty')
