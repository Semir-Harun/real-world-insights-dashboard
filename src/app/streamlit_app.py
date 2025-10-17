import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.set_page_config(page_title="Real-World Data Insights", layout="wide")
st.title("🔎 Real-World Data Insights Dashboard")

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "ev_metrics.csv"

with st.sidebar:
    st.header("Data")
    st.write("This app expects a processed CSV at: `data/processed/ev_metrics.csv`")
    st.write("Run the pipeline in README to generate it.")

if not DATA_PATH.exists():
    st.warning("No processed dataset found. Please run the pipeline (see README).")
    st.stop()

df = pd.read_csv(DATA_PATH)
st.success(f"Loaded {len(df)} rows from {DATA_PATH.name}")

years = sorted(df["year"].unique().tolist())
year_sel = st.multiselect("Year", years, default=years)
df_f = df[df["year"].isin(year_sel)] if year_sel else df.copy()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total (sum)", f"{df_f['value_sum'].sum():,.0f}")
col2.metric("Average monthly", f"{df_f['value_mean'].mean():,.2f}")
col3.metric("Median monthly", f"{df_f['value_median'].median():,.2f}")
col4.metric("Months counted", f"{int(df_f['value_count'].sum()):,}")

fig1 = px.line(df_f, x=pd.to_datetime(df_f["year"].astype(str) + "-" + df_f["month"].astype(str) + "-01"),
               y="value_sum", title="Monthly Total")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(df_f, x="month", y="value_mean", color="year", barmode="group", title="Monthly Mean by Year")
st.plotly_chart(fig2, use_container_width=True)

st.caption("Tip: Replace the pipeline with domain-specific metrics once you pick a dataset.")