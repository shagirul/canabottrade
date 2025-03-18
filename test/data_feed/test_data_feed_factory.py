import pytest
from main.data_feed import DataFeedFactory
from main.data_feed import CSVDataFeed
from main.data_feed import APIDataFeed

def test_create_csv_data_feed():
    """Test if DataFeedFactory correctly returns CSVDataFeed."""
    csv_feed = DataFeedFactory.create_data_feed("csv", file_path="test.csv")
    assert isinstance(csv_feed, CSVDataFeed)

def test_create_api_data_feed():
    """Test if DataFeedFactory correctly returns APIDataFeed."""
    api_feed = DataFeedFactory.create_data_feed("api", api_url="https://fakeapi.com")
    assert isinstance(api_feed, APIDataFeed)

def test_invalid_data_feed():
    """Test if DataFeedFactory raises an error for unsupported sources."""
    with pytest.raises(ValueError, match="Unsupported data source: invalid"):
        DataFeedFactory.create_data_feed("invalid")
