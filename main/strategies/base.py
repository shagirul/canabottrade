from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    """Abstract class for trading strategies."""
    
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Analyzes data and generates buy/sell signals.
        
        :param data: DataFrame containing OHLCV + indicators.
        :return: DataFrame with an additional 'signal' column.
        """
        pass
