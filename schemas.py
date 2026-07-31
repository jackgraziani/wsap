# schemas.py
# Jack Graziani
# creation date: July 30, 2026
# Defining the type of data I want to pull from APIs

from dataclasses import dataclass
from typing import Optional

@dataclass
class StockHealth:
    st_assets: Optional[float]
    st_liabilities: Optional[float]
    lt_liabilities: Optional[float]
    total_debt_Tminus0: Optional[float]
    total_debt_Tminus1: Optional[float]
    total_debt_Tminus5: Optional[float]
    fcf: Optional[float]
    total_cash: Optional[float]
    ebit: Optional[float]
    interest_expense: Optional[float]

@dataclass
class StockValue:
    market_cap: Optional[float]
    net_income: Optional[float]
    p_e_ratio: Optional[float]
    p_s_ratio: Optional[float]
    current_price: Optional[float]
    avg_analyst_price_target: Optional[float]
    number_analysts: Optional[int]
    avg_analyst_price_target_Tminus90days: Optional[float]
    number_analysts_Tminus90days: Optional[int]

@dataclass
class StockGrowth:
    eps_3yr_growth_rate_forecast: Optional[float]
    revenue_3yr_growth_rate_forecast: Optional[float]
    roe_3yr_forecast: Optional[float]
    sp500_eps_3yr_growth_rate_forecast: Optional[float]
    sp500_revenue_3yr_growth_rate_forecast: Optional[float]
    _5yr_treasury_yield: Optional[float]

@dataclass
class StockFullAnalysis:
    ticker: str
    company_name: str
    sector: str
    health: StockHealth
    value: StockValue
    growth: StockGrowth
