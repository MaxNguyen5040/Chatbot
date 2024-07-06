import pickle

class DialogueManager:
    def __init__(self):
        with open('../models/intent_recognizer.pkl', 'rb') as f:
            self.vectorizer, self.model = pickle.load(f)

    def recognize_intent(self, text):
        X = self.vectorizer.transform([text])
        intent = self.model.predict(X)[0]
        return intent

    def handle_intent(self, intent):
        if intent == "operating_hours":
            return "Our operating hours are from 9 AM to 5 PM, Monday to Friday."
        elif intent == "reset_password":
            return "You can reset your password by clicking on the 'Forgot Password' link on the login page."
        else:
            return "I'm not sure how to help with that."

if __name__ == "__main__":
    manager = DialogueManager()
    print(manager.handle_intent(manager.recognize_intent("What are your operating hours?")))