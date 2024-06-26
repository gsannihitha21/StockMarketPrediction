from flask import Flask, request, jsonify
import yfinance as yf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    try:
        data = request.get_json()
        ticker = data['ticker']
        period = data.get('period', '1d')  # Default to '1d' if not provided
        interval = data.get('interval', '1h')  # Default to '1h' if not provided

        stock_data = yf.download(ticker, period=period, interval=interval)

        if stock_data.empty:
            return jsonify({'error': 'No data found for the given ticker'}), 404

        stock_data.reset_index(inplace=True)
        stock_data.rename(columns={'Datetime': 'Date'}, inplace=True)
        stock_data = stock_data.to_dict(orient='records')
        return jsonify(stock_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
