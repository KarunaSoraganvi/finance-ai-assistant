#!/usr/bin/env python3
"""Simple Stock Price Fetcher - Direct data without AI"""
import os
from stock_fetcher import StockFetcher
from dotenv import load_dotenv

load_dotenv()

class SimpleStockApp:
    """Simple command-line tool for fetching stock prices"""
    
    def __init__(self):
        self.fetcher = StockFetcher()
    
    def print_stock_price(self, ticker: str):
        """Print a single stock price"""
        print(f"\n📊 Fetching {ticker}...")
        data = self.fetcher.get_stock_price(ticker)
        
        if data:
            print(f"\n{'='*50}")
            print(f"  {data['name']} ({data['ticker']})")
            print(f"{'='*50}")
            print(f"  Current Price:  ${data['current_price']}")
            print(f"  Previous Close: ${data['previous_close']}")
            print(f"  Change:         ${data['change']} ({data['change_percent']}%)")
            print(f"  Currency:       {data['currency']}")
            print(f"{'='*50}\n")
        else:
            print(f"❌ Could not find stock: {ticker}\n")
    
    def print_multiple_prices(self, tickers: list):
        """Print prices for multiple stocks"""
        print(f"\n📈 Fetching {len(tickers)} stocks...")
        data = self.fetcher.get_multiple_prices(tickers)
        
        if data:
            print(f"\n{'='*70}")
            print(f"  {'Ticker':<10} {'Price':<12} {'Change':<15} {'Change %':<10}")
            print(f"{'='*70}")
            
            for ticker, info in data.items():
                change_color = "🔴" if info['change'] < 0 else "🟢"
                print(f"  {ticker:<10} ${info['current_price']:<11} {change_color} ${info['change']:<14} {info['change_percent']}%")
            
            print(f"{'='*70}\n")
        else:
            print(f"❌ Could not fetch any stocks\n")
    
    def print_price_change(self, ticker: str, days: int = 30):
        """Print price change over time"""
        print(f"\n📉 Fetching {days}-day price change for {ticker}...")
        data = self.fetcher.get_price_change(ticker, days)
        
        if data:
            print(f"\n{'='*50}")
            print(f"  {data['ticker']} - {data['period_days']} Day Analysis")
            print(f"{'='*50}")
            print(f"  Start Price:    ${data['start_price']}")
            print(f"  Current Price:  ${data['end_price']}")
            print(f"  Change:         ${data['change']} ({data['change_percent']}%)")
            print(f"  Highest:        ${data['highest']}")
            print(f"  Lowest:         ${data['lowest']}")
            print(f"{'='*50}\n")
        else:
            print(f"❌ Could not fetch data for {ticker}\n")
    
    def compare_stocks(self, tickers: list):
        """Compare multiple stocks side by side"""
        print(f"\n🔄 Comparing {len(tickers)} stocks...")
        data = self.fetcher.compare_stocks(tickers)
        
        if data:
            print(f"\n{'='*50}")
            print(f"  {'Ticker':<10} {'Price':<15} {'Change %':<15}")
            print(f"{'='*50}")
            
            for ticker, info in data.items():
                change_color = "📈" if info['change_percent'] > 0 else "📉"
                print(f"  {ticker:<10} ${info['price']:<14} {change_color} {info['change_percent']}%")
            
            print(f"{'='*50}\n")
        else:
            print(f"❌ Could not compare stocks\n")
    
    def interactive_menu(self):
        """Interactive menu for simple stock fetching"""
        print("\n" + "="*50)
        print("  💰 Stock Price Fetcher")
        print("  Direct data from Yahoo Finance")
        print("="*50)
        print("\nOptions:")
        print("  1. Get single stock price")
        print("  2. Get multiple stock prices")
        print("  3. Check price change over time")
        print("  4. Compare stocks")
        print("  5. Exit")
        print()
        
        while True:
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                ticker = input("Enter ticker symbol (e.g., AAPL): ").strip().upper()
                if ticker:
                    self.print_stock_price(ticker)
            
            elif choice == '2':
                tickers_input = input("Enter ticker symbols separated by commas (e.g., AAPL,MSFT,GOOGL): ").strip().upper()
                tickers = [t.strip() for t in tickers_input.split(',') if t.strip()]
                if tickers:
                    self.print_multiple_prices(tickers)
            
            elif choice == '3':
                ticker = input("Enter ticker symbol: ").strip().upper()
                days_input = input("Enter number of days (default 30): ").strip()
                days = int(days_input) if days_input.isdigit() else 30
                if ticker:
                    self.print_price_change(ticker, days)
            
            elif choice == '4':
                tickers_input = input("Enter ticker symbols to compare (e.g., AAPL,MSFT): ").strip().upper()
                tickers = [t.strip() for t in tickers_input.split(',') if t.strip()]
                if tickers:
                    self.compare_stocks(tickers)
            
            elif choice == '5':
                print("\n👋 Goodbye!\n")
                break
            
            else:
                print("❌ Invalid option. Please select 1-5.")

def main():
    """Main entry point"""
    app = SimpleStockApp()
    app.interactive_menu()

if __name__ == '__main__':
    main()
