from __future__ import annotations

import os
from typing import Optional


def get_ai_analysis(
    holdings: list[dict],
    summary: dict,
    market: dict,
    api_key: Optional[str] = None,
) -> Optional[str]:
    """
    Send portfolio data to Claude and get a plain-language analysis.
    Returns None if API key is missing or call fails.
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
    except ImportError:
        return None

    # Build context
    holdings_text = "\n".join(
        f"- {h['ticker']} ({h['name']}): {h['shares']} shares, "
        f"avg buy ${h['avg_buy_price']}, current ${h['current_price']}, "
        f"P&L {h['pnl_pct']:+.1f}%, 1d {h.get('change_1d_pct', 0):+.1f}%, "
        f"1m {h.get('change_1m_pct') or 0:+.1f}%"
        for h in holdings if not h.get("error")
    )

    market_text = "\n".join(
        f"- {name}: {data['change_pct']:+.1f}% today"
        for name, data in market.items()
    ) if market else "Not available"

    prompt = f"""You are a concise financial analyst. Analyze this portfolio and provide a brief, actionable summary.

PORTFOLIO SUMMARY:
- Total value: ${summary.get('total_value', 0):,.2f}
- Total P&L: ${summary.get('total_pnl', 0):+,.2f} ({summary.get('total_pnl_pct', 0):+.1f}%)
- Holdings: {summary.get('n_holdings', 0)} ({summary.get('n_stocks', 0)} stocks, {summary.get('n_crypto', 0)} crypto)

HOLDINGS:
{holdings_text}

MARKET CONTEXT (today):
{market_text}

Write a 3-4 sentence analysis covering:
1. Overall portfolio health
2. Key winners/losers and why it might matter
3. One brief risk or opportunity to watch

Be direct, specific, and avoid generic advice. No bullet points — flowing prose only."""

    try:
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text.strip()
    except Exception:
        return None
