#!/usr/bin/env python3
"""NLP-Based Stock Fetcher - Natural Language Understanding"""
import re
from stock_fetcher import StockFetcher
from dotenv import load_dotenv

load_dotenv()

class NLPStockFetcher:
    """NLP-based stock fetcher with natural language understanding"""
    
    def __init__(self):
        self.fetcher = StockFetcher()
        self.ticker_map = {
            'apple': 'AAPL',
            'microsoft': 'MSFT',
            'google': 'GOOGL',
            'alphabet': 'GOOGL',
            'amazon': 'AMZN',
            'meta': 'META',
            'facebook': 'META',
            'tesla': 'TSLA',
            'nvidia': 'NVDA',
            'intel': 'INTC',
            'amd': 'AMD',
            'coca cola': 'KO',
            'mcdonalds': 'MCD',
            'netflix': 'NFLX',
            'uber': 'UBER',
        }
    
    def extract_tickers(self, text: str) -> list:
        """Extract ticker symbols from natural language text"""
        tickers = []
        text_lower = text.lower()
        
        # Check for company names
        for company, ticker in self.ticker_map.items():
            if company in text_lower:
                tickers.append(ticker)
        
        # Check for direct ticker symbols (e.g., AAPL, MSFT)
        ticker_pattern = r'\b[A-Z]{1,5}\b'
        found_tickers = re.findall(ticker_pattern, text)
        tickers.extend(found_tickers)
        
        return list(set(tickers))  # Remove duplicates
    
    def extract_days(self, text: str) -> int:
        """Extract number of days from text"""
        # Pattern for "X days"
        days_match = re.search(r'(\d+)\s*(?:day|days)', text, re.IGNORECASE)
        if days_match:
            return int(days_match.group(1))
        
        # Pattern for time periods
        if re.search(r'week', text, re.IGNORECASE):
            return 7
        elif re.search(r'month', text, re.IGNORECASE):
            return 30
        elif re.search(r'quarter', text, re.IGNORECASE):
            return 90
        elif re.search(r'year', text, re.IGNORECASE):
            return 365
        
        return 30  # Default
    
    def detect_query_type(self, text: str) -> str:
        """Detect what the user is asking for"""
        text_lower = text.lower()
        
        # Single stock price
        if re.search(r'(price|current|what.*price|how much)', text_lower):
            if 'compare' in text_lower or ' vs ' in text_lower or ' and ' in text_lower:
                return 'compare'
            else:
                return 'single_price'
        
        # Multiple stocks
        if re.search(r'(multiple|several|list|prices|all)', text_lower):
            return 'multiple_prices'
        
        # Comparison
        if re.search(r'(compare|vs|versus|difference)', text_lower):
            return 'compare'
        
        # Price change
        if re.search(r'(change|change over|last|past|how much.*changed)', text_lower):
            return 'price_change'
        
        # Default
        return 'single_price'
    
    def process_query(self, user_input: str) -> dict:
        """Process natural language query"""
        print(f"\n🔍 Analyzing: '{user_input}'\n")
        
        # Extract information
        tickers = self.extract_tickers(user_input)
        days = self.extract_days(user_input)
        query_type = self.detect_query_type(user_input)
        
        if not tickers:
            return {'error': '❌ No stock ticker found. Try: "AAPL", "Apple", or "Microsoft"'}
        
        print(f"📊 Detected: {query_type.replace('_', ' ').title()}")
        print(f"🎯 Tickers: {', '.join(tickers)}")
        if query_type == 'price_change':
            print(f"⏰ Period: {days} days\n")
        else:
            print()
        
        # Execute query
        if query_type == 'single_price':
            return self.get_single_price(tickers[0])
        elif query_type == 'multiple_prices':
            return self.get_multiple_prices(tickers)
        elif query_type == 'compare':
            return self.compare_stocks(tickers[:2] if len(tickers) >= 2 else tickers)
        elif query_type == 'price_change':
            return self.get_price_change(tickers[0], days)
        
        return {'error': 'Could not process query'}
    
    def get_single_price(self, ticker: str) -> dict:
        """Get single stock price"""
        data = self.fetcher.get_stock_price(ticker)
        if data:
            return {'type': 'single', 'data': data}
        return {'error': f'Could not fetch {ticker}'}
    
    def get_multiple_prices(self, tickers: list) -> dict:
        """Get multiple stock prices"""
        data = self.fetcher.get_multiple_prices(tickers)
        if data:
            return {'type': 'multiple', 'data': data}
        return {'error': 'Could not fetch stocks'}
    
    def compare_stocks(self, tickers: list) -> dict:
        """Compare stocks"""
        data = self.fetcher.compare_stocks(tickers)
        if data:
            return {'type': 'comparison', 'data': data}
        return {'error': 'Could not compare stocks'}
    
    def get_price_change(self, ticker: str, days: int) -> dict:
        """Get price change over time"""
        data = self.fetcher.get_price_change(ticker, days)
        if data:
            return {'type': 'price_change', 'data': data}
        return {'error': f'Could not fetch data for {ticker}'}
    
    def display_result(self, result: dict):
        """Display result in formatted way"""
        if 'error' in result:
            print(result['error'])
            return
        
        result_type = result.get('type')
        data = result.get('data')
        
        if result_type == 'single':
            print(f"{'='*50}")
            print(f"  {data['name']} ({data['ticker']})")
            print(f"{'='*50}")
            print(f"  Current Price:  ${data['current_price']}")
            print(f"  Change:         ${data['change']} ({data['change_percent']}%)")
            print(f"  Previous Close: ${data['previous_close']}")
            print(f"{'='*50}\n")
        
        elif result_type == 'multiple':
            print(f"{'='*70}")
            print(f"  {'Ticker':<10} {'Price':<12} {'Change':<15} {'Change %':<10}")
            print(f"{'='*70}")
            for ticker, info in data.items():
                change_color = "🔴" if info['change'] < 0 else "🟢"
                print(f"  {ticker:<10} ${info['current_price']:<11} {change_color} ${info['change']:<14} {info['change_percent']}%")
            print(f"{'='*70}\n")
        
        elif result_type == 'comparison':
            print(f"{'='*50}")
            print(f"  {'Ticker':<10} {'Price':<15} {'Change %':<15}")
            print(f"{'='*50}")
            for ticker, info in data.items():
                change_color = "📈" if info['change_percent'] > 0 else "📉"
                print(f"  {ticker:<10} ${info['price']:<14} {change_color} {info['change_percent']}%")
            print(f"{'='*50}\n")
        
        elif result_type == 'price_change':
            print(f"{'='*50}")
            print(f"  {data['ticker']} - {data['period_days']} Day Analysis")
            print(f"{'='*50}")
            print(f"  Start Price:    ${data['start_price']}")
            print(f"  Current Price:  ${data['end_price']}")
            print(f"  Change:         ${data['change']} ({data['change_percent']}%)")
            print(f"  Highest:        ${data['highest']}")
            print(f"  Lowest:         ${data['lowest']}")
            print(f"{'='*50}\n")
    
    def interactive_chat(self):
        """Interactive NLP chat mode"""
        print("\n" + "="*60)
        print("  💬 NLP STOCK FETCHER")
        print("  Ask naturally about stock prices!")
        print("="*60)
        print("\nExample queries:")
        print("  • What is the price of Apple?")
        print("  • Compare AAPL and MSFT")
        print("  • TSLA vs GOOGL over 90 days")
        print("  • Show me Tesla, Microsoft, and Google prices")
        print("  • Microsoft price change last month")
        print("  • help - Show commands")
        print("  • exit - Quit\n")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'exit':
                    print("\n👋 Goodbye!\n")
                    break
                
                if user_input.lower() == 'help':
                    print("\nExample queries:")
                    print("  • What is the current price of Apple stock?")
                    print("  • Compare AAPL and Microsoft")
                    print("  • Tesla vs Nvidia over 90 days")
                    print("  • Show prices for AAPL, MSFT, GOOGL")
                    print("  • How much did TSLA change in the last 60 days?")
                    continue
                
                result = self.process_query(user_input)
                self.display_result(result)
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")

def main():
    """Main entry point"""
    fetcher = NLPStockFetcher()
    fetcher.interactive_chat()

if __name__ == '__main__':
    main()
