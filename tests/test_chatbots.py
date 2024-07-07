import unittest
from app import (
    translate_message, analyze_sentiment, handle_intent,
    query_knowledge_base, update_user_preferences, get_user_preferences,
    advanced_intent_recognition, update_conversation_history, get_conversation_history
)

class TestChatbot(unittest.TestCase):

    def test_translate_message(self):
        translated_text = translate_message("Hola", 'en')
        self.assertEqual(translated_text, "Hello")

    def test_analyze_sentiment(self):
        polarity, subjectivity = analyze_sentiment("I am happy")
        self.assertGreater(polarity, 0)

    def test_handle_intent_weather(self):
        response = handle_intent('weather_query', [{'entity': 'location', 'value': 'New York'}])
        self.assertIn("weather in New York", response)

    def test_handle_intent_flight(self):
        response = handle_intent('flight_booking', [{'entity': 'location', 'value': 'Paris'}, {'entity': 'date', 'value': '2024-07-01'}])
        self.assertIn("Booking a flight to Paris on 2024-07-01", response)

    def test_knowledge_base_query(self):
        response = query_knowledge_base("What is your name")
        self.assertEqual(response, "I am your friendly chatbot!")

    def test_update_user_preferences(self):
        user_id = "test_user"
        update_user_preferences(user_id, 'favorite_color', 'blue')
        self.assertEqual(get_user_preferences(user_id)['favorite_color'], 'blue')

    def test_advanced_intent_recognition(self):
        user_message = "What is the weather like in Paris?"
        advanced_intent = advanced_intent_recognition(user_message)
        self.assertIn("Paris", advanced_intent)

    def test_update_conversation_history(self):
        user_id = "test_user"
        user_message = "How's the weather?"
        response = "It's sunny."
        update_conversation_history(user_id, user_message, response)
        history = get_conversation_history(user_id)
        self.assertEqual(history[-1]['user_message'], user_message)
        self.assertEqual(history[-1]['response'], response)

if __name__ == '__main__':
    unittest.main()

