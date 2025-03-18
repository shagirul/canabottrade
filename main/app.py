import pandas as pd
import matplotlib.pyplot as plt
from data_feed.csv_data_feed import CSVDataFeed
from executor.strategy_executor import StrategyExecutor
from strategies.bb_ma_atr_rmi_strategy import BB_MA_ATR_RMI_Strategy

START_DATE = "2022-01-01 00:00:00"
END_DATE = "2022-01-5 00:00:00"



csv_path = "../resource/minuteBitcoinData.csv"



# Updated constants
START_DATE = "2022-03-18 00:00:00"
END_DATE = "2022-03-19 00:00:00"

def plot_price_with_signals(df, transactions):
    """Plot close price with buy/sell signals."""
    # Convert price data timestamps
    df["Date"] = pd.to_datetime(df["Date"], format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')
    
    # Print price data date range
    print("Price Data Date Range:")
    print("Start:", df["Date"].min())
    print("End:", df["Date"].max())

    # Process transactions
    transactions = transactions.copy()
    for col in ["entry_time", "exit_time"]:
        transactions[col] = pd.to_datetime(
            transactions[col], 
            format='%Y-%m-%d %H:%M:%S.%f', 
            errors='coerce'
        )

    # Print transaction date range
    print("Transaction Date Range:")
    print("Start:", transactions["entry_time"].min())
    print("End:", transactions["exit_time"].max())

    # Filter closed trades within date range
    closed_trades = transactions.loc[
        (transactions["status"] == "CLOSED") &
        (transactions["entry_time"] >= df["Date"].min()) &
        (transactions["exit_time"] <= df["Date"].max())
    ].copy()

    if closed_trades.empty:
        print("No closed trades to plot")
        return

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Close"], label="Close Price", color="blue", alpha=0.6)
    plt.scatter(closed_trades["entry_time"], closed_trades["entry_price"], 
                color="green", marker="^", s=150, label="Entry")
    plt.scatter(closed_trades["exit_time"], closed_trades["exit_price"],
                color="red", marker="v", s=150, label="Exit")
    plt.legend()
    plt.show()









# Load data
data_feed = CSVDataFeed(csv_path)
data = data_feed.fetch_data(symbol="BTCUSD", start_date=START_DATE, end_date=END_DATE, timeframe="1min")

# Run strategy
strategy = BB_MA_ATR_RMI_Strategy()
executor = StrategyExecutor(strategy)

executor.run_backtest(data, symbol="BTCUSD")
df = pd.read_csv("total_Trade.csv")
plot_price_with_signals(data,df)

