from flask import Flask, render_template, request, jsonify, send_from_directory
import os
app = Flask(__name__)
STATIC_FOLDER = 'static'
app.config['STATIC_FOLDER'] = STATIC_FOLDER
CHATBOT_RESPONSES = {
    "hi": "Hello! How can I help you with cyber safety?",
    "how are you": "I am fine and what about you",
    "can you help me": "I can help you with cyber safety tips, password management, and online security",
    "what is cyber safety": "Cyber safety is the practice of protecting yourself and your devices",
    "what is phishing": "Phishing is a scam where attackers trick you into giving up personal information via fake emails or messages.",
    "how to stay safe online": "Use strong passwords, enable two-factor authentication, and never share personal details online.",
    "bye": "Goodbye! Stay safe online."
}
DEFAULT_RESPONSE = "I'm not sure about that. But I can help with online safety tips!"
def chatbot_response(user_input):
    return CHATBOT_RESPONSES.get(user_input.lower(), DEFAULT_RESPONSE)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/get", methods=["POST"])
def get_bot_response():
    user_text = request.json.get("message")
    response = chatbot_response(user_text)
    return jsonify({"response": response})
if __name__ == "__main__":
    app.run(debug=True)
