import pickle
from response_generator.py import generate_response

class DialogueManager:
    def __init__(self):
        with open('../models/intent_recognizer.pkl', 'rb') as f:
            self.vectorizer, self.model = pickle.load(f)

    def recognize_intent(self, text):
        X = self.vectorizer.transform([text])
        intent = self.model.predict(X)[0]
        return intent

    def handle_intent(intent, entities):
        try:
            if intent == 'weather_query':
                location = next((entity['value'] for entity in entities if entity['entity'] == 'location'), None)
                if not location:
                    raise ValueError("Location not provided")
                return f"Fetching weather for {location}..."
            elif intent == 'flight_booking':
                destination = next((entity['value'] for entity in entities if entity['entity'] == 'location'), None)
                date = next((entity['value'] for entity in entities if entity['entity'] == 'date'), None)
                if not destination or not date:
                    raise ValueError("Destination or date not provided")
                return f"Booking a flight to {destination} on {date}."
            else:
                return "I'm not sure how to help with that."
        except Exception as e:
            return str(e)

    def generate_response(intent, entities):
        if intent == 'greeting':
            return "Hello! How can I assist you today?"
        elif intent == 'goodbye':
            return "Goodbye! Have a great day!"
        else:
            return handle_intent(intent, entities)
if __name__ == "__main__":
    manager = DialogueManager()
    print(manager.handle_intent(manager.recognize_intent("What is your pricing?")))
    print(manager.handle_intent(manager.recognize_intent("How can I contact you?")))