from flask import Flask, render_template, request, jsonify
import yfinance as yf
app = Flask(__name__)
def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period="1d")
        if history.empty:
            return None
        price = history["Close"].iloc[-1]
        return round(price, 2)
    except Exception as e:
        return None
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/get_price', methods=['POST'])
def get_price():
    data = request.get_json()
    if not data or "symbol" not in data:
        return jsonify({"error": "Stock symbol required"}), 400
    symbol = data["symbol"].upper()
    price = get_stock_price(symbol)
    if price is None:
        return jsonify({"error": "Invalid stock symbol or no data available"}), 400
    return jsonify({"symbol": symbol, "price": price})
if __name__ == '__main__':
    app.run(debug=True)
