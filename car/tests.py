from django.test import TestCase
from car.crawler import as24


class CrawlerTestCase(TestCase):

    def setUp(self):
        pass

    def test_as24(self):

        cars = as24('triumph', 'spitfire')

        self.assertIsNotNone(cars, 'cars is None')
        self.assertNotEqual(len(cars), 0, 'cars is empty')
