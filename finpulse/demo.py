"""Mock data for --demo mode."""

DEMO_HOLDINGS = [
    {"ticker": "AAPL",    "name": "Apple Inc.",          "type": "stock",  "shares": 15,   "avg_buy_price": 155.00, "current_price": 211.45, "cost_basis": 2325.00, "current_value": 3171.75, "pnl": 846.75,  "pnl_pct": 36.42,  "change_1d": 1.23,  "change_1d_pct": 0.59,  "change_1w_pct": 2.1,   "change_1m_pct": 8.4,  "currency": "USD", "allocation_pct": 21.3, "error": False},
    {"ticker": "MSFT",    "name": "Microsoft Corp.",     "type": "stock",  "shares": 8,    "avg_buy_price": 380.00, "current_price": 425.20, "cost_basis": 3040.00, "current_value": 3401.60, "pnl": 361.60,  "pnl_pct": 11.89,  "change_1d": -2.10, "change_1d_pct": -0.49, "change_1w_pct": -1.2,  "change_1m_pct": 4.1,  "currency": "USD", "allocation_pct": 22.8, "error": False},
    {"ticker": "NVDA",    "name": "NVIDIA Corp.",        "type": "stock",  "shares": 5,    "avg_buy_price": 620.00, "current_price": 950.40, "cost_basis": 3100.00, "current_value": 4752.00, "pnl": 1652.00, "pnl_pct": 53.29,  "change_1d": 18.50, "change_1d_pct": 1.99,  "change_1w_pct": 6.8,   "change_1m_pct": 22.3, "currency": "USD", "allocation_pct": 31.9, "error": False},
    {"ticker": "GOOGL",   "name": "Alphabet Inc.",       "type": "stock",  "shares": 10,   "avg_buy_price": 145.00, "current_price": 178.90, "cost_basis": 1450.00, "current_value": 1789.00, "pnl": 339.00,  "pnl_pct": 23.38,  "change_1d": 0.85,  "change_1d_pct": 0.48,  "change_1w_pct": 1.4,   "change_1m_pct": 5.9,  "currency": "USD", "allocation_pct": 12.0, "error": False},
    {"ticker": "BTC-USD", "name": "Bitcoin",             "type": "crypto", "shares": 0.25, "avg_buy_price": 52000,  "current_price": 67840,  "cost_basis": 13000.0, "current_value": 16960.0, "pnl": 3960.0,  "pnl_pct": 30.46,  "change_1d": 840.0, "change_1d_pct": 1.25,  "change_1w_pct": 4.2,   "change_1m_pct": 18.7, "currency": "USD", "allocation_pct": 0.0,  "error": False},
    {"ticker": "ETH-USD", "name": "Ethereum",            "type": "crypto", "shares": 2,    "avg_buy_price": 3200,   "current_price": 3540,   "cost_basis": 6400.0,  "current_value": 7080.0,  "pnl": 680.0,   "pnl_pct": 10.63,  "change_1d": -45.0, "change_1d_pct": -1.25, "change_1w_pct": -2.1,  "change_1m_pct": 9.4,  "currency": "USD", "allocation_pct": 0.0,  "error": False},
    {"ticker": "AMZN",    "name": "Amazon.com Inc.",     "type": "stock",  "shares": 6,    "avg_buy_price": 185.00, "current_price": 198.40, "cost_basis": 1110.00, "current_value": 1190.40, "pnl": 80.40,   "pnl_pct": 7.24,   "change_1d": -1.20, "change_1d_pct": -0.60, "change_1w_pct": -0.8,  "change_1m_pct": 3.2,  "currency": "USD", "allocation_pct": 0.0,  "error": False},
]

# Fix allocations
total = sum(h["current_value"] for h in DEMO_HOLDINGS)
for h in DEMO_HOLDINGS:
    h["allocation_pct"] = round(h["current_value"] / total * 100, 1)

DEMO_MARKET = {
    "S&P 500":  {"price": 5308.15, "change_pct": 0.48},
    "NASDAQ":   {"price": 16780.2, "change_pct": 0.72},
    "Gold":     {"price": 2340.10, "change_pct": -0.21},
    "Bitcoin":  {"price": 67840.0, "change_pct": 1.25},
    "Ethereum": {"price": 3540.00, "change_pct": -1.25},
}

DEMO_AI_TEXT = (
    "Your portfolio is performing strongly, up 30.5% overall driven by NVIDIA's "
    "exceptional 53% gain and Apple's solid 36% return. The tech-heavy allocation "
    "has paid off in the current AI-driven market rally, with NVDA alone accounting "
    "for nearly a third of your total value. The main risk to watch is concentration — "
    "over 75% of your portfolio sits in three positions (NVDA, MSFT, AAPL), which "
    "leaves you exposed to any sector-wide tech correction."
)
