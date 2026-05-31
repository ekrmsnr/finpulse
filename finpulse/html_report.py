from __future__ import annotations

from datetime import datetime
from pathlib import Path


def build_html(output: Path, holdings: list[dict], summary: dict,
               market: dict, ai_text: str | None) -> None:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    valid = [h for h in holdings if not h.get("error")]

    # ── Summary cards ────────────────────────────────────────────────────
    pnl_color = "#3fb950" if summary["total_pnl"] >= 0 else "#f85149"
    sign = "+" if summary["total_pnl"] >= 0 else ""
    cards = [
        (f"${summary['total_value']:,.2f}", "Total value",  "#58a6ff"),
        (f"${summary['total_cost']:,.2f}",  "Cost basis",   "#7d8590"),
        (f"{sign}${summary['total_pnl']:,.2f}", "Total P&L", pnl_color),
        (f"{sign}{summary['total_pnl_pct']:.2f}%", "Return", pnl_color),
        (str(summary["n_holdings"]), "Holdings",  "#c084fc"),
    ]
    cards_html = "".join(
        f'<div class="card"><div class="val" style="color:{c}">{v}</div>'
        f'<div class="lbl">{l}</div></div>'
        for v, l, c in cards
    )

    # ── Market overview ──────────────────────────────────────────────────
    market_html = ""
    for name, data in market.items():
        pct = data["change_pct"]
        col = "#3fb950" if pct >= 0 else "#f85149"
        arrow = "▲" if pct >= 0 else "▼"
        market_html += (
            f'<div class="card"><div class="val" style="color:{col}">'
            f'{arrow} {abs(pct):.2f}%</div>'
            f'<div class="lbl">{_esc(name)}</div></div>'
        )

    # ── AI analysis ──────────────────────────────────────────────────────
    ai_html = ""
    if ai_text:
        ai_html = f"""
        <h2>🤖 AI Analysis</h2>
        <div class="ai-box">{_esc(ai_text)}</div>"""

    # ── Pie chart data ───────────────────────────────────────────────────
    pie_labels  = [h["ticker"] for h in valid]
    pie_values  = [h["current_value"] for h in valid]
    pie_colors  = ["#58a6ff","#3fb950","#c084fc","#e3b341","#f85149",
                   "#79c0ff","#56d364","#d2a8ff","#ffa657","#ff7b72"]

    # ── Bar chart: P&L % ─────────────────────────────────────────────────
    bar_sorted  = sorted(valid, key=lambda x: x["pnl_pct"])
    bar_labels  = [h["ticker"] for h in bar_sorted]
    bar_values  = [h["pnl_pct"] for h in bar_sorted]
    bar_colors  = ["#3fb950" if v >= 0 else "#f85149" for v in bar_values]

    # ── Holdings table ───────────────────────────────────────────────────
    rows_html = ""
    for h in sorted(valid, key=lambda x: x["current_value"], reverse=True):
        pnl_c = "#3fb950" if h["pnl"] >= 0 else "#f85149"
        s = "+" if h["pnl"] >= 0 else ""
        d1_c = "#3fb950" if (h.get("change_1d_pct") or 0) >= 0 else "#f85149"
        m1_c = "#3fb950" if (h.get("change_1m_pct") or 0) >= 0 else "#f85149"
        rows_html += f"""<tr>
          <td><strong>{_esc(h['ticker'])}</strong></td>
          <td style="color:#7d8590;font-size:.8rem">{_esc(h['name'][:22])}</td>
          <td>{h['shares']}</td>
          <td>${h['avg_buy_price']:,.2f}</td>
          <td>${h['current_price']:,.2f}</td>
          <td>${h['current_value']:,.2f}</td>
          <td style="color:{pnl_c};font-weight:600">{s}${h['pnl']:,.2f}</td>
          <td style="color:{pnl_c}">{s}{h['pnl_pct']:.1f}%</td>
          <td style="color:{d1_c}">{(h.get('change_1d_pct') or 0):+.1f}%</td>
          <td style="color:{m1_c}">{(h.get('change_1m_pct') or 0):+.1f}%</td>
          <td>{h.get('allocation_pct',0):.1f}%</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>finpulse — portfolio report</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
* {{ box-sizing:border-box; margin:0; padding:0 }}
body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
       background:#0d1117; color:#e6edf3; padding:2rem; line-height:1.6 }}
h1 {{ font-size:1.6rem; font-weight:700; margin-bottom:.25rem }}
h2 {{ font-size:.85rem; font-weight:600; color:#7d8590; margin:2rem 0 .75rem;
     text-transform:uppercase; letter-spacing:.06em }}
.sub {{ color:#7d8590; font-size:.875rem; margin-bottom:2rem }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr));
        gap:12px; margin-bottom:1.5rem }}
.card {{ background:#161b22; border:1px solid #30363d; border-radius:8px; padding:1rem }}
.card .val {{ font-size:1.3rem; font-weight:700 }}
.card .lbl {{ font-size:.75rem; color:#7d8590; margin-top:4px }}
.charts {{ display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; margin-bottom:2rem }}
.chart-box {{ background:#161b22; border:1px solid #30363d; border-radius:8px; padding:1rem }}
.chart-box h3 {{ font-size:.8rem; color:#7d8590; margin-bottom:.5rem; text-transform:uppercase }}
table {{ width:100%; border-collapse:collapse; background:#161b22;
        border-radius:8px; overflow:hidden; font-size:.8rem; margin-bottom:2rem }}
th {{ text-align:left; padding:.5rem 1rem; color:#7d8590; font-size:.75rem;
     font-weight:600; border-bottom:1px solid #30363d }}
td {{ padding:.4rem 1rem; border-bottom:1px solid #21262d }}
tr:last-child td {{ border-bottom:none }}
.ai-box {{ background:#161b22; border:1px solid #e3b341; border-radius:8px;
          padding:1.25rem 1.5rem; color:#e6edf3; font-size:.95rem;
          line-height:1.7; margin-bottom:2rem }}
</style>
</head>
<body>
  <h1>💰 finpulse</h1>
  <p class="sub">Portfolio report · {now}</p>

  <h2>Summary</h2>
  <div class="grid">{cards_html}</div>

  <h2>Market overview</h2>
  <div class="grid">{market_html}</div>

  {ai_html}

  <h2>Allocation & performance</h2>
  <div class="charts">
    <div class="chart-box">
      <h3>Portfolio allocation</h3>
      <div id="pie"></div>
    </div>
    <div class="chart-box">
      <h3>Total return by asset</h3>
      <div id="bar"></div>
    </div>
  </div>

  <h2>Holdings</h2>
  <table>
    <thead><tr>
      <th>Ticker</th><th>Name</th><th>Shares</th><th>Avg buy</th>
      <th>Current</th><th>Value</th><th>P&L ($)</th><th>Return</th>
      <th>1D</th><th>1M</th><th>Alloc</th>
    </tr></thead>
    <tbody>{rows_html}</tbody>
  </table>

  <p style="color:#7d8590;font-size:.75rem;margin-top:2rem">
    Made with <a href="https://github.com/ekrmsnr/finpulse" style="color:#e3b341">finpulse</a>
    · Data from Yahoo Finance · Not financial advice
  </p>

<script>
const dark = {{
  paper_bgcolor:'#161b22', plot_bgcolor:'#161b22',
  font:{{color:'#e6edf3',size:11}},
  margin:{{t:10,r:10,b:40,l:50}}
}};

Plotly.newPlot('pie', [{{
  labels: {pie_labels},
  values: {pie_values},
  type: 'pie',
  marker: {{colors: {pie_colors[:len(pie_labels)]}}},
  textinfo: 'label+percent',
  hovertemplate: '%{{label}}<br>$%{{value:,.2f}}<br>%{{percent}}<extra></extra>'
}}], {{...dark, showlegend:false, margin:{{t:10,r:10,b:10,l:10}}}},
{{responsive:true, displayModeBar:false}});

Plotly.newPlot('bar', [{{
  x: {bar_values}, y: {bar_labels},
  type:'bar', orientation:'h',
  marker:{{color:{bar_colors}}},
  hovertemplate:'%{{y}}: %{{x:+.1f}}%<extra></extra>'
}}], {{...dark,
  xaxis:{{...dark.xaxis, title:'Return (%)', zeroline:true, zerolinecolor:'#30363d'}},
  yaxis:{{autorange:'reversed'}},
  showlegend:false, margin:{{...dark.margin, l:60}}
}}, {{responsive:true, displayModeBar:false}});
</script>
</body>
</html>"""

    output.write_text(html, encoding="utf-8")


def _esc(s: str) -> str:
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
