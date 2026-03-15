# vol-surface-summary-tool

This script analyses an options implied volatility dataset and
computes metrics for each instrument's volatility surface, including skew, term structure slope, liquidity statistics, and
volatility outliers.

These computed metrics are passed to an LLM which generates a narrative describing the notable features of the surface.

## Run

```bash
python main.py --csv data/options_eod.csv
```
```bash
python main.py --csv data/options_eod.csv --narrative-style short
```

## Example output

```text
% python main.py --csv data/options_eod.csv --narrative-style short

Underlying: AAPL
Rows: 1204
Trade dates: 2025-03-03, 2025-03-04, 2025-03-05, 2025-03-06, 2025-03-07
Expiries: 9 | DTE range: 1 to 56
Average IV: 21.71%
Put avg IV: 21.66% | Call avg IV: 21.77%
Strike skew: 1.75 vol pts | Smile curvature: -0.00 vol pts
Term slope: 1.32 vol pts / 30d
Average spread: 0.5704 | Median relative spread: 3.33%
Total volume: 225,506 | Open interest: 961,387
Front expiry volume share: 11.53%
Anomalies: 2

Narrative: AAPL's implied-volatility surface over the March 3–7, 2025 observation window shows a mean IV of roughly 21.7%, with puts and calls nearly at parity (put avg IV 21.66% vs. call avg IV 21.77%), a modest positive strike skew of 0.018, and slight negative smile curvature, indicating a mildly downward-sloping skew with minimal wing convexity. The term structure is gently upward-sloping at approximately 1.3 vol points per 30 days, and front-expiry volume accounts for only about 11.5% of total activity, suggesting trader interest is distributed across the nine available expirations rather than concentrated in the nearest contract. Liquidity appears adequate given 225,506 contracts traded against 961,387 in open interest, though the median relative spread of 3.3% and average dollar spread of $0.57 point to moderate bid-ask friction. Two notable anomalies are present: a May 2 200-strike call with IV of 6.50 versus a fitted value of 0.95 (residual +5.56), and an April 25 150-strike put with IV of 5.74 versus a fitted value of 2.78 (residual +2.96), both representing deep-strike outliers that are likely artifacts of stale quotes or extremely thin markets rather than genuine surface features.
```