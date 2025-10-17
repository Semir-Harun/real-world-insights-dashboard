from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2]
RAW = BASE / "data" / "raw" / "norwegian_ev_registrations.csv"
OUT = BASE / "data" / "processed" / "ev_metrics.csv"
DATE_COL_CANDIDATES = ["date", "timestamp", "datetime"]


def load_raw(path: Path) -> pd.DataFrame:
    """Load Norwegian EV registration data with enhanced processing."""
    df = pd.read_csv(path)
    
    # Convert date column
    for c in DATE_COL_CANDIDATES:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c])
            df = df.rename(columns={c: "date"})
            break
    if "date" not in df.columns:
        raise ValueError("Could not find a date column. Add 'date' to your CSV.")
    
    # Handle value column (EV registrations)
    if "value" not in df.columns:
        num_cols = df.select_dtypes(include="number").columns.tolist()
        if not num_cols:
            raise ValueError(
                "No numeric column found. Add a 'value' column to your CSV."
            )
        df = df.rename(columns={num_cols[0]: "value"})
    
    # Keep additional Norwegian EV data if available
    keep_cols = ["date", "value"]
    if "vehicle_type" in df.columns:
        keep_cols.append("vehicle_type")
    if "region" in df.columns:
        keep_cols.append("region")
    if "fuel_type" in df.columns:
        keep_cols.append("fuel_type")
    
    return df[keep_cols].sort_values("date")


def build_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Build comprehensive EV metrics with Norwegian context."""
    out = df.copy()
    out["year"] = out["date"].dt.year
    out["month"] = out["date"].dt.month
    
    # Calculate growth metrics for EV registrations
    out = out.sort_values("date")
    out["monthly_growth"] = out["value"].pct_change() * 100
    out["yearly_growth"] = out["value"].pct_change(12) * 100
    
    # Monthly aggregation
    monthly = (
        out.groupby(["year", "month"])
        .agg({
            "value": ["sum", "mean", "median", "count", "max"],
            "monthly_growth": "mean",
            "yearly_growth": "mean"
        })
        .reset_index()
    )
    
    # Flatten column names
    monthly.columns = [
        "year",
        "month", 
        "ev_registrations_total",
        "ev_registrations_mean",
        "ev_registrations_median", 
        "data_points",
        "ev_registrations_max",
        "monthly_growth_rate",
        "yearly_growth_rate"
    ]
    
    # Add Norwegian EV adoption insights
    monthly["date"] = pd.to_datetime(monthly[["year", "month"]].assign(day=1))
    monthly["season"] = monthly["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring", 
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    })
    
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
