import pandas as pd
from .base import Indicator
import talib


class MovingAverage(Indicator):
    """Calculates Moving Averages (SMA/EMA)."""

    def __init__(self, period=14, method="SMA"):
        self.period = period
        self.method = method.upper()  # Ensure uppercase

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculates the moving average and adds it to the dataframe."""
        if "Close" not in data.columns:
            raise ValueError("Data must contain a 'Close' column.")

        if self.method == "SMA":
            data[f"SMA_{self.period}"] = talib.SMA(data["Close"], timeperiod=self.period)
        elif self.method == "EMA":
            data[f"EMA_{self.period}"] = talib.EMA(data["Close"], timeperiod=self.period)
        else:
            raise ValueError("Unsupported moving average method. Use 'SMA' or 'EMA'.")
        
        return data
