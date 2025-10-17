import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Norwegian Traffic Analytics Dashboard", 
    layout="wide",
    page_icon="�"
)
st.title("🇳🇴 Norwegian Traffic Analytics Dashboard (NVDB)")
st.markdown("**Real-world traffic insights from the National Road Database (Nasjonal vegdatabase)**")

DATA_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "traffic_metrics.csv"
)

with st.sidebar:
    st.header("📊 NVDB Traffic Data")
    st.write("**Data source**: National Road Database (NVDB)")
    st.write("**Geographic focus**: Oslo & Bergen")
    st.write("**Time period**: 2020-2024")
    st.write("**Roads**: E6 (European route), Rv7 (National road)")
    st.write("**Measurement**: Annual Average Daily Traffic (AAR_TRAFFIC)")
    st.markdown("---")
    st.info("� This dashboard analyzes Norwegian traffic patterns from official road data")

if not DATA_PATH.exists():
    st.warning("No processed dataset found. Please run the pipeline (see README).")
    st.stop()

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])
st.success(f"✅ Loaded {len(df)} months of Norwegian traffic data from NVDB")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    years = sorted(df["year"].unique().tolist())
    year_sel = st.multiselect("📅 Select Years", years, default=years)
with col2:
    if "region" in df.columns:
        regions = df["region"].unique().tolist()
        region_sel = st.multiselect("�️ Select Regions", regions, default=regions)
    else:
        region_sel = []
with col3:
    if "road_category" in df.columns:
        road_types = df["road_category"].unique().tolist()
        road_sel = st.multiselect("🛣️ Select Road Types", road_types, default=road_types)
    else:
        road_sel = []

# Filter data
df_f = df[df["year"].isin(year_sel)] if year_sel else df.copy()
if region_sel and "region" in df.columns:
    df_f = df_f[df_f["region"].isin(region_sel)]
if road_sel and "road_category" in df.columns:
    df_f = df_f[df_f["road_category"].isin(road_sel)]

# Key Metrics
st.markdown("## � Key Traffic Metrics")
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
        st.metric("�️ Road Types", f"{df_f['road_category'].nunique() if 'road_category' in df_f.columns else 'N/A'}")

with col4:
    if "traffic_max" in df_f.columns:
        peak_traffic = df_f["traffic_max"].max()
        st.metric("🔝 Peak Daily Traffic", f"{peak_traffic:,.0f}")
    else:
        st.metric("⏰ Time Span", f"{df_f['year'].max() - df_f['year'].min() + 1} years" if len(df_f) > 0 else "N/A")

# Main visualizations
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 📈 Traffic Volume Trends")
    if "traffic_mean" in df_f.columns and "region" in df_f.columns:
        fig1 = px.line(
            df_f,
            x="date",
            y="traffic_mean",
            color="region",
            title="� Average Daily Traffic by Region (NVDB Data)",
            labels={
                "traffic_mean": "Average Daily Traffic",
                "date": "Date",
                "region": "Region"
            }
        )
        fig1.update_layout(
            xaxis_title="Timeline",
            yaxis_title="Average Daily Traffic Count",
            hovermode="x unified"
        )
        st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("## 📊 Traffic Changes")
    if "monthly_change_mean" in df_f.columns and "region" in df_f.columns:
        fig2 = px.bar(
            df_f,
            x="date",
            y="monthly_change_mean",
            color="region",
            title="📈 Monthly Traffic Changes (%)",
            labels={
                "monthly_change_mean": "Monthly Change (%)",
                "date": "Date",
                "region": "Region"
            }
        )
        fig2.update_layout(
            xaxis_title="Timeline", 
            yaxis_title="Monthly Change (%)",
            barmode="group"
        )
        st.plotly_chart(fig2, use_container_width=True)

# Regional & Road Type Analysis
col1, col2 = st.columns(2)

with col1:
    if "region" in df_f.columns and "traffic_mean" in df_f.columns:
        st.markdown("## �️ Traffic by Region")
        regional_data = df_f.groupby("region")["traffic_mean"].mean().reset_index()
        
        fig3 = px.pie(
            regional_data,
            values="traffic_mean",
            names="region", 
            title="🚦 Average Daily Traffic by Region",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig3, use_container_width=True)

with col2:
    if "road_category" in df_f.columns and "traffic_mean" in df_f.columns:
        st.markdown("## 🛣️ Traffic by Road Category")
        road_data = df_f.groupby("road_category")["traffic_mean"].mean().reset_index()
        
        fig4 = px.bar(
            road_data,
            x="road_category",
            y="traffic_mean",
            title="📊 Average Traffic by Road Type",
            color="traffic_mean",
            color_continuous_scale="Blues",
            labels={"traffic_mean": "Average Daily Traffic", "road_category": "Road Category"}
        )
        st.plotly_chart(fig4, use_container_width=True)

# Seasonal Analysis
if "season" in df_f.columns and "traffic_mean" in df_f.columns:
    st.markdown("## 🌍 Seasonal Traffic Patterns")
    seasonal_data = df_f.groupby(["season", "region"])["traffic_mean"].mean().reset_index()
    
    fig5 = px.bar(
        seasonal_data,
        x="season",
        y="traffic_mean",
        color="region",
        title="🍂 Seasonal Traffic Patterns by Region",
        labels={"traffic_mean": "Average Daily Traffic", "season": "Season"},
        barmode="group"
    )
    st.plotly_chart(fig5, use_container_width=True)

# Traffic Intensity Analysis
if "traffic_intensity" in df_f.columns:
    st.markdown("## 🚦 Traffic Intensity Categories")
    intensity_data = df_f["traffic_intensity"].value_counts().reset_index()
    intensity_data.columns = ["intensity", "count"]
    
    fig6 = px.bar(
        intensity_data,
        x="intensity",
        y="count",
        title="📊 Distribution of Traffic Intensity Levels",
        color="intensity",
        color_discrete_map={
            "Low": "#90EE90",
            "Medium": "#FFD700", 
            "High": "#FFA500",
            "Very High": "#FF6B6B"
        }
    )
    st.plotly_chart(fig6, use_container_width=True)

# Insights
st.markdown("## 🔍 Key Traffic Insights")
col1, col2 = st.columns(2)

with col1:
    st.info("""
    **🇳🇴 NVDB Data Insights**
    - National Road Database provides comprehensive traffic monitoring
    - E6 (European route) shows higher traffic volumes than regional roads
    - Oslo consistently has higher traffic density than Bergen
    - Data includes Annual Average Daily Traffic (AAR_TRAFFIC)
    """)

with col2:
    st.success("""
    **📊 Traffic Trends Observed**
    - Seasonal variations with summer peaks typical
    - COVID-19 impact visible in 2020 data
    - Recovery and growth in subsequent years
    - Regional differences reflect urban density patterns
    """)

# NVDB Information
st.markdown("## 📋 About NVDB (Nasjonal vegdatabase)")
st.markdown("""
The **National Road Database (NVDB)** is Norway's comprehensive database containing information about 
state, county, municipal, and private roads. Key features:

- **Comprehensive Coverage**: All Norwegian roads with detailed metadata
- **Real-time Updates**: Continuous monitoring and data collection
- **Open Access**: Public API available for analysis and research
- **Traffic Counting**: Automated traffic counting stations across the network
- **Incident Tracking**: Road conditions, maintenance, and traffic incidents
""")

st.markdown("---")
st.caption("📊 Data source: NVDB (Nasjonal vegdatabank) - Norwegian National Road Database | 🔧 Built with Streamlit & Plotly")
