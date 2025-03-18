import pandas as pd
import tempfile
import os
from main.data_feed import CSVDataFeed

# Sample OHLCV CSV content
CSV_CONTENT = """date,open,high,low,close,volume
2024-01-01,100,105,98,102,50000
2024-01-02,102,108,101,107,60000
"""

def test_csv_data_feed():
    """Test CSVDataFeed loading and filtering."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
        tmp_file.write(CSV_CONTENT.encode())
        tmp_file.close()

        # Load CSVDataFeed
        csv_feed = CSVDataFeed(tmp_file.name)
        
        # Fetch data
        df = csv_feed.fetch_data(symbol="AAPL", start_date="2024-01-01", end_date="2024-01-02", timeframe="1day")

        # Expected DataFrame
        expected_df = pd.DataFrame({
            "date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "open": [100, 102],
            "high": [105, 108],
            "low": [98, 101],
            "close": [102, 107],
            "volume": [50000, 60000]
        })

        # Convert dates for comparison
        df["date"] = pd.to_datetime(df["date"])

        # Assertions
        pd.testing.assert_frame_equal(df.reset_index(drop=True), expected_df.reset_index(drop=True))

        # Cleanup
        os.remove(tmp_file.name)
