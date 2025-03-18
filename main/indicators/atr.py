from .base import Indicator
import pandas as pd
import talib

class ATR(Indicator):
    """Calculates Average True Range (ATR)."""

    def __init__(self, period=14):
        self.period = period

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculates ATR and adds it to the dataframe."""
        if not all(col in data.columns for col in ["High", "Low", "Close"]):
            raise ValueError("Data must contain 'High', 'Low', and 'Close' columns.")

        data[f"ATR_{self.period}"] = talib.ATR(data["High"], data["Low"], data["Close"], timeperiod=self.period)
        return data
