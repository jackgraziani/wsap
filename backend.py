# backend.py
# Jack Graziani
# creation date: July 30, 2026
# Runs the logic of the back end

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