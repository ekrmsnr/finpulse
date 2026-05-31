from __future__ import annotations

from contextlib import contextmanager
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box


class Display:
    def __init__(self, no_color: bool = False) -> None:
        self.console = Console(no_color=no_color, highlight=False)

    def print_header(self) -> None:
        title = Text()
        title.append("💰 finpulse", style="bold white")
        title.append("  portfolio analyzer", style="dim")
        self.console.print()
        self.console.print(Panel(title, border_style="bright_yellow", padding=(0, 2)))

    def print_success(self, msg: str) -> None:
        self.console.print(f"\n[bold green]✓[/] {msg}")

    def print_error(self, msg: str) -> None:
        self.console.print(f"\n[bold red]✗[/] {msg}")

    def print_warning(self, msg: str) -> None:
        self.console.print(f"\n[yellow]⚠[/] {msg}")

    @contextmanager
    def progress(self, label: str):
        with Progress(SpinnerColumn(),
                      TextColumn("[progress.description]{task.description}"),
                      console=self.console, transient=True) as prog:
            prog.add_task(label, total=None)
            yield

    # ── Market overview ───────────────────────────────────────────────────

    def print_market(self, market: dict) -> None:
        if not market:
            return
        self.console.print("\n[bold]🌍 Market overview[/]", style="bright_yellow")
        cards = []
        for name, data in market.items():
            pct = data["change_pct"]
            color = "green" if pct >= 0 else "red"
            sign  = "▲" if pct >= 0 else "▼"
            content = Text()
            content.append(f"[{color}]{sign} {abs(pct):.2f}%[/]\n", style="bold")
            content.append(name, style="dim")
            cards.append(Panel(content, border_style="dim", padding=(0, 1), width=16))
        self.console.print(Columns(cards, equal=False, padding=(0, 1)))

    # ── Portfolio summary ─────────────────────────────────────────────────

    def print_summary(self, s: dict) -> None:
        self.console.print("\n[bold]📊 Portfolio summary[/]", style="bright_yellow")
        pnl_color = "green" if s["total_pnl"] >= 0 else "red"
        sign = "+" if s["total_pnl"] >= 0 else ""
        cards = [
            _metric(f"${s['total_value']:,.2f}", "Total value"),
            _metric(f"${s['total_cost']:,.2f}",  "Cost basis"),
            _metric(f"[{pnl_color}]{sign}${s['total_pnl']:,.2f}[/]", "Total P&L"),
            _metric(f"[{pnl_color}]{sign}{s['total_pnl_pct']:.2f}%[/]", "Return"),
            _metric(str(s["n_holdings"]), "Holdings"),
            _metric(str(s["n_stocks"]),   "Stocks"),
            _metric(str(s["n_crypto"]),   "Crypto"),
        ]
        self.console.print(Columns(cards, equal=False, padding=(0, 2)))

        if s.get("best_performer"):
            b = s["best_performer"]
            w = s["worst_performer"]
            self.console.print(
                f"\n  [green]Best:[/]  [bold]{b['ticker']}[/] [green]{b['pnl_pct']:+.1f}%[/]"
                f"   [red]Worst:[/] [bold]{w['ticker']}[/] [red]{w['pnl_pct']:+.1f}%[/]"
            )

    # ── Holdings table ────────────────────────────────────────────────────

    def print_holdings(self, holdings: list[dict]) -> None:
        self.console.print("\n[bold]📋 Holdings[/]", style="bright_yellow")
        table = Table(box=box.SIMPLE_HEAD, show_header=True, header_style="bold dim")
        table.add_column("Ticker",  min_width=8)
        table.add_column("Name",    min_width=18)
        table.add_column("Shares",  justify="right", width=8)
        table.add_column("Avg buy", justify="right", width=9)
        table.add_column("Current", justify="right", width=9)
        table.add_column("Value",   justify="right", width=11)
        table.add_column("P&L",     justify="right", width=11)
        table.add_column("Return",  justify="right", width=8)
        table.add_column("1D",      justify="right", width=7)
        table.add_column("1M",      justify="right", width=7)
        table.add_column("Alloc",   justify="right", width=6)

        for h in sorted(holdings, key=lambda x: x.get("current_value", 0), reverse=True):
            if h.get("error"):
                table.add_row(h["ticker"], "[red]fetch error[/]", *["—"] * 9)
                continue

            pnl_c = "green" if h["pnl"] >= 0 else "red"
            d1_c  = "green" if (h.get("change_1d_pct") or 0) >= 0 else "red"
            m1_c  = "green" if (h.get("change_1m_pct") or 0) >= 0 else "red"
            sign  = "+" if h["pnl"] >= 0 else ""

            table.add_row(
                f"[bold]{h['ticker']}[/]",
                h["name"][:20],
                str(h["shares"]),
                f"${h['avg_buy_price']:,.2f}",
                f"${h['current_price']:,.2f}",
                f"${h['current_value']:,.2f}",
                f"[{pnl_c}]{sign}${h['pnl']:,.2f}[/]",
                f"[{pnl_c}]{sign}{h['pnl_pct']:.1f}%[/]",
                f"[{d1_c}]{h.get('change_1d_pct') or 0:+.1f}%[/]",
                f"[{m1_c}]{h.get('change_1m_pct') or 0:+.1f}%[/]",
                f"{h.get('allocation_pct', 0):.1f}%",
            )
        self.console.print(table)

    # ── AI analysis ───────────────────────────────────────────────────────

    def print_ai_analysis(self, text: str) -> None:
        self.console.print("\n[bold]🤖 AI Analysis[/]", style="bright_yellow")
        self.console.print(Panel(
            text,
            border_style="bright_yellow",
            padding=(1, 2),
        ))

    def print_no_api_key(self) -> None:
        self.console.print(
            "\n[dim]💡 Tip: Set [bold]ANTHROPIC_API_KEY[/] to enable AI analysis. "
            "See README for setup instructions.[/]"
        )


def _metric(value: str, label: str) -> Panel:
    content = Text()
    content.append(value + "\n", style="bold white")
    content.append(label, style="dim")
    return Panel(content, border_style="dim", padding=(0, 1), width=18)
