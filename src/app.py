from flask import Flask, request, jsonify
from dialogue_manager import DialogueManager
from googletrans import Translator
from textblob import TextBlob
from transformers import pipeline
from dash import bootstrap_components

translator = Translator()
app = Flask(__name__)
manager = DialogueManager()
user_preferences = {}
nlp = pipeline("question-answering")
knowledge_base = {
    "what is your name": "I am your friendly chatbot!",
    "how can you help me": "I can assist you with weather updates, booking flights, and much more."
}

app.layout = html.Div([
    dcc.Input(id='input-box', type='text', value=''),
    html.Button('Submit', id='button'),
    html.Div(id='output-container-button', children='Enter a value and press submit'),

    dbc.Button("Click me", color="primary", className="mr-1"),
    dbc.Carousel(
        items=[
            {"key": "1", "src": "/assets/image1.jpg", "header": "Header 1", "caption": "Caption 1"},
            {"key": "2", "src": "/assets/image2.jpg", "header": "Header 2", "caption": "Caption 2"},
            {"key": "3", "src": "/assets/image3.jpg", "header": "Header 3", "caption": "Caption 3"},
        ],
        controls=True,
        indicators=True,
        interval=2000,
        ride="carousel"
    )
])

@app.callback(
    Output('output-container-button', 'children'),
    [Input('button', 'n_clicks')],
    [State('input-box', 'value')]
)
def update_output(n_clicks, value):
    if n_clicks is not None:
        return f'The input value was "{value}" and the button has been clicked {n_clicks} times.'


def query_knowledge_base(user_message):
    question = user_message.lower()
    return knowledge_base.get(question, "I'm not sure about that. Can you please rephrase?")


def advanced_intent_recognition(user_message):
    qa_input = {
        'question': user_message,
        'context': "Provide some context about your chatbot here."
    }
    result = nlp(qa_input)
    return result['answer']


@app.route('/chat', methods=['POST'])
def chat():
    user_id = request.json.get('user_id')
    user_message = request.json.get('message')
    translated_message = translate_message(user_message, target_lang='en')
    knowledge_base_response = query_knowledge_base(translated_message)
    intent, entities = recognize_intent(translated_message)
    advanced_intent = advanced_intent_recognition(translated_message)
    sentiment_polarity, sentiment_subjectivity = analyze_sentiment(translated_message)
    response = handle_intent(intent, entities)
    update_user_preferences(user_id, 'last_message', user_message)
    return jsonify({'response': response, 'knowledge_base_response': knowledge_base_response, 'advanced_intent': advanced_intent, 'sentiment_polarity': sentiment_polarity, 'sentiment_subjectivity': sentiment_subjectivity, 'user_preferences': get_user_preferences(user_id)})

user_message = "What is the weather like in Paris?"
advanced_intent = advanced_intent_recognition(user_message)
print(advanced_intent)

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
