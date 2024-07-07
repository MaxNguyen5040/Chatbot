import unittest
from location_based_discussions import get_local_news, get_local_weather

class TestLocationBasedDiscussions(unittest.TestCase):

    def test_get_local_news_new_york(self):
        news = get_local_news("New York")
        self.assertIn("New York", news)

    def test_get_local_news_unknown(self):
        news = get_local_news("Unknown")
        self.assertEqual(news, "No news available for this location.")

    def test_get_local_weather_new_york(self):
        weather = get_local_weather("New York")
        self.assertIn("New York", weather)

    def test_get_local_weather_unknown(self):
        weather = get_local_weather("Unknown")
        self.assertEqual(weather, "Weather data not available for this location.")

if __name__ == '__main__':
    unittest.main()