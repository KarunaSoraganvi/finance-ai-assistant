# 💰 Stock AI Assistant

An intelligent AI-powered stock price assistant that fetches real-time data from Yahoo Finance and provides insights using OpenAI's GPT-4 model.

## 🌟 Features

- **Real-time Stock Prices**: Fetch current prices from Yahoo Finance
- **AI-Powered Analysis**: Ask natural language questions about stocks
- **Multi-Stock Comparison**: Compare prices and performance across stocks
- **Historical Data**: View price trends and changes over time
- **REST API**: Easy-to-use API endpoints for integration
- **Interactive CLI**: Command-line interface for direct interaction
- **Conversation Memory**: Maintains context across multiple queries

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/KarunaSoraganvi/AI-Stock-Assitant-with-Yahoo-Finance.git
   cd AI-Stock-Assitant-with-Yahoo-Finance
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

## 🚀 Usage

### CLI Mode (Interactive Chat)

```bash
python cli.py
```

Example interactions:
```
You: What is the current price of Apple stock?
Assistant: Apple (AAPL) is currently trading at $178.50...

You: Compare AAPL and MSFT
Assistant: Here's a comparison of Apple and Microsoft:
   - AAPL: $178.50 (+2.5%)
   - MSFT: $340.20 (+1.8%)

You: Show me the 90-day price change for Tesla
Assistant: Tesla (TSLA) over the last 90 days:
   - Start: $245.30
   - Current: $285.75
   - Change: +$40.45 (+16.5%)
```

### API Server Mode

```bash
python app.py
```
Server runs on `http://localhost:5000`

### API Endpoints

#### 1. Chat with AI
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Apple stock price?"}'
```

**Response:**
```json
{
  "user_message": "What is Apple stock price?",
  "assistant_response": "Apple (AAPL) is currently trading at $178.50 with a change of +$4.25 (+2.44%) from the previous close..."
}
```

#### 2. Get Single Stock Price
```bash
curl http://localhost:5000/stock/AAPL
```

**Response:**
```json
{
  "ticker": "AAPL",
  "name": "Apple Inc.",
  "current_price": 178.50,
  "previous_close": 174.25,
  "change": 4.25,
  "change_percent": 2.44,
  "currency": "USD",
  "timestamp": "2024-01-15T14:30:00Z"
}
```

#### 3. Get Multiple Stock Prices
```bash
curl -X POST http://localhost:5000/stocks \
  -H "Content-Type: application/json" \
  -d '{"tickers": ["AAPL", "MSFT", "GOOGL"]}'
```

#### 4. Compare Stocks
```bash
curl -X POST http://localhost:5000/compare \
  -H "Content-Type: application/json" \
  -d '{"tickers": ["AAPL", "MSFT"]}'
```

#### 5. Get Historical Data
```bash
curl -X POST http://localhost:5000/history \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "period": "1mo"}'
```

Valid periods: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `max`

#### 6. Reset Conversation
```bash
curl -X POST http://localhost:5000/reset
```

#### 7. Get Conversation History
```bash
curl http://localhost:5000/conversation
```

#### 8. Health Check
```bash
curl http://localhost:5000/health
```

## 📚 Module Documentation

### StockFetcher (`stock_fetcher.py`)
Handles all Yahoo Finance data fetching:
- `get_stock_price(ticker)` - Current price and info
- `get_multiple_prices(tickers)` - Batch price fetching
- `get_historical_data(ticker, period)` - Historical trends
- `get_price_change(ticker, days)` - Change over time
- `compare_stocks(tickers)` - Performance comparison

### StockAIAssistant (`ai_assistant.py`)
AI-powered assistant with GPT-4:
- Natural language understanding
- Automatic tool calling
- Conversation memory management
- Integration with StockFetcher

### Flask App (`app.py`)
REST API server with 8 endpoints

### CLI (`cli.py`)
Interactive command-line interface

## 🔧 Configuration

Edit `.env` file to configure:

```env
# Required: OpenAI API Key
OPENAI_API_KEY=sk-...

# Optional: Flask settings
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000
```

## 🐛 Troubleshooting

### "OpenAI API key not found"
- Create `.env` file from `.env.example`
- Add your OpenAI API key
- Ensure the key is valid and has sufficient credits

### "Stock ticker not found"
- Verify the ticker symbol is correct
- Use uppercase letters (e.g., `AAPL` not `aapl`)
- Check if the ticker is listed on Yahoo Finance

### "Connection error"
- Check your internet connection
- Verify Yahoo Finance is accessible
- Check OpenAI API connectivity

## 📦 Dependencies

- **openai**: GPT-4 API client
- **yfinance**: Yahoo Finance data fetcher
- **pandas**: Data manipulation
- **flask**: REST API framework
- **flask-cors**: Cross-origin support
- **python-dotenv**: Environment variable management

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- [OpenAI](https://openai.com) for GPT-4
- [yfinance](https://github.com/ranaroussi/yfinance) for Yahoo Finance data
- [Flask](https://flask.palletsprojects.com) for the web framework

## 📧 Support

For issues and questions:
1. Check the troubleshooting section
2. Review existing issues on GitHub
3. Create a new issue with details

## 🚀 Future Enhancements

- [ ] Real-time price alerts
- [ ] Portfolio tracking
- [ ] Technical indicators (RSI, MACD, etc.)
- [ ] Sentiment analysis
- [ ] News integration
- [ ] Mobile app
- [ ] Database for storing queries
- [ ] Advanced charting
