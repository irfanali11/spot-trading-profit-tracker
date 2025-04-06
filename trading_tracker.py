# Spot Trading Tracker App with CSV, Summary, and ROI

import datetime
import csv
import os
from collections import defaultdict

TRADES_FILE = "trades.csv"

# Ensure CSV file exists with headers
def init_csv():
    if not os.path.exists(TRADES_FILE):
        with open(TRADES_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["date", "coin", "buy_price", "sell_price", "quantity", "profit", "roi"])

# Function to add a new trade
def add_trade(coin, buy_price, sell_price, quantity):
    trade_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    profit = (sell_price - buy_price) * quantity
    roi = (profit / (buy_price * quantity)) * 100
    trade = [trade_date, coin.upper(), buy_price, sell_price, quantity, round(profit, 2), round(roi, 2)]

    with open(TRADES_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(trade)
    print("\n✅ Trade added and saved to CSV successfully!\n")

# Function to load trades from CSV
def load_trades():
    trades = []
    if not os.path.exists(TRADES_FILE):
        return trades
    with open(TRADES_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            trades.append(row)
    return trades

# Function to show all trades
def show_trades(trades):
    if not trades:
        print("\nNo trades found.\n")
        return
    print("\n📜 Trade History:")
    for i, trade in enumerate(trades, 1):
        print(f"{i}. {trade['date']} | {trade['coin']} | Buy: ${trade['buy_price']} | Sell: ${trade['sell_price']} | Qty: {trade['quantity']} | Profit: ${trade['profit']} | ROI: {trade['roi']}%")

# Function to calculate total profit and monthly summary
def show_summary(trades):
    total_profit = 0.0
    monthly_summary = defaultdict(float)

    for trade in trades:
        profit = float(trade['profit'])
        date = datetime.datetime.strptime(trade['date'], "%Y-%m-%d %H:%M:%S")
        month_key = date.strftime("%Y-%m")
        total_profit += profit
        monthly_summary[month_key] += profit

    print("\n📈 Total Profit: $", round(total_profit, 2))
    print("\n🗓️ Monthly Summary:")
    for month, profit in sorted(monthly_summary.items()):
        print(f"{month}: ${round(profit, 2)}")

# Main loop
def run_trading_app():
    init_csv()
    print("\n📊 Spot Trading Profit Tracker 📊")
    while True:
        print("\nChoose an option:")
        print("1. Add New Trade")
        print("2. Show Trade History")
        print("3. Show Profit Summary")
        print("4. Exit")

        choice = input("Enter choice (1/2/3/4): ")

        trades = load_trades()

        if choice == '1':
            coin = input("Enter coin symbol (e.g., ETH): ")
            buy_price = float(input("Enter buy price ($): "))
            sell_price = float(input("Enter sell price ($): "))
            quantity = float(input("Enter quantity: "))
            add_trade(coin, buy_price, sell_price, quantity)
        elif choice == '2':
            show_trades(trades)
        elif choice == '3':
            show_summary(trades)
        elif choice == '4':
            print("\nGood luck and happy trading! 🚀")
            break
        else:
            print("\n❌ Invalid option. Try again.")

# Run the app
if __name__ == "__main__":
    run_trading_app()
