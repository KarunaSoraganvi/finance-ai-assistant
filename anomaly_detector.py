"""Anomaly Detection - Detect unusual stock price movements"""
import numpy as np
from stock_fetcher import StockFetcher

class AnomalyDetector:
    \"\"\"Detects anomalies and unusual price movements\"\"\"
    
    def __init__(self):
        self.fetcher = StockFetcher()
    
    def detect_price_spike(self, ticker: str, threshold: float = 2.0) -> dict:
        \"\"\"Detect unusual price spikes using statistical analysis\"\"\"
        try:
            hist = self.fetcher.get_historical_data(ticker, period='3mo')
            if hist is None or len(hist) < 20:
                return {'error': 'Not enough data'}
            
            prices = hist['Close'].values
            returns = np.diff(prices) / prices[:-1] * 100  # Daily returns %
            
            # Calculate mean and std
            mean_return = np.mean(returns)
            std_return = np.std(returns)
            
            # Get today's return
            today_return = returns[-1]
            
            # Z-score
            z_score = (today_return - mean_return) / std_return if std_return > 0 else 0
            
            # Detect anomaly
            is_anomaly = abs(z_score) > threshold
            
            if is_anomaly:
                if z_score > 0:
                    anomaly_type = \"📈 UNUSUAL SPIKE UP\"\n                    reason = f\"Price jumped {today_return:.2f}% (Z-score: {z_score:.2f})\"\n                else:
                    anomaly_type = \"📉 UNUSUAL SPIKE DOWN\"\n                    reason = f\"Price dropped {today_return:.2f}% (Z-score: {z_score:.2f})\"\n            else:
                anomaly_type = \"➡️ NORMAL MOVEMENT\"\n                reason = f\"Price movement within normal range ({today_return:.2f}%)\"\n            
            return {
                'ticker': ticker.upper(),
                'anomaly_detected': is_anomaly,
                'anomaly_type': anomaly_type,
                'daily_return': round(today_return, 2),
                'z_score': round(z_score, 2),
                'mean_return': round(mean_return, 2),
                'std_return': round(std_return, 2),
                'reason': reason,
                'alert_level': 'HIGH' if abs(z_score) > 3 else 'MEDIUM' if abs(z_score) > 2 else 'LOW'\n            }
        except Exception as e:
            return {'error': str(e)}
    
    def detect_trend_reversal(self, ticker: str) -> dict:
        \"\"\"Detect potential trend reversals\"\"\"
        try:
            hist = self.fetcher.get_historical_data(ticker, period='6mo')
            if hist is None or len(hist) < 50:
                return {'error': 'Not enough data'}
            
            prices = hist['Close'].values
            
            # Calculate short and long moving averages
            sma_5 = np.mean(prices[-5:])
            sma_20 = np.mean(prices[-20:])
            sma_50 = np.mean(prices[-50:])
            
            # Detect crossovers (potential reversals)
            if sma_5 > sma_20 > sma_50:
                trend = \"📈 UPTREND\"\n                reversal_risk = \"Low\"\n            elif sma_5 < sma_20 < sma_50:
                trend = \"📉 DOWNTREND\"\n                reversal_risk = \"Low\"\n            elif (sma_5 > sma_20 and sma_20 < sma_50) or (sma_5 < sma_20 and sma_20 > sma_50):
                trend = \"↩️ POTENTIAL REVERSAL\"\n                reversal_risk = \"HIGH\"\n            else:
                trend = \"➡️ MIXED\"\n                reversal_risk = \"Medium\"\n            
            return {
                'ticker': ticker.upper(),
                'current_trend': trend,
                'reversal_risk': reversal_risk,
                'sma_5': round(sma_5, 2),
                'sma_20': round(sma_20, 2),
                'sma_50': round(sma_50, 2),
                'current_price': round(prices[-1], 2)\n            }
        except Exception as e:
            return {'error': str(e)}
    
    def detect_volatility_surge(self, ticker: str) -> dict:
        \"\"\"Detect unusual volatility increases\"\"\"
        try:
            hist = self.fetcher.get_historical_data(ticker, period='3mo')
            if hist is None or len(hist) < 30:
                return {'error': 'Not enough data'}
            
            prices = hist['Close'].values
            returns = np.diff(prices) / prices[:-1] * 100
            
            # Recent volatility vs historical
            recent_vol = np.std(returns[-5:])
            historical_vol = np.std(returns[:-5])
            
            vol_ratio = recent_vol / historical_vol if historical_vol > 0 else 1
            
            if vol_ratio > 1.5:
                volatility_status = \"🔥 HIGH VOLATILITY SPIKE\"\n                action = \"Exercise caution - market is unstable\"\n            elif vol_ratio > 1.2:
                volatility_status = \"⚠️ ELEVATED VOLATILITY\"\n                action = \"Increased risk - monitor closely\"\n            else:
                volatility_status = \"✅ NORMAL VOLATILITY\"\n                action = \"Market is stable\"\n            
            return {
                'ticker': ticker.upper(),
                'volatility_status': volatility_status,
                'recent_volatility': round(recent_vol, 2),
                'historical_volatility': round(historical_vol, 2),
                'volatility_ratio': round(vol_ratio, 2),
                'action': action\n            }
        except Exception as e:
            return {'error': str(e)}
    
    def detect_multiple_anomalies(self, tickers: list) -> dict:
        \"\"\"Detect anomalies for multiple stocks\"\"\"
        results = {}
        for ticker in tickers:
            spike = self.detect_price_spike(ticker)
            if 'error' not in spike:
                results[ticker.upper()] = {
                    'spike': spike,
                    'trend': self.detect_trend_reversal(ticker),
                    'volatility': self.detect_volatility_surge(ticker)\n                }
        return results
