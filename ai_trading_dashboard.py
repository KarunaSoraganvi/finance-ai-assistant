"""AI Trading Dashboard - Interactive Interface for All AI Features"""
import os
from dotenv import load_dotenv
from price_predictor import PricePredictor
from sentiment_analyzer import SentimentAnalyzer
from trading_recommender import TradingRecommender
from anomaly_detector import AnomalyDetector
from stock_fetcher import StockFetcher

load_dotenv()

class AITradingDashboard:
    """Interactive dashboard for AI trading features"""
    
    def __init__(self):
        self.predictor = PricePredictor()
        self.sentiment = SentimentAnalyzer()
        self.recommender = TradingRecommender()
        self.anomaly = AnomalyDetector()
        self.fetcher = StockFetcher()
    
    def print_header(self):
        """Print dashboard header"""
        print("\n" + "="*60)
        print("  🤖 AI TRADING DASHBOARD")
        print("  Powered by Machine Learning & Technical Analysis")
        print("="*60)
        print("\nOptions:")
        print("  1. 📈 Price Prediction       (Next day/week forecast)")
        print("  2. 💭 Sentiment Analysis     (Market mood 0-100)")
        print("  3. 💡 Trading Recommendation (BUY/SELL/HOLD signals)")
        print("  4. 🚨 Anomaly Detection      (Unusual movements)")
        print("  5. 💼 Portfolio Analysis     (Your holdings analysis)")
        print("  6. 📊 Full Stock Report      (Everything combined)")
        print("  7. ❌ Exit\n")
    
    def display_price_prediction(self):
        """Display price prediction"""
        print("\n" + "="*60)
        print("  📈 PRICE PREDICTION")
        print("="*60)
        
        ticker = input("\nEnter ticker symbol (e.g., AAPL): ").strip().upper()
        if not ticker:
            return
        
        print("\nSelect prediction type:")
        print("  1. Next day")
        print("  2. Next week\n")
        choice = input("Select (1-2): ").strip()
        
        if choice == '1':
            result = self.predictor.predict_next_day(ticker)
        elif choice == '2':
            result = self.predictor.predict_week(ticker)
        else:
            print("Invalid choice")
            return
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return
        
        print(f"\n{'─'*60}")
        print(f"Stock: {result['ticker']}")
        print(f"Current Price: ${result['current_price']}")
        print(f"Predicted Price: ${result['predicted_price']}")
        print(f"Expected Change: ${result['predicted_change']} ({result['predicted_change_percent']}%)")
        print(f"Direction: {result['direction']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"Recommendation: {result['recommendation']}")
        print(f"{'─'*60}\n")
    
    def display_sentiment_analysis(self):
        """Display sentiment analysis"""
        print("\n" + "="*60)
        print("  💭 SENTIMENT ANALYSIS")
        print("="*60)
        
        ticker = input("\nEnter ticker symbol (e.g., AAPL): ").strip().upper()
        if not ticker:
            return
        
        result = self.sentiment.calculate_technical_sentiment(ticker)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return
        
        print(f"\n{'─'*60}")
        print(f"Stock: {result['ticker']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Sentiment Score: {result['sentiment_score']}/100")
        print(f"RSI: {result['rsi']} {'(Oversold ⬇️)' if result['rsi'] < 30 else '(Overbought ⬆️)' if result['rsi'] > 70 else '(Neutral ➡️)'}")
        print(f"Current Price: ${result['current_price']}")
        print(f"SMA 20: ${result['sma_20']}")
        print(f"SMA 50: ${result['sma_50']}")
        print(f"{'─'*60}\n")
    
    def display_trading_recommendation(self):
        """Display trading recommendation"""
        print("\n" + "="*60)
        print("  💡 TRADING RECOMMENDATION")
        print("="*60)
        
        ticker = input("\nEnter ticker symbol (e.g., AAPL): ").strip().upper()
        if not ticker:
            return
        
        result = self.recommender.get_recommendation(ticker)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return
        
        print(f"\n{'─'*60}")
        print(f"Stock: {result['ticker']}")
        print(f"Current Price: ${result['current_price']}")
        print(f"Recommendation: {result['recommendation']}")
        print(f"Signal Strength: {result['signal_strength']}")
        print(f"Confidence Score: {result['confidence_score']}/100")
        print(f"Predicted Price: ${result['predicted_price']}")
        print(f"Predicted Change: ${result['predicted_change']}")
        print(f"RSI: {result['rsi']}")
        print(f"{'─'*60}\n")
    
    def display_anomaly_detection(self):
        """Display anomaly detection"""
        print("\n" + "="*60)
        print("  🚨 ANOMALY DETECTION")
        print("="*60)
        
        ticker = input("\nEnter ticker symbol (e.g., AAPL): ").strip().upper()
        if not ticker:
            return
        
        spike = self.anomaly.detect_price_spike(ticker)
        trend = self.anomaly.detect_trend_reversal(ticker)
        volatility = self.anomaly.detect_volatility_surge(ticker)
        
        if 'error' in spike:
            print(f"❌ Error: {spike['error']}")
            return
        
        print(f"\n{'─'*60}")
        print(f"Stock: {spike['ticker']}")
        print(f"\n📊 Price Spike Analysis:")
        print(f"  Anomaly: {spike['anomaly_type']}")
        print(f"  Daily Return: {spike['daily_return']}%")
        print(f"  Alert Level: {spike['alert_level']}")
        print(f"\n📈 Trend Analysis:")
        print(f"  Current Trend: {trend['current_trend']}")
        print(f"  Reversal Risk: {trend['reversal_risk']}")
        print(f"\n💨 Volatility Analysis:")
        print(f"  Status: {volatility['volatility_status']}")
        print(f"{'─'*60}\n")
    
    def display_portfolio_analysis(self):
        """Display portfolio analysis"""
        print("\n" + "="*60)
        print("  💼 PORTFOLIO ANALYSIS")
        print("="*60)
        
        portfolio_str = input("\nEnter portfolio (format: AAPL:100,MSFT:50): ").strip()
        
        try:
            portfolio = {}
            for item in portfolio_str.split(','):
                ticker, shares = item.split(':')
                portfolio[ticker.strip()] = int(shares.strip())
        except:
            print("❌ Invalid format. Use: AAPL:100,MSFT:50")
            return
        
        result = self.recommender.portfolio_recommendation(portfolio)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return
        
        print(f"\n{'─'*60}")
        print(f"Total Portfolio Value: ${result['total_portfolio_value']}")
        print(f"\n📊 Current Allocations:")
        for ticker, allocation in result['allocations'].items():
            print(f"  {ticker}: {allocation}%")
        print(f"{'─'*60}\n")
    
    def display_full_report(self):
        """Display full stock report"""
        print("\n" + "="*60)
        print("  📊 FULL STOCK REPORT")
        print("="*60)
        
        ticker = input("\nEnter ticker symbol (e.g., AAPL): ").strip().upper()
        if not ticker:
            return
        
        print(f"\nGenerating comprehensive report for {ticker}...")
        
        price_data = self.fetcher.get_stock_price(ticker)
        prediction = self.predictor.predict_next_day(ticker)
        sentiment = self.sentiment.calculate_technical_sentiment(ticker)
        anomaly = self.anomaly.detect_price_spike(ticker)
        
        print(f"\n{'═'*60}")
        print(f"  {ticker} - COMPREHENSIVE ANALYSIS")
        print(f"{'═'*60}")
        print(f"\n💰 CURRENT PRICE: ${price_data['current_price']} ({price_data['change_percent']}%)")
        print(f"📈 PREDICTION: ${prediction['predicted_price']} ({prediction['direction']})")
        print(f"💭 SENTIMENT: {sentiment['sentiment']} ({sentiment['sentiment_score']}/100)")
        print(f"🚨 ANOMALY: {anomaly['anomaly_type']} (Alert: {anomaly['alert_level']})")
        print(f"{'═'*60}\n")
    
    def run(self):
        """Main dashboard loop"""
        while True:
            self.print_header()
            choice = input("Select option (1-7): ").strip()
            
            if choice == '1':
                self.display_price_prediction()
            elif choice == '2':
                self.display_sentiment_analysis()
            elif choice == '3':
                self.display_trading_recommendation()
            elif choice == '4':
                self.display_anomaly_detection()
            elif choice == '5':
                self.display_portfolio_analysis()
            elif choice == '6':
                self.display_full_report()
            elif choice == '7':
                print("\n👋 Thank you for using AI Trading Dashboard!\n")
                break
            else:
                print("❌ Invalid option. Please select 1-7.")

def main():
    """Main entry point"""
    dashboard = AITradingDashboard()
    dashboard.run()

if __name__ == '__main__':
    main()
