import argparse
import pandas as pd
from pathlib import Path


def load_raw(filename):
    """Load raw data file"""
    raw_path = Path(__file__).resolve().parents[2] / "data" / "raw" / filename
    print(f"Processing {filename.split('_')[1].upper()} data from {raw_path}")
    return pd.read_csv(raw_path)


def build_ev_metrics(df):
    """Build EV registration metrics with growth calculations"""
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["season"] = df["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring", 
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    })
    
    # Group by date and calculate metrics
    monthly = df.groupby("date").agg({
        "value": ["sum", "mean", "max", "count"]
    }).round(1)
    monthly.columns = ["ev_registrations_total", "ev_registrations_mean", "ev_registrations_max", "ev_registrations_count"]
    monthly = monthly.reset_index()
    
    # Calculate monthly growth rate
    monthly["monthly_growth_rate"] = monthly["ev_registrations_total"].pct_change() * 100
    monthly["monthly_growth_rate"] = monthly["monthly_growth_rate"].fillna(0).round(1)
    
    # Add date components
    monthly["year"] = monthly["date"].dt.year
    monthly["month"] = monthly["date"].dt.month
    monthly["season"] = monthly["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring", 
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    })
    
    return monthly


def build_traffic_metrics(df):
    """Build traffic metrics with regional and temporal analysis"""
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    
    # Group by date and region
    monthly = df.groupby(["date", "region", "road_category"]).agg({
        "value": ["sum", "mean", "max", "count"]
    }).round(1)
    monthly.columns = ["traffic_sum", "traffic_mean", "traffic_max", "traffic_count"]
    monthly = monthly.reset_index()
    
    # Calculate monthly changes
    monthly["monthly_change_mean"] = monthly.groupby(["region", "road_category"])["traffic_mean"].pct_change() * 100
    monthly["monthly_change_mean"] = monthly["monthly_change_mean"].fillna(0).round(1)
    
    # Add date components
    monthly["year"] = monthly["date"].dt.year
    monthly["month"] = monthly["date"].dt.month
    
    return monthly


def build_entur_metrics(df):
    """Build public transport punctuality metrics"""
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    
    # Group by date and region
    monthly = df.groupby(["date", "region", "operator"]).agg({
        "scheduled_trips": ["sum", "mean"],
        "on_time_trips": ["sum", "mean"], 
        "delayed_trips": ["sum", "mean"],
        "avg_delay_minutes": ["mean", "max"],
        "punctuality_rate": ["mean", "min", "max"],
        "passenger_impact_score": ["mean", "sum"]
    }).round(1)
    
    # Flatten column names
    monthly.columns = [
        "scheduled_trips_total", "scheduled_trips_mean",
        "on_time_trips_total", "on_time_trips_mean",
        "delayed_trips_total", "delayed_trips_mean", 
        "avg_delay_mean", "avg_delay_max",
        "punctuality_rate_mean", "punctuality_rate_min", "punctuality_rate_max",
        "passenger_impact_mean", "passenger_impact_total"
    ]
    monthly = monthly.reset_index()
    
    # Calculate monthly improvements
    monthly["punctuality_improvement"] = monthly.groupby(["region", "operator"])["punctuality_rate_mean"].diff()
    monthly["punctuality_improvement"] = monthly["punctuality_improvement"].fillna(0).round(1)
    
    # Add date components
    monthly["year"] = monthly["date"].dt.year
    monthly["month"] = monthly["date"].dt.month
    monthly["season"] = monthly["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring", 
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn"
    })
    
    return monthly


def build_geonorge_metrics(df):
    """Build geographic KPI metrics by county/kommune"""
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    
    # Group by date and geographic region
    monthly = df.groupby(["date", "county_name", "kommune_name"]).agg({
        "population_density": ["mean", "max"],
        "road_network_km": ["sum", "mean"],
        "green_area_pct": ["mean"],
        "urban_development_index": ["mean", "max"],
        "transport_accessibility_score": ["mean"],
        "economic_activity_index": ["mean"],
        "infrastructure_quality_score": ["mean"],
        "environmental_quality_index": ["mean"],
        "regional_connectivity_score": ["mean"]
    }).round(1)
    
    # Flatten column names
    monthly.columns = [
        "population_density_mean", "population_density_max",
        "road_network_total", "road_network_mean", 
        "green_area_pct_mean",
        "urban_development_mean", "urban_development_max",
        "transport_accessibility_mean",
        "economic_activity_mean", 
        "infrastructure_quality_mean",
        "environmental_quality_mean",
        "regional_connectivity_mean"
    ]
    monthly = monthly.reset_index()
    
    # Calculate development rates
    monthly["urban_development_rate"] = monthly.groupby(["county_name", "kommune_name"])["urban_development_mean"].pct_change() * 100
    monthly["urban_development_rate"] = monthly["urban_development_rate"].fillna(0).round(1)
    
    # Add date components
    monthly["year"] = monthly["date"].dt.year
    monthly["month"] = monthly["date"].dt.month
    
    return monthly


def main():
    parser = argparse.ArgumentParser(description="Process Norwegian transportation datasets")
    parser.add_argument("--dataset", 
                       choices=["ev", "traffic", "entur", "geonorge", "both", "all"], 
                       default="all",
                       help="Which dataset to process")
    args = parser.parse_args()
    
    processed_dir = Path(__file__).resolve().parents[2] / "data" / "processed"
    processed_dir.mkdir(exist_ok=True)
    
    if args.dataset in ["ev", "both", "all"]:
        # Process EV data
        df_ev = load_raw("norwegian_ev_registrations.csv")
        metrics_ev = build_ev_metrics(df_ev)
        ev_out = processed_dir / "ev_metrics.csv"
        metrics_ev.to_csv(ev_out, index=False)
        print(f"EV data: Wrote {ev_out} ({len(metrics_ev)} rows)")
    
    if args.dataset in ["traffic", "both", "all"]:
        # Process traffic data
        df_traffic = load_raw("norwegian_traffic_nvdb.csv")
        metrics_traffic = build_traffic_metrics(df_traffic)
        traffic_out = processed_dir / "traffic_metrics.csv"
        metrics_traffic.to_csv(traffic_out, index=False)
        print(f"Traffic data: Wrote {traffic_out} ({len(metrics_traffic)} rows)")
    
    if args.dataset in ["entur", "all"]:
        # Process Entur data
        df_entur = load_raw("norwegian_entur_punctuality.csv")
        metrics_entur = build_entur_metrics(df_entur)
        entur_out = processed_dir / "entur_metrics.csv"
        metrics_entur.to_csv(entur_out, index=False)
        print(f"Entur data: Wrote {entur_out} ({len(metrics_entur)} rows)")
    
    if args.dataset in ["geonorge", "all"]:
        # Process Geonorge data
        df_geonorge = load_raw("norwegian_geonorge_kpis.csv")
        metrics_geonorge = build_geonorge_metrics(df_geonorge)
        geonorge_out = processed_dir / "geonorge_metrics.csv"
        metrics_geonorge.to_csv(geonorge_out, index=False)
        print(f"Geonorge data: Wrote {geonorge_out} ({len(metrics_geonorge)} rows)")


if __name__ == "__main__":
    main()