import argparse

from src.volsurf.data_loader import load_options_csv
from src.volsurf.summary import build_summaries
from src.volsurf.llm import build_narrator
from src.volsurf.record import render_console_block,save_json


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
  
  records = []
  for summary in summaries:
    narrative = narrator.generate(summary)
    print(render_console_block(summary, narrative))
    records.append(
      {
        **summary.to_dict(),
        "narrative": narrative,
      }
    )
    
  save_json(args.save, records)
  print(f"Saved {len(records)} summaries to {args.save}")

if __name__ == "__main__":
    main()