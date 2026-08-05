# backend.py
# Jack Graziani
# creation date: July 30, 2026
# Runs the logic of the back end

from yfinance_adapter import YFinanceAdapter
from screener import ScreenerEngine

def main():
    adapter = YFinanceAdapter()
    screener = ScreenerEngine()

    ticker = input("Enter a ticker (e.g., AAPL): ").strip().upper()
    print(".............")

    try:
        data = adapter.fetch_stock_data(ticker)
        results = screener.evaluate(data)

        print(results.summarize())


    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    main()


