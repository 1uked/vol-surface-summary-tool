from __future__ import annotations

import json

from .summary import InstrumentSummary

SYSTEM_PROMPT = """You are a careful quantitative analyst.
Write exactly one paragraph of plain-English commentary about an options implied-volatility surface.
Use only the supplied metrics and anomaly examples.
Do not invent causes, news, catalysts, spot prices, or macro context.
If a feature is missing, simply omit it or say the data does not show it.
Keep the tone precise and concise.
"""

def build_user_prompt(summary: InstrumentSummary) -> str:
  payload = summary.to_dict()
  return (
    "Generate a one-paragraph grounded narrative for this underlying. "
    "Describe skew shape, term structure, liquidity, and any anomalies when supported by the metrics.\n\n"
    f"METRICS_JSON:\n{json.dumps(payload, indent=2)}"
  )
