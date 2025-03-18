import pandas as pd
from .base import Strategy
from indicators.rsi import RSI
from indicators.bollinger_bands import BollingerBands
from indicators.ma import MovingAverage
from indicators.atr import ATR

class BB_MA_ATR_RMI_Strategy(Strategy):
    """Trading strategy using Bollinger Bands, MA, ATR, and RSI."""
    
    def __init__(self):
        self.rsi = RSI(14)
        self.bb = BollingerBands(20, 2)
        self.ma = MovingAverage(50)
        self.atr = ATR(14)

       
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
    
        """Applies all indicators and generates buy/sell signals."""
    
        data = self.rsi.calculate(data)
        data = self.bb.calculate(data)
        data = self.ma.calculate(data)
        data = self.atr.calculate(data)
        
        # Generate Buy/Sell Signals
        data["signal"] = 0
        data.loc[(data["RSI"] < 30) & (data["Close"] < data["BB_Lower"]), "signal"] = 1  # Buy
        data.loc[(data["RSI"] > 70) & (data["Close"] > data["BB_Upper"]), "signal"] = -1  # Sell
   

        return data
