#yfinance_adapter
# Jack Graziani
# created on Jul 31, 2026
# DESCRIPTION

import math
import yfinance as yf
from typing import Any, Optional

from interfaces import StockDataInterface
from schemas import StockFullAnalysis, StockValue, StockHealth, StockGrowth

class YFinanceAdapter(StockDataInterface):

    def convert_float_or_none(self, value: Any) -> Optional[float]:
        """Converts numbers/NaNs to floats or type None"""

        # if value is None return None
        if value is None:
            return None

        # try converting to float
        try:
            val = float(value)
            # if it's NaN (missing), return None
            if math.isnan(val):
                return None
            # otherwise, you can return a float-converted value
            else:
                return val
        # if you run into value or type errors, return none
        except (ValueError, TypeError):
            return None

    def extract_df(self, df, row_label: str, col_index: int) -> Optional[float]:
        """extract cell value from pandas DF"""
        # if the data from is none/empty, return None (no cell vals)
        if df is None or df.empty:
            return None

        # if we have the appropiate row label
        # and the column is in bounds of the df
        if row_label in df.index and len(df.columns) > col_index:
            # return the value of the cell
            return self.convert_float_or_none(df.loc[row_label].iloc[col_index])

        # if we don't meet those conditions, return None.
        return None

    def fetch_stock_data(self, ticker) -> StockFullAnalysis:

        # get the stock from yfinance
        stock = yf.Ticker(ticker)

        info = stock.info or {}

        try:
            bs = stock.balance_sheet
        except Exception:
            bs = None

        try:
            fin = stock.financials
        except Exception:
            fin = None

        try:
            cf = stock.cashflow
        except Exception:
            cf = None

        # extract health data
        health = StockHealth(
            st_assets = self.extract_df(bs, "Current Assets", 0),
            st_liabilities = self.extract_df(bs, "Current Liabilities", 0),
            lt_liabilities = self.extract_df(bs, "Total Non Current Liabilities Net Minority Interest", 0),
            total_debt_Tminus0 = self.extract_df(bs, "Total Debt", 0),
            total_debt_Tminus1 = self.extract_df(bs, "Total Debt", 1),
            total_debt_Tminus5 = self.extract_df(bs, "Total Debt", 5),
            fcf = self.extract_df(cf, "Free Cash Flow", 0),
            total_cash = self.extract_df(bs, "Cash Cash Equivalents And Short Term Investments", 0),
            ebit = self.extract_df(fin, "EBIT", 0),
            interest_expense = self._safe_df_extract(fin, "Interest Expense", 0),
        )

        # extract value data
        analyst_targets = getattr(stock, "analyst_price_targets", {}) or {}

        value = StockValue(
            market_cap = self.convert_float_or_none(info.get("marketCap")),
            net_income = self.extract_df(fin, "Net Income Common Stockholders", 0),
            p_e_ratio = self.convert_float_or_none(info.get("trailingPE")),
            p_s_ratio = self.convert_float_or_none(info.get("priceToSalesTrailing12Months")),
            current_price = self.convert_float_or_none(info.get("currentPrice") or info.get("regularMarketPrice")),
            avg_analyst_price_target = self.convert_float_or_none(analyst_targets.get("mean") or info.get("targetMeanPrice")),
            number_analysts = info.get("numberOfAnalystOpinions"),
            #NOT PROVIDED BY YFINANCE:
            avg_analyst_price_target_Tminus90days = None,
            number_analysts_Tminus90days = None
        )

        # extract growth data

        # Pull 5-Year Treasury Yield macro data directly using symbol ^FVX
        treasury_yield = None
        try:
            fv_ticker = yf.Ticker("^FVX")
            treasury_yield = self._safe_float(
                fv_ticker.info.get("regularMarketPrice")
            )
        except Exception:
            pass

        growth = StockGrowth(
            eps_3yr_growth_rate_forecast = None,  # Missing on free yfinance, defaulted to None
            revenue_3yr_growth_rate_forecast = None,
            roe_3yr_forecast = None,
            sp500_eps_3yr_growth_rate_forecast = None,
            sp500_revenue_3yr_growth_rate_forecast = None,
            _5yr_treasury_yield = treasury_yield,
        )

