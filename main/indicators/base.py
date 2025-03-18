from abc import ABC, abstractmethod
import pandas as pd

class Indicator(ABC):
    """Abstract class for indicators."""
    
    @abstractmethod
    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Computes the indicator and adds it to the DataFrame.
        
        :param data: DataFrame with OHLCV data.
        :return: DataFrame with additional indicator column(s).
        """
        pass
