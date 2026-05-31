from __future__ import annotations

import pandas as pd
from pathlib import Path


def load_portfolio(path: Path) -> list[dict]:
    """Load portfolio from CSV. Required columns: ticker, shares, avg_buy_price"""
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    required = {"ticker", "shares", "avg_buy_price"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing columns: {missing}. "
            f"CSV must have: ticker, shares, avg_buy_price"
        )
    return df[["ticker", "shares", "avg_buy_price"]].to_dict("records")


def compute_summary(holdings: list[dict]) -> dict:
    """Compute portfolio-level aggregates."""
    valid = [h for h in holdings if not h.get("error")]
    if not valid:
        return {}

    total_cost    = sum(h["cost_basis"]     for h in valid)
    total_value   = sum(h["current_value"]  for h in valid)
    total_pnl     = total_value - total_cost
    total_pnl_pct = (total_pnl / total_cost * 100) if total_cost else 0

    # Best and worst performers
    by_pnl_pct = sorted(valid, key=lambda x: x["pnl_pct"], reverse=True)
    best  = by_pnl_pct[0]  if by_pnl_pct else None
    worst = by_pnl_pct[-1] if by_pnl_pct else None

    # Allocation
    for h in valid:
        h["allocation_pct"] = round(h["current_value"] / total_value * 100, 1) if total_value else 0

    stocks = [h for h in valid if h.get("type") != "crypto"]
    crypto = [h for h in valid if h.get("type") == "crypto"]

    return {
        "total_cost":      round(total_cost, 2),
        "total_value":     round(total_value, 2),
        "total_pnl":       round(total_pnl, 2),
        "total_pnl_pct":   round(total_pnl_pct, 2),
        "n_holdings":      len(valid),
        "n_stocks":        len(stocks),
        "n_crypto":        len(crypto),
        "best_performer":  best,
        "worst_performer": worst,
    }
