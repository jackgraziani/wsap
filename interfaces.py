#interfaces.py
#jack graziani
#creation date: Jul 31, 2026
# uses abstract class to define input/output for data structure rather than being committed to using a single API


from abc import ABC, abstractmethod
from schemas import StockFullAnalysis

class StockDataInterface(ABC):

    @abstractmethod
    def fetch_stock_data(self, ticker: str) -> StockFullAnalysis:
        """
        Fetch raw financial data given a ticker.
        map it to the StockFullAnalysis schema
        """
        pass