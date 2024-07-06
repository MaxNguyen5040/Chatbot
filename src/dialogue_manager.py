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
        elif intent == "pricing":
            return "Our pricing varies depending on the service. Please visit our pricing page for more details."
        elif intent == "contact_info":
            return "You can contact us at support@example.com or call us at 123-456-7890."
        else:
            return "I'm not sure how to help with that."

if __name__ == "__main__":
    manager = DialogueManager()
    print(manager.handle_intent(manager.recognize_intent("What is your pricing?")))
    print(manager.handle_intent(manager.recognize_intent("How can I contact you?")))