from flask import Flask, request, jsonify
from dialogue_manager import DialogueManager

app = Flask(__name__)
manager = DialogueManager()

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    intent = manager.recognize_intent(user_input)
    response = manager.handle_intent(intent)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)