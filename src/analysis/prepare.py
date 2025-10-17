from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2]
RAW = BASE / "data" / "raw" / "dataset.csv"
OUT = BASE / "data" / "processed" / "ev_metrics.csv"
DATE_COL_CANDIDATES = ["date", "timestamp", "datetime"]


def load_raw(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    for c in DATE_COL_CANDIDATES:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c])
            df = df.rename(columns={c: "date"})
            break
    if "date" not in df.columns:
        raise ValueError("Could not find a date column. Add 'date' to your CSV.")
    if "value" not in df.columns:
        num_cols = df.select_dtypes(include="number").columns.tolist()
        if not num_cols:
            raise ValueError(
                "No numeric column found. Add a 'value' column to your CSV."
            )
        df = df.rename(columns={num_cols[0]: "value"})
    return df[["date", "value"]].sort_values("date")


def build_metrics(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["year"] = out["date"].dt.year
    out["month"] = out["date"].dt.month
    monthly = (
        out.groupby(["year", "month"])["value"]
        .agg(["sum", "mean", "median", "count"])
        .reset_index()
    )
    monthly.columns = [
        "year",
        "month",
        "value_sum",
        "value_mean",
        "value_median",
        "value_count",
    ]
    return monthly


def main() -> None:
    if not RAW.exists():
        print(f"Missing raw file: {RAW}. Put your CSV there or run downloader.")
        sys.exit(1)
    df = load_raw(RAW)
    metrics = build_metrics(df)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(OUT, index=False)
    print(f"Wrote {OUT} ({len(metrics)} rows).")


if __name__ == "__main__":
    main()
