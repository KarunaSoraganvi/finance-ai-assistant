#!/usr/bin/env python3
"""Command-line interface for Stock AI Assistant"""
import os
import sys
from dotenv import load_dotenv
from ai_assistant import StockAIAssistant
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*50)
    print("  💰 Stock AI Assistant - CLI")
    print("  Powered by OpenAI GPT-4 & Yahoo Finance")
    print("="*50)
    print("\nCommands:")
    print("  - Type your question to get stock information")
    print("  - Example: 'What is the price of Apple stock?'")
    print("  - Example: 'Compare AAPL and MSFT'")
    print("  - Type 'exit' or 'quit' to exit")
    print("  - Type 'clear' to clear conversation history")
    print("  - Type 'history' to see conversation history\n")

def main():
    """Main CLI function"""
    try:
        print_banner()
        assistant = StockAIAssistant()
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit']:
                    print("\n👋 Thank you for using Stock AI Assistant!")
                    sys.exit(0)
                
                if user_input.lower() == 'clear':
                    assistant.reset_conversation()
                    print("✓ Conversation history cleared")
                    continue
                
                if user_input.lower() == 'history':
                    history = assistant.get_conversation_history()
                    print("\n📋 Conversation History:")
                    print("-" * 50)
                    for msg in history:
                        role = msg.get('role', 'unknown').upper()
                        content = msg.get('content', '')[:100]  # First 100 chars
                        print(f"{role}: {content}...")
                    continue
                
                print("\nAssistant: ", end="", flush=True)
                response = assistant.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Thank you for using Stock AI Assistant!")
                sys.exit(0)
            except Exception as e:
                logger.error(f"Error: {str(e)}")
                print(f"❌ Error: {str(e)}")
    
    except ValueError as e:
        print(f"❌ Initialization Error: {str(e)}")
        print("\nPlease make sure:")
        print("1. Create a .env file with OPENAI_API_KEY")
        print("2. Copy from .env.example and add your OpenAI API key")
        sys.exit(1)

if __name__ == '__main__':
    main()
