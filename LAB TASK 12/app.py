from flask import Flask, render_template, request, jsonify
from transformers import pipeline


app = Flask(__name__)


chatbot = pipeline('text-generation', model='gpt2')


@app.route("/")
def home():
    return render_template("index.html")


def get_gpt2_response(user_input):
    try:
        response = chatbot(user_input, max_length=150, num_return_sequences=1)
        return response[0]['generated_text'].strip()
    except Exception as e:
        return f"Error: {str(e)}"
    

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_text = request.json.get("message")
    response = get_gpt2_response(user_text)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
