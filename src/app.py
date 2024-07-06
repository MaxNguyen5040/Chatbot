from flask import Flask, request, jsonify
from dialogue_manager import DialogueManager
from googletrans import Translator
from textblob import TextBlob

translator = Translator()


app = Flask(__name__)
manager = DialogueManager()

def translate_message(user_message, target_lang='en'):
    translation = translator.translate(user_message, dest=target_lang)
    return translation.text

@app.route('/chat', methods=['POST'])
def mutli_lingual_chat():
    user_message = request.json.get('message')
    translated_message = translate_message(user_message, target_lang='en')
    intent, entities = recognize_intent(translated_message)
    response = handle_intent(intent, entities)
    return jsonify({'response': response})

def sentiment_chat():
    user_message = request.json.get('message')
    translated_message = translate_message(user_message, target_lang='en')
    intent, entities = recognize_intent(translated_message)
    sentiment_polarity, sentiment_subjectivity = analyze_sentiment(translated_message)
    response = handle_intent(intent, entities)
    return jsonify({'response': response, 'sentiment_polarity': sentiment_polarity, 'sentiment_subjectivity': sentiment_subjectivity})

user_message = "¿Cómo está el clima hoy?"
translated_message = translate_message(user_message, target_lang='en')
print(translated_message)

user_message = "I am very happy today!"
polarity, subjectivity = analyze_sentiment(user_message)
print(f"Polarity: {polarity}, Subjectivity: {subjectivity}")