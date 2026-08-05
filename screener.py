# screener.py
# Jack Graziani
# created on 8/5/26

# here is a description of the process
# belongs in documentation rather than this file but that's what it is for now
#===========================================
"""
----- (1) FINANCIAL HEALTH -----
SCREENER:
1a: short term assets > short term liabilities?
1b: short term assets > long term liabilities?
1c: currently debt free? (total debt)
1d: reducing debt over the past 5 years? (total debt)
1e: Positive FCF? Or, if not, 2 years of cash runway?
1f: Is EBIT atleast 3x interest payments?

GRANULAR FIN METRICS:
short term assets
short term liabilities
long term liabilities
totalDebtT-0
totalDebtT-1
totalDebtT-5
FCF
Total Cash
EBIT
Interest expense

CALCULATIONS: 
1a: -
1b: -
1c: -
1d: debtT-0 < debtT-5 AND debtT-0 <= debtT-1
1e: - OR total cash / abs(FCF) > 2
"""
#===========================================
"""
----- (2) VALUATION -----
SCREENER:
2a1: if profitable, is P/E < sector & market cap median P/E (HARDCODED)
2a2: if unprofitable, is P/S < sector & market cap median P/S (HARDCODED)
2b: is current price < analyst price target
2c: is current price significantly < analyst price target (20%+)
2d: does analyst price target have upward revision mommentum?

GRANULAR FIN METRICS:
market cap
sector
net income
p/e
p/s
current share price
analyst price target
number of analysts
analyst price target T-90 days
number of analyst (T-90)

CALCULATIONS:
2a1: -
2a2: -
2b: -
2c: -
2d: analyst price target > analyst price target T-90 days
"""
#===========================================
"""
----- (3) GROWTH -----
SCREENER:
3a: eps growth vs savings rate
3b: eps growth vs market eps growth
3c: revenue growth vs market revenue growth 
3d: ROE 3 year forecast > 20%

GRANULAR FIN METRICS:
forward eps 3 year growth forecast
forward revenue 3 year growth forecast
forward roe 3 year forecast
forward s&p 500 eps 3 year growth forecast
forward s&p 500 revenue 3 year growth forecast
5 year treausry yield

CALCULATIONS:
3a: forward eps 3 year growth forecast > 5 year treasury yield
3b: forward eps 3 year growth forecast > forward s&p 500 eps 3 year growth forecast
3c: forward revenue 3 year growth forecast > forward s&p 500 revenue 3 year growth forecast
3d: -
"""
#===========================================

from dataclasses import dataclass
from typing import Optional, Dict
from schemas import StockFullAnalysis

# HARDCODED SECTOR AND MARKET CAP
# P/E & P/S MEDIAN VALUES 
# ** ESTIMATED WITH AI **
# may follow up on deeper research in the future

# screener.py

SECTOR_PE_MEDIANS = {
    "Energy": {"small": 10.5, "medium": 11.5, "large": 12.5},
    "Basic Materials": {"small": 13.0, "medium": 15.0, "large": 17.5},
    "Industrials": {"small": 16.5, "medium": 19.5, "large": 22.0},
    "Utilities": {"small": 14.0, "medium": 16.5, "large": 18.5},
    "Healthcare": {"small": 17.0, "medium": 21.0, "large": 24.5},
    "Financial Services": {"small": 10.0, "medium": 12.0, "large": 14.0},
    "Consumer Cyclical": {"small": 15.0, "medium": 18.5, "large": 23.0},
    "Consumer Defensive": {"small": 17.5, "medium": 20.0, "large": 22.5},
    "Technology": {"small": 20.0, "medium": 25.0, "large": 30.0},
    "Communication Services": {"small": 14.0, "medium": 18.0, "large": 22.0},
    "Real Estate": {"small": 28.0, "medium": 33.0, "large": 38.0},
}

SECTOR_PS_MEDIANS = {
    "Energy": {"small": 0.9, "medium": 1.2, "large": 1.5},
    "Basic Materials": {"small": 1.0, "medium": 1.3, "large": 1.7},
    "Industrials": {"small": 1.1, "medium": 1.5, "large": 2.0},
    "Utilities": {"small": 1.5, "medium": 2.0, "large": 2.4},
    "Healthcare": {"small": 2.0, "medium": 3.5, "large": 4.8},
    "Financial Services": {"small": 1.2, "medium": 1.8, "large": 2.5},
    "Consumer Cyclical": {"small": 0.8, "medium": 1.3, "large": 1.9},
    "Consumer Defensive": {"small": 0.9, "medium": 1.4, "large": 1.8},
    "Technology": {"small": 2.5, "medium": 4.5, "large": 6.5},
    "Communication Services": {"small": 1.2, "medium": 2.0, "large": 3.0},
    "Real Estate": {"small": 3.0, "medium": 4.5, "large": 6.0},
}

# Standard fallbacks for unmapped sectors
DEFAULT_PE = {"small": 15.0, "medium": 18.0, "large": 22.0}
DEFAULT_PS = {"small": 1.2, "medium": 2.0, "large": 3.0}




def get_market_cap_tier(market_cap: Optional[float]) -> str:
    if market_cap is None:
        return "medium"  # default fallback
    if market_cap < 2_000_000_000:
        return "small"
    elif market_cap <= 10_000_000_000:
        return "medium"
    else:
        return "large"


def get_median_pe(sector: str, market_cap: Optional[float]) -> float:
    tier = get_market_cap_tier(market_cap)
    sector_dict = SECTOR_PE_MEDIANS.get(sector, DEFAULT_PE)
    return sector_dict.get(tier, DEFAULT_PE[tier])


def get_median_ps(sector: str, market_cap: Optional[float]) -> float:
    tier = get_market_cap_tier(market_cap)
    sector_dict = SECTOR_PS_MEDIANS.get(sector, DEFAULT_PS)
    return sector_dict.get(tier, DEFAULT_PS[tier])

"""
SCREENER:
1a: short term assets > short term liabilities?
1b: short term assets > long term liabilities?
1c: currently debt free? (total debt)
1d: reducing debt over the past 5 years? (total debt)
1e: Positive FCF? Or, if not, 2 years of cash runway?
1f: Is EBIT atleast 3x interest payments?
"""

@dataclass
class HealthResults:
    r1a_st_assets_vs_liabilities: Optional[bool]
    r1b_st_assets_vs_lt_liabilities: Optional[bool]
    r1c_is_debt_free: Optional[bool]
    r1d_reducing_debt_5yr: Optional[bool]
    r1e_fcf_or_runway: Optional[bool]
    r1f_ebit_coverage: Optional[bool]

"""
SCREENER:
2a1: if profitable, is P/E < sector & market cap median P/E (HARDCODED)
2a2: if unprofitable, is P/S < sector & market cap median P/S (HARDCODED)
2b: is current price < analyst price target
2c: is current price significantly < analyst price target (20%+)
2d: does analyst price target have upward revision mommentum?
"""
@dataclass
class ValuationResults:
    r2a1_pe_vs_sector_median: Optional[bool]
    r2a2_ps_vs_sector_median: Optional[bool]
    r2b_price_below_target: Optional[bool]
    r2c_price_significantly_below_target: Optional[bool]
    r2d_target_upward_momentum: Optional[bool]

"""
SCREENER:
3a: eps growth vs savings rate
3b: eps growth vs market eps growth
3c: revenue growth vs market revenue growth 
3d: ROE 3 year forecast > 20%
"""
@dataclass
class GrowthResults:
    r3a_eps_vs_treasury_yield: Optional[bool]
    r3b_eps_vs_sp500_eps: Optional[bool]
    r3c_rev_vs_sp500_rev: Optional[bool]
    r3d_roe_forecast_over_20: Optional[bool]

@dataclass
class ScreenerResults:
    ticker: str
    health: HealthResults
    valuation: ValuationResults
    growth: GrowthResults


class ScreenerEngine:
    def evaluate(self, analysis: StockFullAnalysis) -> ScreenerResults:
            return ScreenerResults(
                ticker=analysis.ticker,
                health=self._eval_health(analysis.health),
                valuation=self._eval_valuation(analysis.value, analysis.sector),
                growth=self._eval_growth(analysis.growth)
            )

    def _eval_health(self, h) -> HealthResults:
        # 1a: ST Assets > ST Liabilities
        r1a = (h.st_assets > h.st_liabilities) if (h.st_assets is not None and h.st_liabilities is not None) else None
        
        # 1b: ST Assets > LT Liabilities
        r1b = (h.st_assets > h.lt_liabilities) if (h.st_assets is not None and h.lt_liabilities is not None) else None
        
        # 1c: Currently debt free
        r1c = (h.total_debt_Tminus0 == 0) if h.total_debt_Tminus0 is not None else None
        
        # 1d: debtT-0 < debtT-5 AND debtT-0 <= debtT-1
        r1d = None
        if all(x is not None for x in [h.total_debt_Tminus0, h.total_debt_Tminus1, h.total_debt_Tminus5]):
            r1d = (h.total_debt_Tminus0 < h.total_debt_Tminus5) and (h.total_debt_Tminus0 <= h.total_debt_Tminus1)

        # 1e: Positive FCF? Or total cash / abs(FCF) > 2
        r1e = None
        if h.fcf is not None:
            if h.fcf > 0:
                r1e = True
            elif h.total_cash is not None and h.fcf != 0:
                r1e = (h.total_cash / abs(h.fcf)) > 2.0

        # 1f: EBIT at least 3x Interest Expense
        r1f = None
        if h.ebit is not None and h.interest_expense is not None and h.interest_expense != 0:
            r1f = (h.ebit / abs(h.interest_expense)) >= 3.0

        return HealthResults(r1a, r1b, r1c, r1d, r1e, r1f)

    def _eval_valuation(self, v, sector: str) -> ValuationResults:
            # Dynamically fetch sector + tier median multiples
            target_pe = get_median_pe(sector, v.market_cap)
            target_ps = get_median_ps(sector, v.market_cap)
            
            is_profitable = (v.net_income > 0) if v.net_income is not None else None

            # 2a1: If profitable, P/E < sector & market cap median
            r2a1 = (v.p_e_ratio < target_pe) if (is_profitable is True and v.p_e_ratio is not None) else None

            # 2a2: If unprofitable, P/S < sector & market cap median
            r2a2 = (v.p_s_ratio < target_ps) if (is_profitable is False and v.p_s_ratio is not None) else None

            # 2b: Price < analyst price target
            r2b = (v.current_price < v.avg_analyst_price_target) if (v.current_price is not None and v.avg_analyst_price_target is not None) else None

            # 2c: Price < 80% of analyst target (20%+ upside)
            r2c = (v.current_price < (v.avg_analyst_price_target * 0.80)) if (v.current_price is not None and v.avg_analyst_price_target is not None) else None

            # 2d: Price target upward momentum
            r2d = (v.avg_analyst_price_target > v.avg_analyst_price_target_Tminus90days) if (v.avg_analyst_price_target is not None and v.avg_analyst_price_target_Tminus90days is not None) else None

            return ValuationResults(r2a1, r2a2, r2b, r2c, r2d)

    def _eval_growth(self, g) -> GrowthResults:
        # 3a: EPS forecast > 5-year treasury yield
        r3a = (g.eps_3yr_growth_rate_forecast > g._5yr_treasury_yield) if (g.eps_3yr_growth_rate_forecast is not None and g._5yr_treasury_yield is not None) else None

        # 3b: EPS forecast > S&P 500 EPS forecast
        r3b = (g.eps_3yr_growth_rate_forecast > g.sp500_eps_3yr_growth_rate_forecast) if (g.eps_3yr_growth_rate_forecast is not None and g.sp500_eps_3yr_growth_rate_forecast is not None) else None

        # 3c: Revenue forecast > S&P 500 revenue forecast
        r3c = (g.revenue_3yr_growth_rate_forecast > g.sp500_revenue_3yr_growth_rate_forecast) if (g.revenue_3yr_growth_rate_forecast is not None and g.sp500_revenue_3yr_growth_rate_forecast is not None) else None

        # 3d: ROE forecast > 20% (0.20)
        r3d = (g.roe_3yr_forecast > 0.20) if g.roe_3yr_forecast is not None else None

        return GrowthResults(r3a, r3b, r3c, r3d)


@dataclass
class ScreenerResults:
    ticker: str
    health: HealthResults
    valuation: ValuationResults
    growth: GrowthResults

    def summarize(self) -> dict:
        """Returns passed/evaluated counts for each category and overall score."""
        def count_score(dc):
            vals = [v for v in dc.__dict__.values() if v is not None]
            passed = sum(1 for v in vals if v is True)
            return passed, len(vals)

        h_pass, h_total = count_score(self.health)
        v_pass, v_total = count_score(self.valuation)
        g_pass, g_total = count_score(self.growth)

        total_pass = h_pass + v_pass + g_pass
        total_eval = h_total + v_total + g_total

        return {
            "ticker": self.ticker,
            "health_score": f"{h_pass}/{h_total}",
            "valuation_score": f"{v_pass}/{v_total}",
            "growth_score": f"{g_pass}/{g_total}",
            "total_score": f"{total_pass}/{total_eval}",
            "pass_rate": round((total_pass / total_eval) * 100, 1) if total_eval > 0 else 0.0
        }