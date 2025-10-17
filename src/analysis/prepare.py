from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[2]
RAW = BASE / "data" / "raw" / "norwegian_traffic_nvdb.csv"
OUT = BASE / "data" / "processed" / "traffic_metrics.csv"
DATE_COL_CANDIDATES = ["date", "timestamp", "datetime"]


def load_raw(path: Path) -> pd.DataFrame:
    """Load Norwegian NVDB traffic count data with enhanced processing."""
    df = pd.read_csv(path)
    
    # Convert date column
    for c in DATE_COL_CANDIDATES:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c])
            df = df.rename(columns={c: "date"})
            break
    if "date" not in df.columns:
        raise ValueError("Could not find a date column. Add 'date' to your CSV.")
    
    # Handle value column (traffic counts)
    if "value" not in df.columns:
        num_cols = df.select_dtypes(include="number").columns.tolist()
        if not num_cols:
            raise ValueError(
                "No numeric column found. Add a 'value' column to your CSV."
            )
        df = df.rename(columns={num_cols[0]: "value"})
    
    # Keep NVDB-specific data columns if available
    keep_cols = ["date", "value"]
    nvdb_cols = ["region", "road_category", "traffic_type", "county", "road_number"]
    for col in nvdb_cols:
        if col in df.columns:
            keep_cols.append(col)
    
    return df[keep_cols].sort_values("date")


def build_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Build comprehensive traffic metrics from NVDB data."""
    out = df.copy()
    out["year"] = out["date"].dt.year
    out["month"] = out["date"].dt.month
    
    # Calculate traffic trend metrics
    out = out.sort_values(["region", "date"])
    out["monthly_change"] = out.groupby("region")["value"].pct_change() * 100
    out["yearly_change"] = out.groupby("region")["value"].pct_change(12) * 100
    
    # Calculate rolling averages for trend analysis
    out["rolling_3_month"] = out.groupby("region")["value"].rolling(3, min_periods=1).mean().values
    out["rolling_12_month"] = out.groupby("region")["value"].rolling(12, min_periods=1).mean().values
    
    # Monthly aggregation by region and road category
    group_cols = ["year", "month"]
    if "region" in df.columns:
        group_cols.append("region")
    if "road_category" in df.columns:
        group_cols.append("road_category")
    
    monthly = (
        out.groupby(group_cols)
        .agg({
            "value": ["sum", "mean", "median", "count", "max", "min"],
            "monthly_change": "mean",
            "yearly_change": "mean",
            "rolling_3_month": "last",
            "rolling_12_month": "last"
        })
        .reset_index()
    )
    
    # Flatten column names for traffic data
    new_cols = []
    for col in monthly.columns:
        if isinstance(col, tuple):
            if col[0] == "value":
                new_cols.append(f"traffic_{col[1]}")
            else:
                new_cols.append(f"{col[0]}_{col[1]}" if col[1] else col[0])
        else:
            new_cols.append(col)
    
    monthly.columns = new_cols
    
    # Add Norwegian traffic analysis context
    monthly["date"] = pd.to_datetime(monthly[["year", "month"]].assign(day=1))
    monthly["season"] = monthly["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring", 
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    })
    
    # Add traffic intensity categories
    if "traffic_mean" in monthly.columns:
        monthly["traffic_intensity"] = pd.cut(
            monthly["traffic_mean"],
            bins=[0, 30000, 45000, 60000, float('inf')],
            labels=["Low", "Medium", "High", "Very High"]
        )
    
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
