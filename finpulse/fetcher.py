from __future__ import annotations

import time
from typing import Optional
import requests
import yfinance as yf
import pandas as pd


def fetch_portfolio(holdings: list[dict]) -> list[dict]:
    """
    Fetch current price data for each holding.
    holdings: [{"ticker": "AAPL", "shares": 10, "avg_buy_price": 150.0}, ...]
    Returns enriched list with current price, change, value etc.
    """
    results = []
    for h in holdings:
        ticker = h["ticker"].upper()
        shares = float(h["shares"])
        avg_buy = float(h["avg_buy_price"])

        data = _fetch_ticker(ticker)
        if data is None:
            results.append({**h, "error": True, "ticker": ticker})
            continue

        current = data["price"]
        cost_basis = shares * avg_buy
        current_value = shares * current
        pnl = current_value - cost_basis
        pnl_pct = (pnl / cost_basis * 100) if cost_basis else 0

        results.append({
            "ticker": ticker,
            "name": data.get("name", ticker),
            "type": data.get("type", "stock"),
            "shares": shares,
            "avg_buy_price": avg_buy,
            "current_price": round(current, 4),
            "cost_basis": round(cost_basis, 2),
            "current_value": round(current_value, 2),
            "pnl": round(pnl, 2),
            "pnl_pct": round(pnl_pct, 2),
            "change_1d": data.get("change_1d"),
            "change_1d_pct": data.get("change_1d_pct"),
            "change_1w_pct": data.get("change_1w_pct"),
            "change_1m_pct": data.get("change_1m_pct"),
            "currency": data.get("currency", "USD"),
            "error": False,
        })

    return results


def _fetch_ticker(ticker: str) -> Optional[dict]:
    try:
        tk = yf.Ticker(ticker)
        info = tk.info

        # Current price — try multiple fields
        price = (
            info.get("regularMarketPrice")
            or info.get("currentPrice")
            or info.get("previousClose")
        )
        if not price:
            return None

        prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose") or price
        change_1d = price - prev_close
        change_1d_pct = (change_1d / prev_close * 100) if prev_close else 0

        # Historical changes
        hist = tk.history(period="1mo", interval="1d")
        change_1w_pct = None
        change_1m_pct = None
        if not hist.empty and len(hist) >= 2:
            price_1m_ago = float(hist["Close"].iloc[0])
            price_1w_ago = float(hist["Close"].iloc[-6]) if len(hist) >= 6 else price_1m_ago
            change_1m_pct = round((price - price_1m_ago) / price_1m_ago * 100, 2)
            change_1w_pct = round((price - price_1w_ago) / price_1w_ago * 100, 2)

        asset_type = "crypto" if ticker.endswith("-USD") or ticker.endswith("-USDT") else "stock"

        return {
            "price": float(price),
            "name": info.get("longName") or info.get("shortName") or ticker,
            "type": asset_type,
            "currency": info.get("currency", "USD"),
            "change_1d": round(change_1d, 4),
            "change_1d_pct": round(change_1d_pct, 2),
            "change_1w_pct": change_1w_pct,
            "change_1m_pct": change_1m_pct,
        }
    except Exception:
        return None


def fetch_market_overview() -> dict:
    """Fetch major indices and crypto for context."""
    tickers = {
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "Gold": "GC=F",
        "Bitcoin": "BTC-USD",
        "Ethereum": "ETH-USD",
    }
    overview = {}
    for name, symbol in tickers.items():
        try:
            tk = yf.Ticker(symbol)
            info = tk.info
            price = info.get("regularMarketPrice") or info.get("currentPrice")
            prev  = info.get("previousClose") or info.get("regularMarketPreviousClose")
            if price and prev:
                change_pct = round((price - prev) / prev * 100, 2)
                overview[name] = {"price": price, "change_pct": change_pct}
        except Exception:
            pass
    return overview
