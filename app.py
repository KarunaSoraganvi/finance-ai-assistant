"""Flask REST API for Stock AI Assistant"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from ai_assistant import StockAIAssistant
import logging

load_dotenv()

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize AI Assistant
try:
    ai_assistant = StockAIAssistant()
except ValueError as e:
    logger.error(f"Failed to initialize AI Assistant: {str(e)}")
    ai_assistant = None

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Stock AI Assistant"})

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint - send message and get AI response"""
    if not ai_assistant:
        return jsonify({"error": "AI Assistant not initialized"}), 500
    
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' field"}), 400
    
    try:
        user_message = data['message']
        response = ai_assistant.chat(user_message)
        return jsonify({
            "user_message": user_message,
            "assistant_response": response
        })
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/stock/<ticker>', methods=['GET'])
def get_stock(ticker):
    """Get current stock price"""
    if not ai_assistant:
        return jsonify({"error": "AI Assistant not initialized"}), 500
    
    try:
        stock_data = ai_assistant.stock_fetcher.get_stock_price(ticker)
        if stock_data:
            return jsonify(stock_data)
        else:
            return jsonify({"error": f"Stock {ticker} not found"}), 404
    except Exception as e:
        logger.error(f"Stock fetch error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/stocks', methods=['POST'])
def get_multiple_stocks():
    """Get prices for multiple stocks"""
    if not ai_assistant:
        return jsonify({"error": "AI Assistant not initialized"}), 500
    
    data = request.get_json()
    if not data or 'tickers' not in data:
        return jsonify({"error": "Missing 'tickers' field"}), 400
    
    try:
        stocks_data = ai_assistant.stock_fetcher.get_multiple_prices(data['tickers'])
        return jsonify(stocks_data)
    except Exception as e:
        logger.error(f"Multiple stocks fetch error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/compare', methods=['POST'])
def compare_stocks():
    """Compare multiple stocks"""
    if not ai_assistant:
        return jsonify({"error": "AI Assistant not initialized"}), 500
    
    data = request.get_json()
    if not data or 'tickers' not in data:
        return jsonify({"error": "Missing 'tickers' field"}), 400
    
    try:
        comparison = ai_assistant.stock_fetcher.compare_stocks(data['tickers'])
        return jsonify(comparison)
    except Exception as e:
        logger.error(f"Comparison error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/history', methods=['POST'])
def get_price_history():
    """Get historical price data"""
    if not ai_assistant:
        return jsonify({"error": "AI Assistant not initialized"}), 500
    
    data = request.get_json()
    if not data or 'ticker' not in data:
        return jsonify({"error": "Missing 'ticker' field"}), 400
    
    try:
        ticker = data['ticker']
        period = data.get('period', '1mo')
        hist_data = ai_assistant.stock_fetcher.get_historical_data(ticker, period)
        if hist_data is not None:
            return jsonify(hist_data.to_dict())
        else:
            return jsonify({"error": f"Historical data not found for {ticker}"}), 404
    except Exception as e:
        logger.error(f"History fetch error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset():
    """Reset conversation history"""
    if not ai_assistant:
        return jsonify({"error": "AI Assistant not initialized"}), 500
    
    ai_assistant.reset_conversation()
    return jsonify({"status": "Conversation history cleared"})

@app.route('/conversation', methods=['GET'])
def get_conversation():
    """Get current conversation history"""
    if not ai_assistant:
        return jsonify({"error": "AI Assistant not initialized"}), 500
    
    history = ai_assistant.get_conversation_history()
    return jsonify({"conversation": history})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
