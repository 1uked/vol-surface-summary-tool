import json
from pathlib import Path
from typing import Iterable

from src.volsurf.summary import InstrumentSummary

def render_console_block(summary: InstrumentSummary, narrative: str) -> str:
  lines = [
    f"Underlying: {summary.underlying}",
    f"Rows: {summary.rows}",
    f"Trade dates: {', '.join(summary.trade_dates)}",
    f"Expiries: {summary.expiry_count} | DTE range: {summary.dte_min} to {summary.dte_max}",
    f"Average IV: {pct(summary.avg_iv)}",
    f"Put avg IV: {pct(summary.put_avg_iv)} | Call avg IV: {pct(summary.call_avg_iv)}",
    f"Strike skew: {vol_pts(summary.strike_skew)} | Smile curvature: {vol_pts(summary.smile_curvature)}",
    f"Term slope: {vol_pts(summary.term_slope_per_30d)} / 30d",
    f"Average spread: {summary.avg_spread:.4f} | Median relative spread: {pct(summary.median_relative_spread)}",
    f"Total volume: {summary.total_volume:,} | Open interest: {summary.total_open_interest:,}",
    f"Front expiry volume share: {pct(summary.front_expiry_volume_share)}",
    f"Anomalies: {summary.anomaly_count}",
    f"Narrative: {narrative}",
  ]
  return "\n".join(lines)

def save_json(path: str | Path, records: Iterable[dict]) -> None:
  out_path = Path(path)
  out_path.parent.mkdir(parents=True, exist_ok=True)
  with out_path.open("w", encoding="utf-8") as f:
    json.dump(list(records), f, indent=2)

def pct(value: float | None) -> str:
  if value is None:
    return "n/a"
  return f"{value * 100:.5f}%"

def vol_pts(value: float | None) -> str:
  if value is None:
    return "n/a"
  return f"{value * 100:.5f} vol pts"