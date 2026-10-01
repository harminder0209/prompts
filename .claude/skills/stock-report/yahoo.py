#!/usr/bin/env python3
"""Pull consensus, revisions, surprises and valuation from Yahoo Finance (via yfinance) as JSON.

Usage: python yahoo.py TICKER [--peers T1,T2,...] [--out FILE]

Unofficial source: yfinance reads Yahoo's internal endpoints. Personal research use only.
Every section is fetched independently; a failure becomes {"error": "..."} instead of aborting.
"""
import argparse
import json
import math
import sys
from datetime import datetime, timezone

try:
    import yfinance as yf
except ImportError:
    sys.exit("yfinance not installed: python3 -m pip install yfinance")

INFO_KEYS = [
    "longName", "currency", "currentPrice", "regularMarketTime", "marketCap", "enterpriseValue",
    "sharesOutstanding", "trailingPE", "forwardPE", "priceToSalesTrailing12Months",
    "enterpriseToRevenue", "enterpriseToEbitda", "trailingEps", "forwardEps",
    "numberOfAnalystOpinions", "recommendationKey", "fiftyTwoWeekLow", "fiftyTwoWeekHigh",
    "totalCash", "totalDebt", "freeCashflow", "operatingMargins", "revenueGrowth",
]
PEER_KEYS = [
    "longName", "currentPrice", "marketCap", "trailingPE", "forwardPE",
    "priceToSalesTrailing12Months", "enterpriseToEbitda", "operatingMargins", "revenueGrowth",
]
TABLES = {
    "earnings_estimate": "EPS consensus by period (0q=current qtr, +1q=next qtr, 0y=current FY, +1y=next FY)",
    "revenue_estimate": "Revenue consensus by period",
    "eps_trend": "Consensus EPS now vs 7/30/60/90 days ago (revision history)",
    "eps_revisions": "Count of analysts revising EPS up/down over 7/30 days",
    "earnings_history": "Last 4 quarters: actual EPS vs estimate (surprise)",
    "growth_estimates": "Consensus growth estimates",
}


def clean(v):
    """Make values JSON-safe (NaN -> None, timestamps -> ISO)."""
    if isinstance(v, float) and math.isnan(v):
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if hasattr(v, "item"):  # numpy scalar
        return clean(v.item())
    return v


def frame(df):
    if df is None or getattr(df, "empty", True):
        return None
    return {str(idx): {str(c): clean(val) for c, val in row.items()} for idx, row in df.iterrows()}


def section(fn):
    try:
        return fn()
    except Exception as e:  # noqa: BLE001 - report, never abort
        return {"error": f"{type(e).__name__}: {e}"}


def info_subset(t, keys):
    info = t.info or {}
    out = {k: clean(info.get(k)) for k in keys}
    if out.get("regularMarketTime"):
        out["regularMarketTime"] = datetime.fromtimestamp(out["regularMarketTime"], timezone.utc).isoformat()
    return out


def next_earnings(t):
    cal = t.calendar or {}
    dates = cal.get("Earnings Date") or []
    return {"earnings_date": [clean(d) for d in dates], "note": "Yahoo calendar; confirm against a company announcement"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--peers", default="")
    ap.add_argument("--out")
    a = ap.parse_args()

    t = yf.Ticker(a.ticker)
    data = {
        "source": "Yahoo Finance via yfinance (unofficial)",
        "label": "Consensus / Market data",
        "ticker": a.ticker.upper(),
        "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "url": f"https://finance.yahoo.com/quote/{a.ticker.upper()}/analysis/",
        "quote_and_valuation": section(lambda: info_subset(t, INFO_KEYS)),
        "next_earnings": section(lambda: next_earnings(t)),
    }
    for name, desc in TABLES.items():
        data[name] = {"description": desc, "data": section(lambda n=name: frame(getattr(t, n)))}
    if a.peers:
        data["peers"] = {
            p.strip().upper(): section(lambda p=p: info_subset(yf.Ticker(p.strip()), PEER_KEYS))
            for p in a.peers.split(",") if p.strip()
        }

    text = json.dumps(data, indent=2, default=str)
    if a.out:
        with open(a.out, "w") as f:
            f.write(text)
        print(a.out)
    else:
        print(text)


if __name__ == "__main__":
    main()
