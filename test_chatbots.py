import unittest

class TestChatbot(unittest.TestCase):

    def test_translate_message(self):
        self.assertEqual(translate_message("Hola", 'en'), "Hello")
    
    def test_analyze_sentiment(self):
        polarity, subjectivity = analyze_sentiment("I am happy")
        self.assertGreater(polarity, 0)

    def test_handle_intent(self):
        self.assertEqual(handle_intent('weather_query', [{'entity': 'location', 'value': 'New York'}]), "The weather in New York is clear sky with a temperature of 20.00°C.")
    
    def test_knowledge_base_query(self):
        self.assertEqual(query_knowledge_base("What is your name"), "I am your friendly chatbot!")
    
    def test_update_user_preferences(self):
        user_id = "test_user"
        update_user_preferences(user_id, 'favorite_color', 'blue')
        self.assertEqual(get_user_preferences(user_id)['favorite_color'], 'blue')

if __name__ == '__main__':
    unittest.main()
