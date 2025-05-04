from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pandas as pd
import os
import csv
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = '7654'
DATASET_PATH = r'C:\Users\WB\Desktop\New folder (4)\LAB TASK 13\Dataset_Banking_chatbot.csv'
USER_CSV_PATH = 'users.csv'
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
THRESHOLD = 0.7
bank = pd.read_csv(DATASET_PATH, encoding='cp1252')
embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
query_embeddings = embeddings.embed_documents(bank["Query"].tolist())
if not os.path.exists(USER_CSV_PATH):
    with open(USER_CSV_PATH, 'w', newline='') as f:
        csv.writer(f).writerow(['username', 'password'])
def get_response(query):
    user_embedding = embeddings.embed_query(query)
    similarities = cosine_similarity([user_embedding], query_embeddings)[0]
    idx = similarities.argmax()
    return bank.iloc[idx]["Response"] if similarities[idx] >= THRESHOLD else "Sorry, please ask a question related to finance."
def authenticate_user(username, password):
    with open(USER_CSV_PATH, 'r') as f:
        for row in csv.DictReader(f):
            if row['username'] == username and check_password_hash(row['password'], password):
                return True
    return False
def username_exists(username):
    with open(USER_CSV_PATH, 'r') as f:
        return any(row['username'] == username for row in csv.DictReader(f))
@app.route('/')
def main_page():
    session.clear()
    return render_template('main.html')
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('main_page'))
    return render_template('index.html', conversation=[], username=session['username'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if authenticate_user(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        return render_template('login.html', error_message="Account not found. Would you like to create a new account?")
    return render_template('login.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username_exists(username):
            return "Username already exists!", 409
        with open(USER_CSV_PATH, 'a', newline='') as f:
            csv.writer(f).writerow([username, generate_password_hash(password)])
        return redirect(url_for('login'))
    return render_template('signup.html')
@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.get_json()['query']
    return jsonify({'response': get_response(user_input)})
if __name__ == '__main__':
    app.run(debug=True)
