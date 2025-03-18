import pandas as pd
from order_book.orderbook import OrderBook

class StrategyExecutor:
    """Executes strategy and simulates trades."""
    
    def __init__(self, strategy):
        self.strategy = strategy
        self.order_book = OrderBook()

    def run_backtest(self, data: pd.DataFrame, symbol: str):
        """Executes the strategy on historical data."""
        data = self.strategy.generate_signals(data)

        for index, row in data.iterrows():
            print("entry_time=", row["Date"])
            print( "exit_time=",row["Date"])
            if row["signal"] == 1:  # Buy
                # Place order with entry_time from the data
                self.order_book.place_order(
                    symbol=symbol,
                    side="BUY",
                    quantity=1,
                    entry_price=row["Close"],
                    sl=row["Close"] * 0.95,
                    tp=row["Close"] * 1.05,
                    entry_time=row["Date"]  # Pass entry time from the DataFrame
                )
            elif row["signal"] == -1:  # Sell
                open_trades = self.order_book.get_open_trades()
                if not open_trades.empty:
                    trade_id = open_trades.iloc[0]["trade_id"]
                    # Close order with exit_time from the data
                    self.order_book.close_order(
                        trade_id=trade_id,
                        exit_price=row["Close"],
                        exit_time=row["Date"]  # Pass exit time from the DataFrame
                    )

        print("📊 Backtest Complete!")
