from flask import Flask, jsonify, request
import yfinance as yf
app = Flask(__name__)
def get_stock_price(symbol):
    try:
        return round(yf.Ticker(symbol).history(period="1d")["Close"].iloc[-1], 2)
    except Exception as e:
        return f"Error fetching stock price: {e}"
@app.route('/get_price', methods=['POST'])
def get_price():
    symbol = request.json.get("symbol", "").upper()
    if not symbol:
        return jsonify({"error": "Stock symbol required"}), 400
    price = get_stock_price(symbol)
    if isinstance(price, str):
        return jsonify({"error": price}), 400
    return jsonify({"symbol": symbol, "price": price})
if __name__ == '__main__':
    app.run(debug=True)