"""Yahoo Finance Stock Price Fetcher Module"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockFetcher:
    """Fetches stock data from Yahoo Finance"""
    
    def __init__(self):
        self.cache = {}
        self.cache_expiry = {}
        self.cache_duration = 300  # 5 minutes
    
    def get_stock_price(self, ticker: str) -> Optional[Dict]:
        """Get current price for a single stock"""
        try:
            stock = yf.Ticker(ticker.upper())
            hist = stock.history(period='1d')
            
            if hist.empty:
                return None
            
            info = stock.info
            current_price = hist['Close'].iloc[-1]
            previous_close = info.get('previousClose', current_price)
            change = current_price - previous_close
            change_percent = (change / previous_close * 100) if previous_close else 0
            
            return {
                'ticker': ticker.upper(),
                'name': info.get('longName', 'N/A'),
                'current_price': round(current_price, 2),
                'previous_close': round(previous_close, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'currency': info.get('currency', 'USD'),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching {ticker}: {str(e)}")
            return None
    
    def get_multiple_prices(self, tickers: List[str]) -> Dict[str, Dict]:
        """Get prices for multiple stocks"""
        results = {}
        for ticker in tickers:
            price_data = self.get_stock_price(ticker)
            if price_data:
                results[ticker.upper()] = price_data
        return results
    
    def get_historical_data(self, ticker: str, period: str = '1mo') -> Optional[pd.DataFrame]:
        """Get historical data for a stock"""
        try:
            stock = yf.Ticker(ticker.upper())
            hist = stock.history(period=period)
            return hist
        except Exception as e:
            logger.error(f"Error fetching historical data for {ticker}: {str(e)}")
            return None
    
    def get_price_change(self, ticker: str, days: int = 30) -> Optional[Dict]:
        """Get price change over specified days"""
        try:
            stock = yf.Ticker(ticker.upper())
            period_days = f"{days}d"
            hist = stock.history(period=period_days)
            
            if hist.empty or len(hist) < 2:
                return None
            
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            change = end_price - start_price
            change_percent = (change / start_price * 100) if start_price else 0
            
            return {
                'ticker': ticker.upper(),
                'period_days': days,
                'start_price': round(start_price, 2),
                'end_price': round(end_price, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'highest': round(hist['High'].max(), 2),
                'lowest': round(hist['Low'].min(), 2)
            }
        except Exception as e:
            logger.error(f"Error calculating price change for {ticker}: {str(e)}")
            return None
    
    def compare_stocks(self, tickers: List[str]) -> Dict:
        """Compare multiple stocks"""
        comparison = {}
        for ticker in tickers:
            price_data = self.get_stock_price(ticker)
            if price_data:
                comparison[ticker.upper()] = {
                    'price': price_data['current_price'],
                    'change_percent': price_data['change_percent']
                }
        return comparison
