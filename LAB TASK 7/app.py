from flask import Flask, jsonify, render_template, request
import requests
app = Flask(__name__)
API_KEY = "S628GKBNREDKJG1C"
BASE_URL = "https://www.alphavantage.co/query"
def get_stock_price(symbol):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "1min",
        "apikey": API_KEY
    }
    data = requests.get(BASE_URL, params=params).json()
    return float(data["Time Series (1min)"][next(reversed(data["Time Series (1min)"]))]["4. close"])
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/get_price', methods=['POST'])
def price():
    symbol = request.get_json()["symbol"].upper()
    try:
        return jsonify({"symbol": symbol, "price": round(get_stock_price(symbol), 2)})
    except:
        return jsonify({"error": "Invalid symbol or no data"}), 400
if __name__ == '__main__':
    app.run(debug=True)
