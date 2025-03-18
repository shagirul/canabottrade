import pandas as pd
import uuid
import csv
from typing import Dict, Optional
from order_book.base import IOrderBook
from .trade import Trade
from datetime import datetime

class OrderBook(IOrderBook):
    """Manages open trades and trade history."""

    def __init__(self, csv_filename="total_Trade.csv"):
        self.open_trades: Dict[str, Trade] = {}  # Active trades (trade_id -> Trade)
        self.trade_history: Dict[str, Trade] = {}  # Completed trades
        self.csv_filename = csv_filename
        self._initialize_csv()

    def _initialize_csv(self):
        """Creates CSV file with headers if it does not exist."""
        try:
            with open(self.csv_filename, "x", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "trade_id", "entry_time", "symbol", "side", "quantity", "entry_price",
                    "exit_price", "exit_time", "sl", "tp", "pnl", "status"
                ])
        except FileExistsError:
            pass  # File already exists, no need to reinitialize

    def place_order(self, symbol: str, side: str, quantity: float, entry_price: float, sl: float, tp: float, entry_time: Optional[datetime] = None):
        """Places a new order in the system and logs it."""
        trade_id = str(uuid.uuid4())  # Unique trade ID
        trade = Trade(trade_id, symbol, side, quantity, entry_price, sl, tp, entry_time)
        self.open_trades[trade_id] = trade

        # Log trade to CSV with "OPEN" status
        self._log_trade_to_csv(trade, status="OPEN")

    def close_order(self, trade_id: str, exit_price: float, exit_time: Optional[datetime] = None):
        """Closes an existing trade and updates the CSV."""
        if trade_id not in self.open_trades:
            print(f"❌ Trade ID {trade_id} not found!")
            return
        
        trade = self.open_trades.pop(trade_id)  # Remove from open trades
        trade.close_trade(exit_price, exit_time)  # Finalize trade details
        self.trade_history[trade_id] = trade  # Move to trade history

        # Update CSV with "CLOSED" status
        self._log_trade_to_csv(trade, status="CLOSED")

    def _log_trade_to_csv(self, trade: Trade, status: str):
        """Logs trade data into CSV file."""
        with open(self.csv_filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                trade.trade_id,
                trade.entry_time.strftime('%Y-%m-%d %H:%M:%S.%f'),  # Format entry_time for CSV
                trade.symbol,
                trade.side,
                trade.quantity,
                trade.entry_price,
                trade.exit_price if trade.exit_price else "",
                trade.exit_time.strftime('%Y-%m-%d %H:%M:%S.%f') if trade.exit_time else "", 
                trade.sl,
                trade.tp,
                trade.pnl if trade.pnl else "",
                status
            ])

    def get_open_trades(self) -> pd.DataFrame:
        """Returns all currently open trades as a DataFrame."""
        return pd.DataFrame([vars(trade) for trade in self.open_trades.values()])

    def get_trade_history(self) -> pd.DataFrame:
        """Returns trade history as a DataFrame."""
        return pd.DataFrame([vars(trade) for trade in self.trade_history.values()])
