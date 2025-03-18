from .csv_data_feed import CSVDataFeed
from .api_data_feed import APIDataFeed

class DataFeedFactory:
    """Factory to create different types of DataFeed instances."""

    @staticmethod
    def create_data_feed(source: str, **kwargs):
        """
        Create a DataFeed instance based on the source type.
        
        :param source: "csv" or "api"
        :param kwargs: Additional parameters like file_path or api_url.
        :return: Instance of CSVDataFeed or APIDataFeed.
        """
        if source == "csv":
            return CSVDataFeed(kwargs.get("file_path"))
        elif source == "api":
            return APIDataFeed(kwargs.get("api_url"))
        else:
            raise ValueError(f"Unsupported data source: {source}")
