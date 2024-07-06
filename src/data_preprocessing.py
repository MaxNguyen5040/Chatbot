from sklearn.preprocessing import LabelEncoder
import numpy as np

def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in string.punctuation]
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return tokens

def preprocess_data(data):
    questions, intents = zip(*data)
    processed_questions = [" ".join(preprocess_text(question)) for question in questions]
    label_encoder = LabelEncoder()
    encoded_intents = label_encoder.fit_transform(intents)
    return processed_questions, encoded_intents, label_encoder

if __name__ == "__main__":
    data = [
        ("What are your operating hours?", "operating_hours"),
        ("How can I reset my password?", "reset_password")
    ]
    processed_questions, encoded_intents, label_encoder = preprocess_data(data)
    print(processed_questions)
    print(encoded_intents)
