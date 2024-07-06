from flask import Flask, request, jsonify
from dialogue_manager import DialogueManager
from googletrans import Translator
from textblob import TextBlob

translator = Translator()
app = Flask(__name__)
manager = DialogueManager()
user_preferences = {}

def update_user_preferences(user_id, key, value):
    if user_id not in user_preferences:
        user_preferences[user_id] = {}
    user_preferences[user_id][key] = value

def get_user_preferences(user_id):
    return user_preferences.get(user_id, {})

def translate_message(user_message, target_lang='en'):
    translation = translator.translate(user_message, dest=target_lang)
    return translation.text

@app.route('/lingual_chat', methods=['POST'])
def mutli_lingual_chat():
    user_message = request.json.get('message')
    translated_message = translate_message(user_message, target_lang='en')
    intent, entities = recognize_intent(translated_message)
    response = handle_intent(intent, entities)
    return jsonify({'response': response})

@app.route('/sentiment_chat', methods=['POST'])
def sentiment_chat():
    user_message = request.json.get('message')
    translated_message = translate_message(user_message, target_lang='en')
    intent, entities = recognize_intent(translated_message)
    sentiment_polarity, sentiment_subjectivity = analyze_sentiment(translated_message)
    response = handle_intent(intent, entities)
    return jsonify({'response': response, 'sentiment_polarity': sentiment_polarity, 'sentiment_subjectivity': sentiment_subjectivity})


@app.route('/chat', methods=['POST'])
def chat():
    user_id = request.json.get('user_id')
    user_message = request.json.get('message')
    translated_message = translate_message(user_message, target_lang='en')
    intent, entities = recognize_intent(translated_message)
    sentiment_polarity, sentiment_subjectivity = analyze_sentiment(translated_message)
    response = handle_intent(intent, entities)
    update_user_preferences(user_id, 'last_message', user_message)
    return jsonify({'response': response, 'sentiment_polarity': sentiment_polarity, 'sentiment_subjectivity': sentiment_subjectivity, 'user_preferences': get_user_preferences(user_id)})

user_id = "user123"
user_message = "I love sunny weather!"
update_user_preferences(user_id, 'favorite_weather', 'sunny')
print(get_user_preferences(user_id))
