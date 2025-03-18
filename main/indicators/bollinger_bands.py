import pandas as pd
import talib
from .base import Indicator

class BollingerBands(Indicator):
    """Bollinger Bands Indicator."""
    
    def __init__(self, period: int = 20, std_dev: int = 2):
        self.period = period
        self.std_dev = std_dev
    
    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """Computes Bollinger Bands and adds them to the DataFrame."""
        upper, middle, lower = talib.BBANDS(data["Close"], timeperiod=self.period, nbdevup=self.std_dev, nbdevdn=self.std_dev)
        data["BB_Upper"] = upper
        data["BB_Middle"] = middle
        data["BB_Lower"] = lower
        return data
