from flask import Flask, request, jsonify
from dialogue_manager import DialogueManager

app = Flask(__name__)
manager = DialogueManager()


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    intent, entities = recognize_intent(user_message)
    response = handle_intent(intent, entities)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)