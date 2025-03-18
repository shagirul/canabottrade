import pandas as pd
from datetime import datetime
from .base import DataFeed

class CSVDataFeed(DataFeed):
    """Loads OHLCV data from CSV files."""
    
    def __init__(self, file_path: str):
        """
        Initialize CSVDataFeed with a specific CSV file path.
        
        :param file_path: Path to the CSV file containing OHLCV data.
        """
        self.file_path = file_path
        self.data = pd.read_csv(file_path)  

        # Convert 'Date' column to datetime
        self.data['Date'] = pd.to_datetime(self.data['Date'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        
        # Convert 'Close' to float (handling comma-separated values)
        self.data['Close'] = self.data['Close'].astype(str).str.replace(',', '').astype(float)

    def fetch_data(self, symbol: str, start_date: str, end_date: str, timeframe: str) -> pd.DataFrame:
        """
        Fetch OHLCV data filtered by date range and resample based on timeframe.
        
        :param symbol: Asset symbol (e.g., BTC/USD).
        :param start_date: Start date string (YYYY-MM-DD HH:MM:SS).
        :param end_date: End date string (YYYY-MM-DD HH:MM:SS).
        :param timeframe: Timeframe for resampling (e.g., 1min, 15min, 1hour, etc.).
        :return: Resampled OHLCV DataFrame.
        """
        # Convert start and end dates
        start_dt = pd.to_datetime(start_date, format='%Y-%m-%d %H:%M:%S', errors='coerce')
        end_dt = pd.to_datetime(end_date, format='%Y-%m-%d %H:%M:%S', errors='coerce')

        # Ensure data is sorted before filtering
        self.data = self.data.sort_values(by='Date', ascending=True)

        # Apply date filtering
        filtered_df = self.data[(self.data['Date'] >= start_dt) & (self.data['Date'] <= end_dt)]

        if filtered_df.empty:
            print("❌ No data available for the given date range.")
            return filtered_df  # Return empty DataFrame if no data

        # Ensure 'Date' is the index for resampling
        filtered_df = filtered_df.set_index('Date')

        # Define timeframe mapping
        timeframe_mapping = {
            "1min": "1T",
            "15min": "15T",
            "30min": "30T",
            "1hour": "1H",
            "1day": "1D",
            "1week": "1W",
            "1month": "1M",
            "6month": "6M"
        }

        if timeframe not in timeframe_mapping:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        # Resample and aggregate OHLCV data
        rule = timeframe_mapping[timeframe]
        resampled_df = filtered_df.resample(rule).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume BTC': 'sum',
            'Volume USD': 'sum'
        }).dropna()  # Remove NaN values caused by resampling

        # Reset index to bring back 'Date' as a column
        return resampled_df.reset_index()
