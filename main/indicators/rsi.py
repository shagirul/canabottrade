import pandas as pd
import talib
from .base import Indicator

class RSI(Indicator):
    """Relative Strength Index (RSI) Indicator."""
    
    def __init__(self, period: int = 14):
        self.period = period
    
    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """Computes RSI and adds it to the DataFrame."""
        data["RSI"] = talib.RSI(data["Close"], timeperiod=self.period)
        
        return data
