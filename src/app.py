from flask import Flask, request, jsonify
from dialogue_manager import DialogueManager
from googletrans import Translator
from textblob import TextBlob
from transformers import pipeline
import dash_bootstrap_components as dbc
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

translator = Translator()
app = Flask(__name__)
manager = DialogueManager()
user_preferences = {}
nlp = pipeline("question-answering")
knowledge_base = {
    "what is your name": "I am your friendly chatbot!",
    "how can you help me": "I can assist you with weather updates, booking flights, and much more."
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

db.create_all()

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

def get_user_message(request):
    return request.json.get('message')

def translate_and_analyze(user_message):
    translated_message = translate_message(user_message, target_lang='en')
    intent, entities = recognize_intent(translated_message)
    advanced_intent = advanced_intent_recognition(translated_message)
    sentiment_polarity, sentiment_subjectivity = analyze_sentiment(translated_message)
    knowledge_base_response = query_knowledge_base(translated_message)
    return translated_message, intent, entities, advanced_intent, sentiment_polarity, sentiment_subjectivity, knowledge_base_response

def translate_message(user_message, target_lang='en'):
    try:
        translation = translator.translate(user_message, dest=target_lang)
        return translation.text
    except Exception as e:
        return f"Error translating message: {str(e)}"

def handle_intent(intent, entities):
    try:
        if intent == 'weather_query':
            location = next((entity['value'] for entity in entities if entity['entity'] == 'location'), None)
            if not location:
                raise ValueError("Location not provided")
            return get_weather(location)
        elif intent == 'flight_booking':
            destination = next((entity['value'] for entity in entities if entity['entity'] == 'location'), None)
            date = next((entity['value'] for entity in entities if entity['entity'] == 'date'), None)
            if not destination or not date:
                raise ValueError("Destination or date not provided")
            return f"Booking a flight to {destination} on {date}."
        else:
            return "I'm not sure how to help with that."
    except Exception as e:
        return f"Error handling intent: {str(e)}"

@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    return f"Number of interactions: {n}"

@app.route('/feedback', methods=['POST'])
def feedback():
    user_id = request.json.get('user_id')
    rating = request.json.get('rating')
    feedback_data.append({'user_id': user_id, 'rating': rating})
    return jsonify({'message': 'Feedback received, thank you!'})

def update_user_profile(user_id, profile_data):
    if user_id not in user_profiles:
        user_profiles[user_id] = {}
    user_profiles[user_id].update(profile_data)

def get_user_profile(user_id):
    return user_profiles.get(user_id, {})

@app.callback(
    Output('output-container-button', 'children'),
    [Input('button', 'n_clicks')],
    [State('input-box', 'value')]
)

@app.route('/profile/<username>')
def profile(username):
    user = user_data.get(username, {'name': 'Unknown', 'history': []})
    return render_template('profile.html', user=user)

def update_output(n_clicks, value):
    if n_clicks is not None:
        return f'The input value was "{value}" and the button has been clicked {n_clicks} times.'

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
