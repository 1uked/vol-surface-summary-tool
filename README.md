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
% python main.py --csv data/options_eod.csv

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

Narrative: AAPL's implied-volatility surface over the five-day observation window shows an average IV of approximately 21.7%, with put and call average IVs of roughly 21.7% each — a difference of less than one percentage point that is consistent with near parity between the two option types. The strike skew summary statistic is a small positive value (0.018), though without an explicitly defined sign convention no directional economic interpretation is warranted; smile curvature is essentially negligible at roughly −0.000023, suggesting the strike profile is quite flat with minimal convexity across the observed strikes. The term structure slopes modestly upward at about 1.3 percentage points per 30 days, which is consistent with a roughly flat-to-mildly-upward-sloping term structure given the small magnitude. Quoted spreads appear moderate, with a median relative spread of approximately 3.3%, and volume is distributed across expirations rather than heavily concentrated in the front expiry, which accounts for about 11.5% of total volume. Two observations stand out as notable outliers relative to the fitted surface: a May 2, 2025 call at the 200-strike with an IV of 6.504 versus a fitted value of 0.948 (residual +5.556), and an April 25, 2025 put at the 150-strike with an IV of 5.744 versus a fitted value of 2.781 (residual +2.963); the data does not establish whether these represent genuine signals or other sources of deviation, only that they appear as significant outliers relative to the modeled surface.
```