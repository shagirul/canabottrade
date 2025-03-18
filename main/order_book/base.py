from abc import ABC, abstractmethod
import pandas as pd
from typing import List

class IOrderBook(ABC):
    """Defines the interface for an Order Book system."""

    @abstractmethod
    def place_order(self, symbol: str, side: str, quantity: float, entry_price: float, sl: float, tp: float):
        """Places a new order in the system."""
        pass

    @abstractmethod
    def close_order(self, trade_id: str, exit_price: float):
        """Closes an existing order and calculates P&L."""
        pass

    @abstractmethod
    def get_open_trades(self) -> pd.DataFrame:
        """Returns all currently active trades."""
        pass

    @abstractmethod
    def get_trade_history(self) -> pd.DataFrame:
        """Returns all completed trades."""
        pass
