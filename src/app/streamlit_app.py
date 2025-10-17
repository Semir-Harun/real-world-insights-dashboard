import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Norwegian EV Analytics Dashboard", 
    layout="wide",
    page_icon="🚗"
)
st.title("🇳🇴 Norwegian Electric Vehicle Analytics Dashboard")
st.markdown("**Real-world insights into Norway's EV adoption trends and patterns**")

DATA_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "ev_metrics.csv"
)

with st.sidebar:
    st.header("📊 Norwegian EV Data")
    st.write("**Data source**: Norwegian EV registrations")
    st.write("**Geographic focus**: Oslo region")
    st.write("**Time period**: 2020-2024")
    st.write("**Vehicle type**: Personal electric vehicles (personbil)")
    st.markdown("---")
    st.info("💡 This dashboard analyzes Norway's world-leading EV adoption trends")

if not DATA_PATH.exists():
    st.warning("No processed dataset found. Please run the pipeline (see README).")
    st.stop()

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])
st.success(f"✅ Loaded {len(df)} months of Norwegian EV registration data")

# Filters
col1, col2 = st.columns(2)
with col1:
    years = sorted(df["year"].unique().tolist())
    year_sel = st.multiselect("📅 Select Years", years, default=years)
with col2:
    if "season" in df.columns:
        seasons = df["season"].unique().tolist()
        season_sel = st.multiselect("🌍 Select Seasons", seasons, default=seasons)
    else:
        season_sel = []

# Filter data
df_f = df[df["year"].isin(year_sel)] if year_sel else df.copy()
if season_sel and "season" in df.columns:
    df_f = df_f[df_f["season"].isin(season_sel)]

# Key Metrics
st.markdown("## 📈 Key EV Adoption Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_evs = df_f["ev_registrations_total"].sum()
    st.metric("🚗 Total EV Registrations", f"{total_evs:,.0f}")

with col2:
    avg_monthly = df_f["ev_registrations_mean"].mean()
    st.metric("📊 Avg Monthly Registrations", f"{avg_monthly:,.0f}")

with col3:
    if "monthly_growth_rate" in df_f.columns:
        avg_growth = df_f["monthly_growth_rate"].mean()
        st.metric("📈 Avg Monthly Growth", f"{avg_growth:.1f}%")
    else:
        st.metric("📈 Data Points", f"{len(df_f):,}")

with col4:
    latest_registrations = df_f["ev_registrations_total"].iloc[-1] if len(df_f) > 0 else 0
    st.metric("🆕 Latest Month Total", f"{latest_registrations:,.0f}")

# Main visualizations
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 📈 EV Registration Growth Trend")
    fig1 = px.line(
        df_f,
        x="date",
        y="ev_registrations_total", 
        title="📊 Cumulative EV Registrations in Oslo (2020-2024)",
        labels={
            "ev_registrations_total": "Total EV Registrations",
            "date": "Date"
        }
    )
    fig1.update_layout(
        xaxis_title="Timeline",
        yaxis_title="Total EV Registrations",
        hovermode="x unified"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("## 📊 Monthly Growth Rate")
    if "monthly_growth_rate" in df_f.columns:
        fig2 = px.bar(
            df_f,
            x="date",
            y="monthly_growth_rate",
            title="📈 Monthly Growth Rate (%)",
            color="monthly_growth_rate",
            color_continuous_scale="RdYlGn",
            labels={
                "monthly_growth_rate": "Growth Rate (%)",
                "date": "Date"
            }
        )
        fig2.update_layout(
            xaxis_title="Timeline", 
            yaxis_title="Monthly Growth Rate (%)",
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

# Seasonal Analysis
if "season" in df_f.columns:
    st.markdown("## 🌍 Seasonal EV Adoption Patterns")
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

# Year-over-Year Comparison  
st.markdown("## 📅 Year-over-Year Analysis")
yearly_data = df_f.groupby("year")["ev_registrations_total"].agg(["min", "max", "mean"]).reset_index()
yearly_data["growth"] = yearly_data["max"] - yearly_data["min"]

fig4 = px.bar(
    yearly_data,
    x="year",
    y="growth", 
    title="🚀 Annual EV Registration Growth",
    color="growth",
    color_continuous_scale="Viridis",
    labels={"growth": "Annual Growth", "year": "Year"}
)
st.plotly_chart(fig4, use_container_width=True)

# Insights
st.markdown("## 🔍 Key Insights")
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
    **📊 Data Trends Observed**
    - Consistent upward trajectory in registrations
    - Seasonal variations in adoption patterns  
    - Accelerating growth year-over-year
    """)

st.markdown("---")
st.caption("📊 Data source: Norwegian EV registrations (Oslo region) | 🔧 Built with Streamlit & Plotly")
