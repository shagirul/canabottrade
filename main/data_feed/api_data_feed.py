import requests
import pandas as pd
from .base import DataFeed
# data_feed import DataFeedFactory

class APIDataFeed(DataFeed):
    """Fetches OHLCV data from an external API."""
    
    def __init__(self, api_url: str):
        """
        Initialize APIDataFeed with an API URL.
        
        :param api_url: Base URL for the market data API.
        """
        self.api_url = api_url

    def fetch_data(self, symbol: str, start_date: str, end_date: str, timeframe: str) -> pd.DataFrame:
        """
        Fetch OHLCV data from an API for a given symbol and date range.
        
        :param symbol: The asset symbol (e.g., "AAPL").
        :param start_date: Start date (YYYY-MM-DD).
        :param end_date: End date (YYYY-MM-DD).
        :param timeframe: Time interval (e.g., "1min", "1hour", "1day").
        :return: Pandas DataFrame with OHLCV data.
        """
        params = {
            "symbol": symbol,
            "start": start_date,
            "end": end_date,
            "timeframe": timeframe
        }
        response = requests.get(f"{self.api_url}/ohlcv", params=params)
        data = response.json()

        return pd.DataFrame(data, columns=["date", "open", "high", "low", "close", "volume"])

# Example API response:
# [
#   {"date": "2024-01-01", "open": 100, "high": 105, "low": 98, "close": 102, "volume": 50000},
#   {"date": "2024-01-02", "open": 102, "high": 108, "low": 101, "close": 107, "volume": 60000}
# ]
