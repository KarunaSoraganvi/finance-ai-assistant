"""AI Assistant for Stock Analysis using OpenAI GPT-4"""
import os
import json
from typing import Optional, List, Dict, Any
from openai import OpenAI
from stock_fetcher import StockFetcher
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockAIAssistant:
    """AI Assistant for stock price queries and analysis"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.stock_fetcher = StockFetcher()
        self.conversation_history = []
        self.model = "gpt-4"
        self.setup_tools()
    
    def setup_tools(self):
        """Define tools available to the AI"""
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_stock_price",
                    "description": "Get the current price and information for a single stock ticker",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ticker": {
                                "type": "string",
                                "description": "Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
                            }
                        },
                        "required": ["ticker"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_multiple_prices",
                    "description": "Get current prices for multiple stock tickers",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tickers": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of stock ticker symbols"
                            }
                        },
                        "required": ["tickers"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "compare_stocks",
                    "description": "Compare prices and performance of multiple stocks",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tickers": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of stock ticker symbols to compare"
                            }
                        },
                        "required": ["tickers"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_price_change",
                    "description": "Get price change over a specified number of days",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ticker": {
                                "type": "string",
                                "description": "Stock ticker symbol"
                            },
                            "days": {
                                "type": "integer",
                                "description": "Number of days to look back (default: 30)",
                                "default": 30
                            }
                        },
                        "required": ["ticker"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_historical_data",
                    "description": "Get historical price data for a stock over a period",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ticker": {
                                "type": "string",
                                "description": "Stock ticker symbol"
                            },
                            "period": {
                                "type": "string",
                                "description": "Period for historical data (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, max)",
                                "default": "1mo"
                            }
                        },
                        "required": ["ticker"]
                    }
                }
            }
        ]
    
    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Execute a tool based on function name"""
        try:
            if tool_name == "get_stock_price":
                result = self.stock_fetcher.get_stock_price(tool_input["ticker"])
            elif tool_name == "get_multiple_prices":
                result = self.stock_fetcher.get_multiple_prices(tool_input["tickers"])
            elif tool_name == "compare_stocks":
                result = self.stock_fetcher.compare_stocks(tool_input["tickers"])
            elif tool_name == "get_price_change":
                days = tool_input.get("days", 30)
                result = self.stock_fetcher.get_price_change(tool_input["ticker"], days)
            elif tool_name == "get_historical_data":
                period = tool_input.get("period", "1mo")
                df = self.stock_fetcher.get_historical_data(tool_input["ticker"], period)
                result = df.to_dict() if df is not None else None
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
            
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return json.dumps({"error": str(e)})
    
    def chat(self, user_message: str) -> str:
        """Send a message and get a response from the AI"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Initial API call
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            tools=self.tools,
            tool_choice="auto"
        )
        
        # Process response and handle tool calls
        while response.choices[0].finish_reason == "tool_calls":
            assistant_message = response.choices[0].message
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [tc.model_dump() for tc in assistant_message.tool_calls]
            })
            
            # Execute tools
            tool_results = []
            for tool_call in assistant_message.tool_calls:
                tool_result = self.execute_tool(
                    tool_call.function.name,
                    json.loads(tool_call.function.arguments)
                )
                tool_results.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "content": tool_result
                })
            
            # Add tool results to history
            self.conversation_history.extend(tool_results)
            
            # Get next response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                tools=self.tools,
                tool_choice="auto"
            )
        
        # Extract final message
        final_message = response.choices[0].message.content
        self.conversation_history.append({
            "role": "assistant",
            "content": final_message
        })
        
        return final_message
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict]:
        """Get current conversation history"""
        return self.conversation_history
