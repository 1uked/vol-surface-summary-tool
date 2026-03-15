from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
  "underlying",
  "expiry",
  "strike",
  "option_type",
  "bid",
  "ask",
  "iv",
  "open_interest",
  "volume",
  "trade_date",
}

def load_options_csv(path: str | Path) -> pd.DataFrame:
  """Load the data and add standard derived columns."""
  df = pd.read_csv(path, parse_dates=["expiry", "trade_date"])

  df["dte"] = (df["expiry"] - df["trade_date"]).dt.days
  df["mid"] = (df["bid"] + df["ask"]) / 2.0
  df["spread"] = df["ask"] - df["bid"]
  df["relative_spread"] = df["spread"] / df["mid"].replace(0, pd.NA)

  return df
