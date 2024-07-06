from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
from rasa_nlu.model import Interpreter

interpreter = Interpreter.load("models/nlu")

def recognize_intent(user_message):
    result = interpreter.parse(user_message)
    intent = result['intent']['name']
    entities = result['entities']
    return intent, entities

def train_intent_recognizer(data):
    questions, intents, label_encoder = preprocess_data(data)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(questions)
    model = MultinomialNB()
    model.fit(X, intents)
    return vectorizer, model, label_encoder

if __name__ == "__main__":
    data = [
        ("What are your operating hours?", "operating_hours"),
        ("How can I reset my password?", "reset_password"),
        ("What is your pricing?", "pricing"),
        ("How can I contact you?", "contact_info"),
        ("Where is your office located?", "office_location"),
        ("Do you offer support?", "support_offering")
    ]
    # vectorizer, model, label_encoder = train_intent_recognizer(data)
    # with open('../models/intent_recognizer.pkl', 'wb') as f:
    #     pickle.dump((vectorizer, model, label_encoder), f)

    result = recognize_intent(data)
    print(result)



