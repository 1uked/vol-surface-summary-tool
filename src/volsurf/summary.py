from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd

@dataclass
class InstrumentSummary:
  underlying: str
  rows: int
  trade_dates: list[str]
  expiry_count: int
  dte_min: int | None
  dte_max: int | None
  avg_iv: float | None
  put_avg_iv: float | None
  call_avg_iv: float | None
  strike_skew: float | None
  smile_curvature: float | None
  term_slope_per_30d: float | None
  avg_spread: float | None
  median_relative_spread: float | None
  total_volume: int
  total_open_interest: int
  front_expiry_volume_share: float | None
  anomaly_count: int
  anomaly_examples: list[str]

  def to_dict(self) -> dict[str, Any]:
    return asdict(self)

def summarise_underlying(group: pd.DataFrame, top_anomalies: int = 3) -> InstrumentSummary:
  return InstrumentSummary


def build_summaries(df: pd.DataFrame, top_anomalies: int = 3) -> list[InstrumentSummary]:
  return [summarise_underlying(group, top_anomalies) for _, group in df.groupby("underlying")]
