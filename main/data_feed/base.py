from abc import ABC, abstractmethod
import pandas as pd

class DataFeed(ABC):
    """Abstract base class for fetching OHLCV data from different sources."""
    
    @abstractmethod
    def fetch_data(self, symbol: str, start_date: str, end_date: str, timeframe: str) -> pd.DataFrame:
        """
        Fetch OHLCV data for a given symbol, date range, and timeframe.
        
        :param symbol: The asset symbol (e.g., "AAPL").
        :param start_date: Start date (YYYY-MM-DD).
        :param end_date: End date (YYYY-MM-DD).
        :param timeframe: Time interval (e.g., "1min", "1hour", "1day").
        :return: Pandas DataFrame with OHLCV data.
        """
        pass
