from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
import argparse

BASE = Path(__file__).resolve().parents[2]
DATE_COL_CANDIDATES = ["date", "timestamp", "datetime"]

def load_raw(path: Path) -> pd.DataFrame:
    """Load Norwegian data with enhanced processing."""
    df = pd.read_csv(path)
    
    # Convert date column
    for c in DATE_COL_CANDIDATES:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c])
            df = df.rename(columns={c: "date"})
            break
    if "date" not in df.columns:
        raise ValueError("Could not find a date column. Add 'date' to your CSV.")
    
    # Handle value column
    if "value" not in df.columns:
        num_cols = df.select_dtypes(include="number").columns.tolist()
        if not num_cols:
            raise ValueError("No numeric column found. Add a 'value' column to your CSV.")
        df = df.rename(columns={num_cols[0]: "value"})
    
    # Keep additional data columns if available
    keep_cols = ["date", "value"]
    additional_cols = ["vehicle_type", "region", "fuel_type", "road_category", "traffic_type", "county", "road_number"]
    for col in additional_cols:
        if col in df.columns:
            keep_cols.append(col)
    
    return df[keep_cols].sort_values("date")

def build_ev_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Build EV registration metrics."""
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
        "year", "month", "ev_registrations_total", "ev_registrations_mean",
        "ev_registrations_median", "data_points", "ev_registrations_max",
        "monthly_growth_rate", "yearly_growth_rate"
    ]
    
    # Add additional analysis
    monthly["date"] = pd.to_datetime(monthly[["year", "month"]].assign(day=1))
    monthly["season"] = monthly["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring", 
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    })
    
    return monthly

def build_traffic_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Build traffic metrics from NVDB data."""
    out = df.copy()
    out["year"] = out["date"].dt.year
    out["month"] = out["date"].dt.month
    
    # Calculate traffic trend metrics
    out = out.sort_values(["region", "date"])
    out["monthly_change"] = out.groupby("region")["value"].pct_change() * 100
    out["yearly_change"] = out.groupby("region")["value"].pct_change(12) * 100
    
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
            "yearly_change": "mean"
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
    
    # Add analysis context
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
    parser = argparse.ArgumentParser(description='Process Norwegian transportation data')
    parser.add_argument('--dataset', choices=['ev', 'traffic', 'both'], default='both',
                       help='Which dataset to process')
    args = parser.parse_args()
    
    if args.dataset in ['ev', 'both']:
        # Process EV data
        ev_raw = BASE / "data" / "raw" / "norwegian_ev_registrations.csv"
        ev_out = BASE / "data" / "processed" / "ev_metrics.csv"
        
        if ev_raw.exists():
            print(f"Processing EV data from {ev_raw}")
            df_ev = load_raw(ev_raw)
            metrics_ev = build_ev_metrics(df_ev)
            ev_out.parent.mkdir(parents=True, exist_ok=True)
            metrics_ev.to_csv(ev_out, index=False)
            print(f"✓ EV data: Wrote {ev_out} ({len(metrics_ev)} rows)")
        else:
            print(f"⚠️ EV raw file not found: {ev_raw}")
    
    if args.dataset in ['traffic', 'both']:
        # Process traffic data
        traffic_raw = BASE / "data" / "raw" / "norwegian_traffic_nvdb.csv"
        traffic_out = BASE / "data" / "processed" / "traffic_metrics.csv"
        
        if traffic_raw.exists():
            print(f"Processing traffic data from {traffic_raw}")
            df_traffic = load_raw(traffic_raw)
            metrics_traffic = build_traffic_metrics(df_traffic)
            traffic_out.parent.mkdir(parents=True, exist_ok=True)
            metrics_traffic.to_csv(traffic_out, index=False)
            print(f"✓ Traffic data: Wrote {traffic_out} ({len(metrics_traffic)} rows)")
        else:
            print(f"⚠️ Traffic raw file not found: {traffic_raw}")

if __name__ == "__main__":
    main()