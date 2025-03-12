import math
import pandas as pd
import talib
from datetime import datetime
import csv
import matplotlib.pyplot as plt

# ✅ Define constants
CSV_PATH = "../resource/minuteBitcoinData.csv"
START_DATE = "2022-01-01 00:00:00"
END_DATE = "2022-01-06 00:00:00"
START_CAPITAL = 10000000  # Set your starting capital
MACD_BUFFER = 35  # Ignore the first 35 rows for trading
TRANSACTION_CSV = "trade_transactions.csv"


import math

class TradingStrategy:
    def __init__(self, start_capital):
        """Initialize with starting capital."""
        self.capital = start_capital
        self.number_of_stocks = 0
        self.last_buy_price = None  # Track last buy price to prevent redundant buys
        

    def buy_all(self, stock_price, date):
        """Buy as many stocks as possible with current capital."""
        if stock_price <= 0:
            print(f"⚠️ [BUY ERROR] {date} | Invalid stock price: ${stock_price:.2f}")
            return

        if self.capital < stock_price:
            print(f"⚠️ [BUY ERROR] {date} | Not enough balance to buy. Capital: ${self.capital:.2f}")
            return
        
        count = math.floor(self.capital / stock_price)
        if count > 0:
            self.capital -= stock_price * count
            self.number_of_stocks += count
            self.last_buy_price = stock_price  # Track last buy price

            # Calculate profit percentage
            profit_percentage = ((self.capital - START_CAPITAL) / START_CAPITAL) * 100
            print(f"🟢 [BUY] {date} | Price: ${stock_price:.2f} | Stocks: {count} | Capital: ${self.capital:.2f} | Profit: {profit_percentage:.2f}%")
        else:
            print(f"⚠️ [BUY ERROR] {date} | Unable to buy any stocks. Capital: ${self.capital:.2f}")

    def sell_all(self, stock_price, date):
        """Sell all owned stocks."""
        if stock_price <= 0:
            print(f"⚠️ [SELL ERROR] {date} | Invalid stock price: ${stock_price:.2f}")
            return

        if self.number_of_stocks == 0:
            print(f"⚠️ [SELL ERROR] {date} | No stocks to sell.")
            return

        self.capital += stock_price * self.number_of_stocks
        self.number_of_stocks = 0

        # Calculate profit percentage
        profit_percentage = ((self.capital - START_CAPITAL) / START_CAPITAL) * 100
        print(f"🔴 [SELL] {date} | Price: ${stock_price:.2f} | Capital: ${self.capital:.2f} | Profit: {profit_percentage:.2f}%")




def load_and_preprocess_data(csv_path):
    """Load CSV, convert Date column, and clean Close prices."""
    try:
        df = pd.read_csv(csv_path)
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        df['Close'] = df['Close'].astype(str).str.replace(',', '').astype(float)
        return df
    except FileNotFoundError:
        print(f"❌ File not found: {csv_path}")
        exit(1)
    except pd.errors.EmptyDataError:
        print(f"❌ No data in file: {csv_path}")
        exit(1)
    except pd.errors.ParserError:
        print(f"❌ Error parsing file: {csv_path}")
        exit(1)


def filter_data_by_date(df, start_date, end_date):
    """Filter data within a given date range."""
    start_dt = pd.to_datetime(start_date, format='%Y-%m-%d %H:%M:%S', errors='coerce')
    end_dt = pd.to_datetime(end_date, format='%Y-%m-%d %H:%M:%S', errors='coerce')

    if start_dt > end_dt:
        print("❌ Error: Start date cannot be after end date.")
        exit(1)

    df = df.sort_values(by='Date', ascending=True)
    return df[(df['Date'] >= start_dt) & (df['Date'] <= end_dt)].copy()


def calculate_macd(df):
    """Calculate MACD and add it to the DataFrame."""
    macd, signal, hist = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['MACD'], df['Signal'], df['Histogram'] = macd, signal, hist

    # ✅ Drop NaN values before simulation
    df = df.dropna(subset=['MACD', 'Signal']).reset_index(drop=True)
    return df


def simulate_trading_strategy(df):
    """Simulate trading using MACD strategy, skipping the first 35 rows and logging transactions."""
    
    if len(df) <= MACD_BUFFER:
        print("⚠️ Not enough data for trading after MACD_BUFFER. Exiting.")
        exit(1)

    trader = TradingStrategy(START_CAPITAL)
    df = df.iloc[MACD_BUFFER:].reset_index(drop=True)  # Skip the first 35 rows



    with open(TRANSACTION_CSV, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Type", "Price", "Stocks", "Capital", "Profit"])  # Header

        for _, row in df.iterrows():
            macd = round(row["MACD"], 2)
            signal = round(row["Signal"], 2)
            price = row["Close"]
            date = row["Date"]

            if macd == signal and macd < 0:  # Buy condition
                stocks_bought = math.floor(trader.capital / price)
                if stocks_bought > 0:
                    trader.capital -= price * stocks_bought
                    trader.number_of_stocks += stocks_bought
                    writer.writerow([date, "BUY", price, stocks_bought, trader.capital, trader.capital - START_CAPITAL])

            elif macd == signal and macd > 0:  # Sell condition
                if trader.number_of_stocks > 0:
                    trader.capital += price * trader.number_of_stocks
                    writer.writerow([date, "SELL", price, trader.number_of_stocks, trader.capital, trader.capital - START_CAPITAL])
                    trader.number_of_stocks = 0  # Reset after selling

        # Final sell at last data point
        if trader.number_of_stocks > 0:
            final_price = df.iloc[-1]["Close"]
            trader.capital += final_price * trader.number_of_stocks
            writer.writerow([df.iloc[-1]["Date"], "FINAL_SELL", final_price, trader.number_of_stocks, trader.capital, trader.capital - START_CAPITAL])

    return trader.capital



def save_to_csv(df, output_csv="Transactions.csv"):
    """Save DataFrame to CSV file."""
    df.to_csv(output_csv, index=False)
    print(f"✅ CSV file saved: {output_csv}")
    


def plot_price_with_signals(df, transaction_csv):
    """Plot close price and overlay buy/sell signals from transactions."""
    # Load transactions
    transactions = pd.read_csv(transaction_csv)
    transactions["Date"] = pd.to_datetime(transactions["Date"])
    
    # Filter buy and sell signals
    buys = transactions[transactions["Type"] == "BUY"]
    sells = transactions[transactions["Type"].str.contains("SELL")]

    # Plot close price
    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Close"], label="Close Price", color="blue", alpha=0.6)

    # Plot buy signals (green markers)
    plt.scatter(buys["Date"], buys["Price"], marker="^", color="green", label="Buy Signal", alpha=1, edgecolors="black")

    # Plot sell signals (red markers)
    plt.scatter(sells["Date"], sells["Price"], marker="v", color="red", label="Sell Signal", alpha=1, edgecolors="black")

    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.title("Close Price with Buy/Sell Signals")
    plt.legend()
    plt.grid()
    plt.show()



def main():
    df = load_and_preprocess_data(CSV_PATH)
    filtered_df = filter_data_by_date(df, START_DATE, END_DATE)
    filtered_df = calculate_macd(filtered_df)

    if filtered_df.empty:
        print("⚠️ No valid data available for trading after MACD calculation. Exiting.")
        exit(1)


    final_capital = simulate_trading_strategy(filtered_df)
    profit = final_capital - START_CAPITAL
    profit_percentage = (profit / START_CAPITAL) * 100
    print(f"\n📈 Final Capital: ${final_capital:.2f} | Profit: ${profit:.2f} ({profit_percentage:.2f}%)")
    plot_price_with_signals(filtered_df, TRANSACTION_CSV)


if __name__ == "__main__":
    main()
