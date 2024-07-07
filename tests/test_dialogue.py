import unittest
from dialogue_manager.py import generate_response

class TestDialogueManager(unittest.TestCase):

    def test_generate_response_greeting(self):
        response = generate_response('greeting', [])
        self.assertEqual(response, "Hello! How can I assist you today?")

    def test_generate_response_goodbye(self):
        response = generate_response('goodbye', [])
        self.assertEqual(response, "Goodbye! Have a great day!")

    def test_generate_response_unknown(self):
        response = generate_response('unknown', [])
        self.assertIn("I'm not sure how to help with that.", response)

if __name__ == '__main__':
    unittest.main()