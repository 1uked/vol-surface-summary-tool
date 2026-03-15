import argparse

from src.volsurf.data_loader import load_options_csv
from src.volsurf.summary import build_summaries
from src.volsurf.llm import build_narrator


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(description="Generate narratives for options vol surfaces.")
  parser.add_argument("--csv", required=True, help="Path to the options CSV file.")
  parser.add_argument("--save", default="outputs/instrument_summaries.json", help="Path to save JSON output.")
  parser.add_argument("--top-anomalies", type=int, default=3, help="Number of anomaly results to keep per underlying.")
  return parser.parse_args()

def main() -> None:
  args = parse_args()
  df = load_options_csv(args.csv)
  summaries = build_summaries(df)
  narrator = build_narrator()
  
  print(summaries)
  # call llm
  
  print(f"Saved {len([])} summaries to {args.save}")


if __name__ == "__main__":
    main()