from flask import Flask, render_template, request, jsonify
import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Config
DATASET_PATH = r'C:\Users\WB\Desktop\PAI LAB PROJECT\Dataset_Banking_chatbot.csv'
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
THRESHOLD = 0.7

# Load data and model
bank = pd.read_csv(DATASET_PATH, encoding='cp1252')
embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
query_embeddings = embeddings.embed_documents(bank["Query"].tolist())

# Generate response
def get_response(query):
    user_embedding = embeddings.embed_query(query)
    similarities = cosine_similarity([user_embedding], query_embeddings)[0]
    best_match_index = similarities.argmax()
    
    return bank.iloc[best_match_index]["Response"] if similarities[best_match_index] >= THRESHOLD else "Sorry, please ask a question related to finance."

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    conversation = []
    if request.method == 'POST':
        user_input = request.form['query']
        bot_response = get_response(user_input)
        conversation = [('User', user_input), ('Bot', bot_response)]
    return render_template('index.html', conversation=conversation)

@app.route('/ask', methods=['POST'])
def ask():
    return jsonify({'response': get_response(request.get_json()['query'])})

if __name__ == '__main__':
    app.run(debug=True)