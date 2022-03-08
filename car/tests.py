from django.test import TestCase
from car.crawler import autoscout24


class CrawlerTestCase(TestCase):

    def setUp(self):
        pass

    def test_autoscout24(self):

        # self.assertEqual(autoscout24(), 'without parameters')
        # self.assertEqual(autoscout24('triumph'), 'maker is triumph')
        self.assertEqual(autoscout24('triumph', 'spitfire'), 'maker is triumph and model is spitfire')
