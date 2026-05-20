"""AI Sentiment Analysis Module"""
import numpy as np
import pandas as pd
from stock_fetcher import StockFetcher
from textblob import TextBlob
import warnings
warnings.filterwarnings('ignore')

class SentimentAnalyzer:
    """Analyzes sentiment and market mood"""
    
    def __init__(self):
        self.fetcher = StockFetcher()
    
    def calculate_technical_sentiment(self, ticker: str) -> dict:
        \"\"\"Calculate sentiment from price action\"\"\"\n        try:
            hist = self.fetcher.get_historical_data(ticker, period='3mo')
            
            if hist is None or len(hist) < 20:
                return {'error': 'Not enough data'}
            
            prices = hist['Close'].values
            returns = np.diff(prices) / prices[:-1]
            
            # Metrics
            avg_return = np.mean(returns) * 100
            volatility = np.std(returns) * 100
            positive_days = np.sum(returns > 0)
            total_days = len(returns)
            win_rate = (positive_days / total_days) * 100
            
            # Sentiment scoring
            if avg_return > 0.5:
                sentiment = "VERY BULLISH 🚀"
                score = 80 + min(avg_return * 5, 15)
            elif avg_return > 0.1:
                sentiment = "BULLISH 📈"
                score = 60 + (avg_return * 10)
            elif avg_return > -0.1:
                sentiment = "NEUTRAL 😐"
                score = 50
            elif avg_return > -0.5:
                sentiment = "BEARISH 📉"
                score = 40 - (abs(avg_return) * 10)
            else:
                sentiment = "VERY BEARISH 🔴"
                score = max(20 - abs(avg_return) * 5, 5)
            
            return {
                'ticker': ticker.upper(),
                'sentiment': sentiment,
                'sentiment_score': round(min(score, 100), 1),
                'avg_daily_return': round(avg_return, 2),
                'volatility': round(volatility, 2),
                'win_rate': round(win_rate, 1),
                'positive_days': int(positive_days),
                'total_days': int(total_days)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def calculate_news_sentiment(self, text: str) -> float:
        \"\"\"Analyze sentiment from news text (using TextBlob)\"\"\"\n        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            sentiment_score = (polarity + 1) * 50  # Convert to 0-100
            return round(sentiment_score, 1)
        except:
            return 50  # Neutral if error
    
    def composite_sentiment(self, ticker: str, news_text: str = None) -> dict:
        \"\"\"Combine technical + news sentiment\"\"\"\n        technical = self.calculate_technical_sentiment(ticker)
        
        if 'error' in technical:
            return technical
        
        tech_score = technical['sentiment_score']
        
        # If news provided, analyze it
        news_score = 50
        if news_text:
            news_score = self.calculate_news_sentiment(news_text)
        
        # Composite score (70% technical, 30% news)
        composite = (tech_score * 0.7) + (news_score * 0.3)
        
        # Overall sentiment
        if composite > 70:
            overall = "STRONG BUY 🟢"
        elif composite > 55:
            overall = "BUY 📈"
        elif composite < 30:
            overall = "STRONG SELL 🔴"
        elif composite < 45:
            overall = "SELL 📉"
        else:
            overall = "HOLD 😐"
        
        return {
            'ticker': ticker.upper(),
            'technical_sentiment': technical['sentiment'],
            'technical_score': tech_score,
            'news_score': news_score if news_text else None,
            'composite_score': round(composite, 1),
            'overall_recommendation': overall
        }
    
    def sentiment_comparison(self, tickers: list) -> dict:
        \"\"\"Compare sentiment across multiple stocks\"\"\"\n        comparison = {}
        for ticker in tickers:
            sentiment = self.calculate_technical_sentiment(ticker)
            if 'error' not in sentiment:
                comparison[ticker.upper()] = {
                    'sentiment': sentiment['sentiment'],
                    'score': sentiment['sentiment_score']
                }
        
        # Sort by score
        sorted_comp = dict(sorted(comparison.items(), key=lambda x: x[1]['score'], reverse=True))
        return sorted_comp
