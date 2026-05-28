"""AI Trading Recommender - Smart Buy/Sell/Hold Recommendations"""
import numpy as np
import pandas as pd
from stock_fetcher import StockFetcher
from price_predictor import PricePredictor
from sentiment_analyzer import SentimentAnalyzer

class TradingRecommender:
    """Provides AI-powered trading recommendations"""
    
    def __init__(self):
        self.fetcher = StockFetcher()
        self.predictor = PricePredictor()
        self.sentiment = SentimentAnalyzer()
    
    def get_technical_indicators(self, ticker: str) -> dict:
        \"\"\"Calculate technical indicators\"\"\"
        try:
            hist = self.fetcher.get_historical_data(ticker, period='3mo')
            if hist is None or len(hist) < 20:
                return {}
            
            prices = hist['Close'].values
            
            # RSI (Relative Strength Index)
            rsi = self._calculate_rsi(prices)
            
            # MACD
            macd_line, signal_line, histogram = self._calculate_macd(prices)
            
            # Bollinger Bands
            sma20 = np.mean(prices[-20:])
            std20 = np.std(prices[-20:])
            upper_band = sma20 + (std20 * 2)
            lower_band = sma20 - (std20 * 2)
            current = prices[-1]
            
            return {
                'rsi': round(rsi, 2),
                'macd_line': round(macd_line, 2),
                'signal_line': round(signal_line, 2),
                'histogram': round(histogram, 2),
                'upper_band': round(upper_band, 2),
                'lower_band': round(lower_band, 2),
                'current_price': round(current, 2),
                'sma_20': round(sma20, 2)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_rsi(self, prices: np.ndarray, period: int = 14) -> float:
        \"\"\"Calculate Relative Strength Index\"\"\"
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        rs = up / down if down != 0 else 0
        rsi = 100 - 100 / (1 + rs)
        
        for d in deltas[period+1:]:
            if d >= 0:
                up = (up * (period - 1) + d) / period
                down = (down * (period - 1)) / period
            else:
                up = (up * (period - 1)) / period
                down = (down * (period - 1) - d) / period
            rs = up / down if down != 0 else 0
            rsi = 100 - 100 / (1 + rs)
        
        return rsi
    
    def _calculate_macd(self, prices: np.ndarray):
        \"\"\"Calculate MACD\"\"\"
        exp1 = self._exponential_moving_average(prices, 12)
        exp2 = self._exponential_moving_average(prices, 26)
        macd_line = exp1 - exp2
        signal_line = self._exponential_moving_average(
            np.array([macd_line] * len(prices)), 9
        )
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    def _exponential_moving_average(self, data: np.ndarray, period: int) -> float:
        \"\"\"Calculate EMA\"\"\"
        return data[-period:].mean()
    
    def get_recommendation(self, ticker: str) -> dict:
        \"\"\"Get comprehensive trading recommendation\"\"\"
        try:
            # Get current price
            price_data = self.fetcher.get_stock_price(ticker)
            if not price_data:
                return {'error': f'Could not fetch data for {ticker}'}
            
            current_price = price_data['current_price']
            
            # Get predictions
            prediction = self.predictor.predict_next_day(ticker)
            
            # Get sentiment
            sentiment_data = self.sentiment.predict_sentiment_score(ticker)
            
            # Get technical indicators
            technicals = self.get_technical_indicators(ticker)
            
            # Calculate composite recommendation score
            score = 0
            reasons = []
            
            # Price prediction (40% weight)
            if prediction.get('predicted_change', 0) > 0:
                score += 40
                reasons.append(f\"✅ Price predicted to rise ({prediction.get('predicted_change_percent')}%)\")\n            else:
                score -= 40
                reasons.append(f\"⚠️ Price predicted to fall ({prediction.get('predicted_change_percent')}%)\")\n            
            # Sentiment (30% weight)
            sentiment_score = sentiment_data.get('composite_score', 0)
            if sentiment_score > 0:
                score += sentiment_score / 2  # Normalize\n                reasons.append(f\"✅ Positive sentiment ({sentiment_score:.1f})\")\n            else:
                score += sentiment_score / 2
                reasons.append(f\"⚠️ Negative sentiment ({sentiment_score:.1f})\")\n            
            # Technical indicators (30% weight)
            rsi = technicals.get('rsi', 50)
            if 30 < rsi < 70:
                score += 15
                reasons.append(f\"✅ RSI in neutral zone ({rsi:.1f})\")\n            elif rsi <= 30:
                score += 20
                reasons.append(f\"✅ RSI oversold - potential buy ({rsi:.1f})\")\n            else:
                score -= 20
                reasons.append(f\"⚠️ RSI overbought - potential sell ({rsi:.1f})\")\n            
            # Generate recommendation
            if score >= 50:
                recommendation = \"🟢 STRONG BUY\"\n                signal = \"HIGH\"\n            elif score >= 20:
                recommendation = \"🟡 BUY\"\n                signal = \"MEDIUM\"\n            elif score >= -20:
                recommendation = \"⚪ HOLD\"\n                signal = \"NEUTRAL\"\n            elif score >= -50:
                recommendation = \"🟠 SELL\"\n                signal = \"MEDIUM\"\n            else:
                recommendation = \"🔴 STRONG SELL\"\n                signal = \"HIGH\"\n            
            return {
                'ticker': ticker.upper(),
                'current_price': current_price,
                'recommendation': recommendation,
                'signal_strength': signal,
                'confidence_score': round(abs(score), 1),
                'predicted_price': prediction.get('predicted_price'),
                'predicted_change': prediction.get('predicted_change'),
                'rsi': technicals.get('rsi'),
                'sentiment': sentiment_data.get('overall_sentiment'),
                'reasons': reasons
            }
        except Exception as e:
            return {'error': str(e)}
    
    def compare_recommendations(self, tickers: list) -> dict:
        \"\"\"Compare recommendations for multiple stocks\"\"\"
        recommendations = {}\n        for ticker in tickers:
            rec = self.get_recommendation(ticker)
            if 'error' not in rec:
                recommendations[ticker.upper()] = rec
        return recommendations
    
    def portfolio_recommendation(self, portfolio: dict) -> dict:
        \"\"\"Analyze and recommend portfolio adjustments\"\"\"
        # portfolio format: {'AAPL': 100, 'MSFT': 50} (shares)\n        try:
            total_value = 0
            holdings = {}
            
            for ticker, shares in portfolio.items():
                price_data = self.fetcher.get_stock_price(ticker)
                if price_data:
                    value = price_data['current_price'] * shares
                    total_value += value
                    holdings[ticker.upper()] = {
                        'shares': shares,
                        'current_price': price_data['current_price'],
                        'value': value
                    }
            
            # Get allocations
            allocations = {}
            for ticker, data in holdings.items():
                allocations[ticker] = round(data['value'] / total_value * 100, 1)
            
            # Get recommendations
            recommendations = self.compare_recommendations(list(portfolio.keys()))
            
            return {
                'total_portfolio_value': round(total_value, 2),
                'allocations': allocations,
                'recommendations': recommendations,
                'rebalance_suggestions': self._suggest_rebalancing(allocations, recommendations)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _suggest_rebalancing(self, allocations: dict, recommendations: dict) -> list:
        \"\"\"Suggest portfolio rebalancing\"\"\"
        suggestions = []
        
        for ticker, allocation in allocations.items():
            rec = recommendations.get(ticker.upper(), {})
            recommendation = rec.get('recommendation', '')
            
            if 'BUY' in recommendation and allocation < 25:
                suggestions.append(f\"Increase {ticker} allocation (Currently {allocation}%)\")\n            elif 'SELL' in recommendation and allocation > 5:
                suggestions.append(f\"Decrease {ticker} allocation (Currently {allocation}%)\")\n        
        return suggestions if suggestions else [\"✅ Portfolio is well-balanced\"]\n
