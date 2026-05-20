"""AI Price Prediction Module using Machine Learning"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from stock_fetcher import StockFetcher
import warnings
warnings.filterwarnings('ignore')

class PricePredictor:
    """Predicts stock prices using ML"""
    
    def __init__(self):
        self.fetcher = StockFetcher()
        self.scaler = MinMaxScaler()
    
    def predict_next_day(self, ticker: str) -> dict:
        """Predict next day's price"""
        try:
            # Get historical data
            hist = self.fetcher.get_historical_data(ticker, period='3mo')
            
            if hist is None or len(hist) < 20:
                return {'error': 'Not enough historical data'}
            
            # Prepare data
            prices = hist['Close'].values.reshape(-1, 1)
            scaled_prices = self.scaler.fit_transform(prices)
            
            # Create sequences
            X = np.arange(len(scaled_prices)).reshape(-1, 1)
            y = scaled_prices.flatten()
            
            # Train model
            model = LinearRegression()
            model.fit(X, y)
            
            # Predict next day
            next_day = len(scaled_prices)
            predicted_scaled = model.predict([[next_day]])[0]
            predicted_price = self.scaler.inverse_transform([[predicted_scaled]])[0][0]
            
            current_price = prices[-1][0]
            change = predicted_price - current_price
            change_percent = (change / current_price * 100)
            
            # Direction prediction
            if change > 0:
                direction = "📈 UP"
                confidence = min(abs(change_percent) / 5 * 100, 95)  # Cap at 95%
            else:
                direction = "📉 DOWN"
                confidence = min(abs(change_percent) / 5 * 100, 95)
            
            return {
                'ticker': ticker.upper(),
                'current_price': round(current_price, 2),
                'predicted_price': round(predicted_price, 2),
                'predicted_change': round(change, 2),
                'predicted_change_percent': round(change_percent, 2),
                'direction': direction,
                'confidence': round(confidence, 1),
                'recommendation': 'BUY' if change > 0 else 'SELL'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def predict_week(self, ticker: str) -> dict:
        """Predict week's trend"""
        try:
            hist = self.fetcher.get_historical_data(ticker, period='6mo')
            
            if hist is None or len(hist) < 50:
                return {'error': 'Not enough data'}
            
            prices = hist['Close'].values
            current_price = prices[-1]
            
            # Simple momentum calculation
            momentum = prices[-1] - prices[-5]  # Last 5 days trend
            sma_short = np.mean(prices[-5:])
            sma_long = np.mean(prices[-20:])
            
            trend_strength = abs(sma_short - sma_long) / current_price * 100
            direction = "📈 UP" if sma_short > sma_long else "📉 DOWN"
            
            predicted_change = momentum * 1.5  # Extrapolate
            predicted_price = current_price + predicted_change
            
            return {
                'ticker': ticker.upper(),
                'current_price': round(current_price, 2),
                'predicted_price': round(predicted_price, 2),
                'predicted_change': round(predicted_change, 2),
                'predicted_change_percent': round(predicted_change / current_price * 100, 2),
                'direction': direction,
                'trend_strength': round(trend_strength, 1),
                'recommendation': 'BUY' if predicted_price > current_price else 'SELL'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def predict_multiple(self, tickers: list) -> dict:
        """Predict prices for multiple stocks"""
        predictions = {}
        for ticker in tickers:
            pred = self.predict_next_day(ticker)
            if 'error' not in pred:
                predictions[ticker.upper()] = pred
        return predictions
