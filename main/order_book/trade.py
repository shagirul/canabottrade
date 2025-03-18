
from datetime import datetime
from typing import Optional

class Trade:
    """Represents a single trade (entry to exit)."""
    
    def __init__(self, trade_id: str, symbol: str, side: str, quantity: float, entry_price: float, sl: Optional[float] = None, tp: Optional[float] = None, entry_time: Optional[datetime] = None):
        self.trade_id = trade_id  # Unique trade ID
        self.symbol = symbol      # Ticker (e.g., BTC/USD)
        self.side = side          # Buy/Sell
        self.quantity = quantity  # Order quantity
        self.entry_price = entry_price  # Initial price
        self.sl = sl              # Stop Loss
        self.tp = tp              # Take Profit
        self.entry_time = entry_time if entry_time is not None else datetime.now()  # Entry timestamp
        self.exit_price: Optional[float] = None  # Set when closed
        self.exit_time: Optional[datetime] = None  # Exit timestamp
        self.pnl: Optional[float] = None  # Profit/Loss

    def close_trade(self, exit_price: float, exit_time: Optional[datetime] = None):
        """Closes the trade and calculates profit/loss."""
        self.exit_price = exit_price
        self.exit_time = exit_time if exit_time is not None else datetime.now()  # Set exit time to now if not given
        self.pnl = (exit_price - self.entry_price) * self.quantity if self.side == "BUY" else (self.entry_price - exit_price) * self.quantity
