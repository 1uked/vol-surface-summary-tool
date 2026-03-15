from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
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


def _fit_residual_anomalies(group: pd.DataFrame, threshold_floor: float = 0.03) -> list[dict[str, Any]]:
  """Detect anomalous points within one expiry/option_type slice."""
  if len(group) < 5:
    return []

  group = group.sort_values("strike")
  x = group["strike"].to_numpy(dtype=float)
  y = group["iv"].to_numpy(dtype=float)

  degree = 2 if len(group) >= 6 else 1
  coeffs = np.polyfit(x, y, deg=degree)
  y_hat = np.polyval(coeffs, x)
  residuals = y - y_hat

  sigma = float(np.std(residuals))
  threshold = max(threshold_floor, 2.0 * sigma)
  flags = np.abs(residuals) > threshold

  anomalies: list[dict[str, Any]] = []
  for row, pred, resid, flagged in zip(group.to_dict("records"), y_hat, residuals, flags):
    if not flagged:
      continue
    anomalies.append(
      {
        "trade_date": str(pd.Timestamp(row["trade_date"]).date()),
        "expiry": str(pd.Timestamp(row["expiry"]).date()),
        "option_type": str(row["option_type"]),
        "strike": float(row["strike"]),
        "iv": float(row["iv"]),
        "expected_iv": float(pred),
        "residual": float(resid),
      }
    )

  return anomalies


def summarise_underlying(group: pd.DataFrame, top_anomalies: int = 3) -> InstrumentSummary:
  underlying = str(group["underlying"].iloc[0])

  skew_values: list[float] = []
  curvature_values: list[float] = []
  anomalies: list[dict[str, Any]] = []

  for _, sub in group.groupby(["trade_date", "expiry", "option_type"], dropna=False):
    sub = sub.sort_values("strike")
    if len(sub) >= 4:
      q1 = sub["strike"].quantile(0.25)
      q3 = sub["strike"].quantile(0.75)
      low = sub.loc[sub["strike"] <= q1, "iv"].mean()
      high = sub.loc[sub["strike"] >= q3, "iv"].mean()
      middle = sub.loc[(sub["strike"] > q1) & (sub["strike"] < q3), "iv"].mean()
      skew_values.append(float(low - high))
      if pd.notna(middle):
        curvature_values.append(float(((low + high) / 2.0) - middle))

    anomalies.extend(_fit_residual_anomalies(sub))

  term_curve = group.groupby("dte", dropna=False)["iv"].mean().sort_index()
  term_slope_per_30d = None
  if len(term_curve) >= 2:
    slope_per_day = float(np.polyfit(term_curve.index.to_numpy(dtype=float), term_curve.to_numpy(dtype=float), 1)[0])
    term_slope_per_30d = slope_per_day * 30.0

  by_type = group.groupby("option_type")["iv"].mean()
  put_avg = by_type.get("put")
  call_avg = by_type.get("call")
  volume_by_expiry = group.groupby("expiry")["volume"].sum().sort_index()
  front_share = None
  if not volume_by_expiry.empty and volume_by_expiry.sum() > 0:
    front_share = float(volume_by_expiry.iloc[0] / volume_by_expiry.sum())

  trade_dates = sorted({str(ts.date()) for ts in pd.to_datetime(group["trade_date"])})

  anomaly_examples = [
    (
      f"{a['expiry']} {a['option_type']} strike {a['strike']:.2f} had IV {a['iv']:.3f}, "
      f"vs fitted {a['expected_iv']:.3f} (residual {a['residual']:+.3f})."
    )
    for a in sorted(anomalies, key=lambda item: abs(item["residual"]), reverse=True)[:top_anomalies]
  ]

  return InstrumentSummary(
    underlying=underlying,
    rows=int(len(group)),
    trade_dates=trade_dates,
    expiry_count=int(group["expiry"].nunique()),
    dte_min=int(group["dte"].min()),
    dte_max=int(group["dte"].max()),
    avg_iv=float(group["iv"].mean()),
    put_avg_iv=float(put_avg) if put_avg is not None else None,
    call_avg_iv=float(call_avg) if call_avg is not None else None,
    strike_skew=float(np.nanmedian(skew_values)) if skew_values else None,
    smile_curvature=float(np.nanmedian(curvature_values)) if curvature_values else None,
    term_slope_per_30d=term_slope_per_30d,
    avg_spread=float(group["spread"].mean()),
    median_relative_spread=float(group["relative_spread"].median()),
    total_volume=int(group["volume"].sum()),
    total_open_interest=int(group["open_interest"].sum()),
    front_expiry_volume_share=front_share,
    anomaly_count=int(len(anomalies)),
    anomaly_examples=anomaly_examples,
  )


def build_summaries(df: pd.DataFrame, top_anomalies: int = 3) -> list[InstrumentSummary]:
  return [summarise_underlying(group, top_anomalies=top_anomalies) for _, group in df.groupby("underlying")]
