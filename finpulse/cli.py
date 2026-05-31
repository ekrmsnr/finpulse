import argparse
import sys
from pathlib import Path

from .display import Display


def main():
    parser = argparse.ArgumentParser(
        prog="finpulse",
        description="Real-time portfolio analyzer with AI insights.",
    )
    parser.add_argument("portfolio", nargs="?",
                        help="Path to portfolio CSV (columns: ticker, shares, avg_buy_price)")
    parser.add_argument("--demo", action="store_true",
                        help="Run with sample data (no setup needed)")
    parser.add_argument("--api-key", metavar="KEY",
                        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)")
    parser.add_argument("--html", metavar="FILE",
                        help="Export HTML report to FILE")
    parser.add_argument("--no-color", action="store_true",
                        help="Disable colored output")
    parser.add_argument("--no-ai", action="store_true",
                        help="Skip AI analysis")

    args = parser.parse_args()
    display = Display(no_color=args.no_color)
    display.print_header()

    if not args.demo and not args.portfolio:
        display.print_error("Provide a portfolio CSV or use --demo to try with sample data.")
        parser.print_help()
        sys.exit(1)

    try:
        if args.demo:
            from .demo import DEMO_HOLDINGS, DEMO_MARKET, DEMO_AI_TEXT
            holdings = DEMO_HOLDINGS
            market   = DEMO_MARKET
            from .analyzer import compute_summary
            summary = compute_summary(holdings)
            display.print_market(market)
            display.print_summary(summary)
            display.print_holdings(holdings)
            if not args.no_ai:
                display.print_ai_analysis(DEMO_AI_TEXT)
            if args.html:
                from .html_report import build_html
                html_path = Path(args.html)
                build_html(html_path, holdings, summary, market, DEMO_AI_TEXT)
                display.print_success(f"HTML report saved → {html_path}")
            return

        # Real mode
        from .analyzer import load_portfolio, compute_summary
        from .fetcher import fetch_portfolio, fetch_market_overview
        from .ai import get_ai_analysis

        with display.progress("Loading portfolio..."):
            holdings_input = load_portfolio(Path(args.portfolio))

        with display.progress("Fetching live prices..."):
            holdings = fetch_portfolio(holdings_input)

        with display.progress("Fetching market overview..."):
            market = fetch_market_overview()

        summary = compute_summary(holdings)
        if not summary:
            display.print_error("No valid holdings found.")
            sys.exit(1)

        display.print_market(market)
        display.print_summary(summary)
        display.print_holdings(holdings)

        ai_text = None
        if not args.no_ai:
            with display.progress("Running AI analysis..."):
                ai_text = get_ai_analysis(
                    holdings, summary, market,
                    api_key=args.api_key,
                )
            if ai_text:
                display.print_ai_analysis(ai_text)
            else:
                display.print_no_api_key()

        if args.html:
            from .html_report import build_html
            html_path = Path(args.html)
            build_html(html_path, holdings, summary, market, ai_text)
            display.print_success(f"HTML report saved → {html_path}")

    except ValueError as exc:
        display.print_error(str(exc))
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        sys.exit(0)


if __name__ == "__main__":
    main()
