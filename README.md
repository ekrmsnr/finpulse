# 💰 finpulse

> Real-time portfolio analyzer with AI-powered insights. Tracks stocks and crypto, shows P&L, and generates a beautiful report — powered by Claude AI.

```bash
pip install finpulse
finpulse portfolio.csv
```

---

## Quick start

**1. Try it instantly (no setup needed):**
```bash
pip install finpulse
finpulse --demo
```

**2. Analyze your own portfolio:**

Create a `portfolio.csv`:
```csv
ticker,shares,avg_buy_price
AAPL,15,155.00
MSFT,8,380.00
NVDA,5,620.00
BTC-USD,0.25,52000.00
ETH-USD,2,3200.00
```

Then run:
```bash
finpulse portfolio.csv
```

**3. Enable AI analysis (optional but highly recommended):**

Get a free API key at **[console.anthropic.com](https://console.anthropic.com)** → sign up → API Keys → Create Key.

```bash
# Option A: pass directly
finpulse portfolio.csv --api-key sk-ant-...

# Option B: set once, use forever (recommended)
export ANTHROPIC_API_KEY=sk-ant-...
finpulse portfolio.csv
```

> **Cost:** AI analysis uses ~300 tokens per run ≈ $0.0004. Practically free.

---

## Features

- **Live prices** — stocks and crypto via Yahoo Finance (no API key needed)
- **Portfolio analytics** — P&L, return %, 1D/1W/1M changes, allocation
- **Market overview** — S&P 500, NASDAQ, Gold, BTC, ETH at a glance
- **AI analysis** — Claude reads your portfolio and writes a plain-language summary with risks and opportunities
- **Interactive HTML report** — allocation pie, return bar chart, full holdings table
- **`--demo` mode** — try everything without any setup

---

## Usage

```bash
# Basic
finpulse portfolio.csv

# With AI analysis
finpulse portfolio.csv --api-key sk-ant-...

# Export HTML report
finpulse portfolio.csv --html report.html

# Demo mode (sample portfolio, no setup)
finpulse --demo

# Demo + HTML
finpulse --demo --html demo-report.html

# Skip AI (faster)
finpulse portfolio.csv --no-ai
```

## Options

| Flag | Description |
|---|---|
| `portfolio` | Path to CSV file |
| `--demo` | Run with sample data |
| `--api-key KEY` | Anthropic API key |
| `--html FILE` | Export HTML report |
| `--no-ai` | Skip AI analysis |
| `--no-color` | Disable colors (for pipes/CI) |

## Portfolio CSV format

| Column | Required | Description |
|---|---|---|
| `ticker` | ✅ | Stock symbol (AAPL, MSFT) or crypto pair (BTC-USD, ETH-USD) |
| `shares` | ✅ | Number of shares or coins held |
| `avg_buy_price` | ✅ | Average purchase price in USD |

Any extra columns are ignored.

## How the AI works

When you provide an Anthropic API key, finpulse sends your portfolio summary (no personal data — just tickers, P&L, and market context) to Claude and asks for a concise 3–4 sentence analysis covering:

- Overall portfolio health
- Key winners and losers
- One risk or opportunity to watch

No data is stored. Each run is independent.

## Installation

```bash
pip install finpulse
```

Or from source:
```bash
git clone https://github.com/ekrmsnr/finpulse
cd finpulse
pip install -e .
```

**Requirements:** Python ≥ 3.9, internet connection for live data.

## Related projects

- [gitpulse](https://github.com/ekrmsnr/gitpulse) — Analyze any Git repository
- [csv-detective](https://github.com/ekrmsnr/csv-detective) — Profile any CSV file

## Disclaimer

finpulse is for informational purposes only. Nothing here is financial advice. Always do your own research before making investment decisions.

## License

MIT
