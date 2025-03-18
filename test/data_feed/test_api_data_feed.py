import pytest
import pandas as pd
import requests
from unittest.mock import patch
from main.data_feed import APIDataFeed

# Mock API response
MOCK_API_RESPONSE = [
    {"date": "2024-01-01", "open": 100, "high": 105, "low": 98, "close": 102, "volume": 50000},
    {"date": "2024-01-02", "open": 102, "high": 108, "low": 101, "close": 107, "volume": 60000}
]

@pytest.fixture
def mock_api():
    """Mocks requests.get() for APIDataFeed."""
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = MOCK_API_RESPONSE
        yield mock_get

def test_api_data_feed(mock_api):
    """Test APIDataFeed fetching data correctly."""
    api_feed = APIDataFeed(api_url="https://fakeapi.com")

    df = api_feed.fetch_data(symbol="AAPL", start_date="2024-01-01", end_date="2024-01-02", timeframe="1day")

    # Expected DataFrame
    expected_df = pd.DataFrame({
        "date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
        "open": [100, 102],
        "high": [105, 108],
        "low": [98, 101],
        "close": [102, 107],
        "volume": [50000, 60000]
    })

    # Convert date column for comparison
    df["date"] = pd.to_datetime(df["date"])

    # Assertions
    pd.testing.assert_frame_equal(df.reset_index(drop=True), expected_df.reset_index(drop=True))
