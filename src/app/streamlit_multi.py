import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

def display_ev_analysis(df):
    """Display EV registration analysis"""
    st.markdown("## ⚡ Electric Vehicle Registration Analysis")
    
    # EV Filters
    col1, col2 = st.columns(2)
    with col1:
        years = sorted(df["year"].unique().tolist())
        year_sel = st.multiselect("📅 Select Years", years, default=years, key="ev_years")
    with col2:
        if "season" in df.columns:
            seasons = df["season"].unique().tolist()
            season_sel = st.multiselect("🌍 Select Seasons", seasons, default=seasons, key="ev_seasons")
        else:
            season_sel = []
    
    # Filter EV data
    df_f = df[df["year"].isin(year_sel)] if year_sel else df.copy()
    if season_sel and "season" in df.columns:
        df_f = df_f[df_f["season"].isin(season_sel)]
    
    # EV Key Metrics
    st.markdown("### 📈 Key EV Adoption Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_evs = df_f["ev_registrations_total"].sum() if "ev_registrations_total" in df_f.columns else 0
        st.metric("🚗 Total EV Registrations", f"{total_evs:,.0f}")
    with col2:
        avg_monthly = df_f["ev_registrations_mean"].mean() if "ev_registrations_mean" in df_f.columns else 0
        st.metric("📊 Avg Monthly Registrations", f"{avg_monthly:,.0f}")
    with col3:
        if "monthly_growth_rate" in df_f.columns:
            avg_growth = df_f["monthly_growth_rate"].mean()
            st.metric("📈 Avg Monthly Growth", f"{avg_growth:.1f}%")
        else:
            st.metric("📈 Data Points", f"{len(df_f):,}")
    with col4:
        latest_evs = df_f["ev_registrations_total"].iloc[-1] if len(df_f) > 0 and "ev_registrations_total" in df_f.columns else 0
        st.metric("🆕 Latest Month Total", f"{latest_evs:,.0f}")
    
    # EV Visualizations
    col1, col2 = st.columns(2)
    with col1:
        if "ev_registrations_total" in df_f.columns:
            fig1 = px.line(
                df_f,
                x="date",
                y="ev_registrations_total", 
                title="📊 Cumulative EV Registrations in Oslo (2020-2024)",
                labels={"ev_registrations_total": "Total EV Registrations", "date": "Date"}
            )
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        if "monthly_growth_rate" in df_f.columns:
            fig2 = px.bar(
                df_f,
                x="date",
                y="monthly_growth_rate",
                title="📈 Monthly EV Growth Rate (%)",
                color="monthly_growth_rate",
                color_continuous_scale="RdYlGn"
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    # EV Seasonal Analysis
    if "season" in df_f.columns and "ev_registrations_total" in df_f.columns:
        st.markdown("### 🌍 Seasonal EV Adoption Patterns")
        seasonal_data = df_f.groupby("season")["ev_registrations_total"].mean().reset_index()
        
        fig3 = px.pie(
            seasonal_data,
            values="ev_registrations_total",
            names="season", 
            title="🍂 Average EV Registrations by Season",
            color_discrete_map={
                "Spring": "#90EE90",
                "Summer": "#FFD700", 
                "Autumn": "#FFA500",
                "Winter": "#87CEEB"
            }
        )
        st.plotly_chart(fig3, use_container_width=True)

    # EV Insights
    st.markdown("### 🔍 EV Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **🇳🇴 Norwegian EV Leadership**
        - Norway leads the world in EV adoption per capita
        - Strong government incentives drive rapid growth
        - Oslo shows particularly high adoption rates
        """)
    with col2:
        st.success("""
        **📊 EV Trends Observed**
        - Consistent upward trajectory in registrations
        - Seasonal variations in adoption patterns  
        - Accelerating growth year-over-year
        """)

def display_traffic_analysis(df):
    """Display traffic analysis from NVDB data"""
    st.markdown("## 🚦 Traffic Analytics (NVDB)")
    
    # Traffic Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        years = sorted(df["year"].unique().tolist())
        year_sel = st.multiselect("📅 Select Years", years, default=years, key="traffic_years")
    with col2:
        if "region" in df.columns:
            regions = df["region"].unique().tolist()
            region_sel = st.multiselect("🏙️ Select Regions", regions, default=regions, key="traffic_regions")
        else:
            region_sel = []
    with col3:
        if "road_category" in df.columns:
            road_types = df["road_category"].unique().tolist()
            road_sel = st.multiselect("🛣️ Select Road Types", road_types, default=road_types, key="traffic_roads")
        else:
            road_sel = []
    
    # Filter traffic data
    df_f = df[df["year"].isin(year_sel)] if year_sel else df.copy()
    if region_sel and "region" in df.columns:
        df_f = df_f[df_f["region"].isin(region_sel)]
    if road_sel and "road_category" in df.columns:
        df_f = df_f[df_f["road_category"].isin(road_sel)]
    
    # Traffic Key Metrics
    st.markdown("### 🚦 Key Traffic Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if "traffic_sum" in df_f.columns:
            total_traffic = df_f["traffic_sum"].sum()
            st.metric("🚗 Total Traffic Volume", f"{total_traffic:,.0f}")
        else:
            st.metric("📊 Data Points", f"{len(df_f):,}")
    with col2:
        if "traffic_mean" in df_f.columns:
            avg_daily = df_f["traffic_mean"].mean()
            st.metric("📊 Avg Daily Traffic", f"{avg_daily:,.0f}")
        else:
            st.metric("📊 Regions", f"{df_f['region'].nunique() if 'region' in df_f.columns else 'N/A'}")
    with col3:
        if "monthly_change_mean" in df_f.columns:
            avg_change = df_f["monthly_change_mean"].mean()
            st.metric("📈 Avg Monthly Change", f"{avg_change:.1f}%")
        else:
            st.metric("🛣️ Road Types", f"{df_f['road_category'].nunique() if 'road_category' in df_f.columns else 'N/A'}")
    with col4:
        if "traffic_max" in df_f.columns:
            peak_traffic = df_f["traffic_max"].max()
            st.metric("🔝 Peak Daily Traffic", f"{peak_traffic:,.0f}")
        else:
            st.metric("⏰ Time Span", f"{df_f['year'].max() - df_f['year'].min() + 1} years" if len(df_f) > 0 else "N/A")
    
    # Traffic Visualizations
    col1, col2 = st.columns(2)
    with col1:
        if "traffic_mean" in df_f.columns and "region" in df_f.columns:
            fig1 = px.line(
                df_f,
                x="date",
                y="traffic_mean",
                color="region",
                title="🚦 Average Daily Traffic by Region",
                labels={"traffic_mean": "Average Daily Traffic", "date": "Date", "region": "Region"}
            )
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        if "monthly_change_mean" in df_f.columns and "region" in df_f.columns:
            fig2 = px.bar(
                df_f,
                x="date",
                y="monthly_change_mean",
                color="region",
                title="📈 Monthly Traffic Changes (%)",
                labels={"monthly_change_mean": "Monthly Change (%)", "date": "Date", "region": "Region"}
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Regional Analysis
    if "region" in df_f.columns and "traffic_mean" in df_f.columns:
        st.markdown("### 🏙️ Regional & Road Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            regional_data = df_f.groupby("region")["traffic_mean"].mean().reset_index()
            fig3 = px.pie(
                regional_data,
                values="traffic_mean",
                names="region", 
                title="🚦 Average Daily Traffic by Region"
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            if "road_category" in df_f.columns:
                road_data = df_f.groupby("road_category")["traffic_mean"].mean().reset_index()
                fig4 = px.bar(
                    road_data,
                    x="road_category",
                    y="traffic_mean",
                    title="📊 Average Traffic by Road Type",
                    color="traffic_mean",
                    color_continuous_scale="Blues"
                )
                st.plotly_chart(fig4, use_container_width=True)

    # Traffic Insights
    st.markdown("### 🔍 Traffic Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **🇳🇴 NVDB Data Insights**
        - National Road Database provides comprehensive monitoring
        - E6 (European route) shows higher volumes than regional roads
        - Oslo consistently higher traffic than Bergen
        """)
    with col2:
        st.success("""
        **📊 Traffic Trends Observed**
        - Seasonal variations with summer peaks
        - COVID-19 impact visible in 2020
        - Recovery and growth in subsequent years
        """)

def display_combined_analysis(ev_df, traffic_df):
    """Display combined analysis of both datasets"""
    st.markdown("## 📊 Combined Transportation Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚡ EV Registration Summary")
        if "ev_registrations_total" in ev_df.columns:
            total_evs = ev_df["ev_registrations_total"].sum()
            latest_evs = ev_df["ev_registrations_total"].iloc[-1]
            st.metric("Total EV Registrations", f"{total_evs:,.0f}")
            st.metric("Latest Month", f"{latest_evs:,.0f}")
            
            # Quick EV trend
            fig_ev = px.line(ev_df.tail(12), x="date", y="ev_registrations_total", 
                           title="EV Registrations (Last 12 Months)")
            st.plotly_chart(fig_ev, use_container_width=True)
    
    with col2:
        st.markdown("### 🚦 Traffic Summary")
        if "traffic_mean" in traffic_df.columns:
            avg_traffic = traffic_df["traffic_mean"].mean()
            peak_traffic = traffic_df["traffic_max"].max() if "traffic_max" in traffic_df.columns else 0
            st.metric("Average Daily Traffic", f"{avg_traffic:,.0f}")
            st.metric("Peak Traffic", f"{peak_traffic:,.0f}")
            
            # Quick traffic trend
            fig_traffic = px.line(traffic_df.tail(12), x="date", y="traffic_mean", 
                                color="region" if "region" in traffic_df.columns else None,
                                title="Traffic Trends (Last 12 Months)")
            st.plotly_chart(fig_traffic, use_container_width=True)
    
    st.markdown("### 🔄 Cross-Analysis Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **EV Growth Trends**
        - Rapid EV adoption in Oslo
        - Strong seasonal patterns
        - Government incentives driving growth
        """)
    with col2:
        st.success("""
        **Traffic Patterns**  
        - Regional variations (Oslo vs Bergen)
        - COVID-19 impact in 2020
        - Road category differences
        """)

# Main Streamlit App
st.set_page_config(
    page_title="Norwegian Transportation Analytics Dashboard", 
    layout="wide",
    page_icon="🚗"
)

st.title("🇳🇴 Norwegian Transportation Analytics Dashboard")
st.markdown("**Multi-dataset analysis: EV Registrations + NVDB Traffic Data**")

# Dataset selection
st.sidebar.header("📊 Select Analysis")
analysis_type = st.sidebar.selectbox(
    "Choose your analysis:",
    ["🚗 EV Registration Analytics", "🚦 Traffic Analytics (NVDB)", "📊 Combined Overview"]
)

# File paths
TRAFFIC_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "traffic_metrics.csv"
EV_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "ev_metrics.csv"

# Sidebar info based on selected analysis
with st.sidebar:
    if analysis_type == "🚗 EV Registration Analytics":
        st.header("📊 EV Registration Data")
        st.write("**Data source**: Norwegian EV registrations")
        st.write("**Geographic focus**: Oslo region")
        st.write("**Time period**: 2020-2024")
        st.write("**Vehicle type**: Personal electric vehicles")
        st.info("⚡ Analyze Norway's world-leading EV adoption trends")
    elif analysis_type == "🚦 Traffic Analytics (NVDB)":
        st.header("📊 NVDB Traffic Data")
        st.write("**Data source**: National Road Database")
        st.write("**Geographic focus**: Oslo & Bergen")
        st.write("**Roads**: E6, Rv7")
        st.write("**Measurement**: Daily traffic counts")
        st.info("🚦 Analyze traffic patterns from official road data")
    else:
        st.header("📊 Multi-Dataset Analysis")
        st.write("**EV Data**: Registration trends")
        st.write("**Traffic Data**: NVDB road counts")
        st.write("**Combined insights**: Transportation patterns")
        st.info("🔄 Compare multiple transportation datasets")

# Load appropriate dataset based on selection
if analysis_type == "🚗 EV Registration Analytics":
    if not EV_PATH.exists():
        st.warning("EV data not found. Please run: `python -m src.analysis.prepare_multi --dataset ev`")
        st.stop()
    df = pd.read_csv(EV_PATH)
    df["date"] = pd.to_datetime(df["date"])
    st.success(f"✅ Loaded {len(df)} months of Norwegian EV registration data")
    display_ev_analysis(df)

elif analysis_type == "🚦 Traffic Analytics (NVDB)":
    if not TRAFFIC_PATH.exists():
        st.warning("Traffic data not found. Please run: `python -m src.analysis.prepare_multi --dataset traffic`")
        st.stop()
    df = pd.read_csv(TRAFFIC_PATH)
    df["date"] = pd.to_datetime(df["date"])
    st.success(f"✅ Loaded {len(df)} months of Norwegian traffic data from NVDB")
    display_traffic_analysis(df)

else:  # Combined overview
    ev_exists = EV_PATH.exists()
    traffic_exists = TRAFFIC_PATH.exists()
    
    if ev_exists and traffic_exists:
        ev_df = pd.read_csv(EV_PATH)
        traffic_df = pd.read_csv(TRAFFIC_PATH)
        ev_df["date"] = pd.to_datetime(ev_df["date"])
        traffic_df["date"] = pd.to_datetime(traffic_df["date"])
        st.success(f"✅ Loaded EV data ({len(ev_df)} months) + Traffic data ({len(traffic_df)} months)")
        display_combined_analysis(ev_df, traffic_df)
    else:
        missing = []
        if not ev_exists:
            missing.append("EV data")
        if not traffic_exists:
            missing.append("Traffic data")
        st.warning(f"Missing: {', '.join(missing)}. Please run: `python -m src.analysis.prepare_multi --dataset both`")
        st.stop()

# Footer
st.markdown("---")
st.caption("📊 Data sources: Norwegian EV registrations (Oslo) + NVDB (National Road Database) | 🔧 Built with Streamlit & Plotly")