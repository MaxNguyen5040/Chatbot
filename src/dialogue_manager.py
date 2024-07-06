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

    def handle_intent(self, intent):
        return generate_response(intent)

if __name__ == "__main__":
    manager = DialogueManager()
    print(manager.handle_intent(manager.recognize_intent("What is your pricing?")))
    print(manager.handle_intent(manager.recognize_intent("How can I contact you?")))