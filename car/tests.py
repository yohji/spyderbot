from django.test import TestCase
from car.crawler import as24


class CrawlerTestCase(TestCase):

    def setUp(self):
        pass

    def test_as24(self):

        # self.assertEqual(as24(), 'without parameters')
        # self.assertEqual(as24('triumph'), 'maker is triumph')
        self.assertEqual(as24('triumph', 'spitfire'), 'maker is triumph and model is spitfire')
