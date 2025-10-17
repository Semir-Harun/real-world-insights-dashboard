# 🇳🇴 Norwegian Transportation Analytics Dashboard

A professional, portfolio-ready **multi-dataset Python analytics platform** showcasing **Norwegian transportation insights** with **Electric Vehicle adoption trends** and **National Road Database (NVDB) traffic patterns**. Features comprehensive time-series analysis, regional comparisons, and interactive Streamlit dashboards.

## 🚗 Multi-Dataset Analytics

### ⚡ **Electric Vehicle Registration Analytics**
- **Data Source**: Norwegian EV registrations (Oslo region, 2020-2024)
- **Analytics**: Cumulative growth trends, monthly adoption rates, seasonal patterns
- **Insights**: Norway's world-leading EV adoption, government incentive impact

### 🚦 **Traffic Analytics (NVDB)**
- **Data Source**: National Road Database (Oslo E6, Bergen Rv7, 2020-2024)
- **Analytics**: Daily traffic volumes, regional comparisons, COVID-19 impact analysis
- **Insights**: Infrastructure utilization, seasonal variations, road category patterns

## 🚀 Quick Start

### Option 1: Multi-Dataset Dashboard (Recommended)
```bash
git clone https://github.com/Semir-Harun/real-world-insights-dashboard.git
cd real-world-insights-dashboard
pip install -r requirements.txt

# Process both datasets
python -m src.analysis.prepare_multi --dataset both

# Launch multi-dataset dashboard
python -m streamlit run src/app/streamlit_multi.py
```

### Option 2: Individual Dataset Processing
```bash
# EV data only
python -m src.analysis.prepare_multi --dataset ev
python -m streamlit run src/app/streamlit_multi.py

# Traffic data only  
python -m src.analysis.prepare_multi --dataset traffic
python -m streamlit run src/app/streamlit_multi.py
```

## 📊 Dashboard Features

### 🚗 EV Registration Analytics
- **📈 Growth Metrics**: Cumulative registrations, monthly growth rates, YoY trends
- **🌍 Seasonal Analysis**: Spring/Summer/Autumn/Winter adoption patterns
- **🎯 Key Insights**: Norway's EV leadership, government incentive effectiveness
- **📊 Visualizations**: Time series charts, growth rate bars, seasonal pie charts

### 🚦 Traffic Analytics (NVDB)
- **📈 Volume Analysis**: Daily traffic counts, regional comparisons (Oslo vs Bergen)
- **🛣️ Road Categories**: E6 (European route) vs Rv7 (regional road) patterns  
- **📅 Temporal Trends**: Monthly changes, COVID-19 impact analysis
- **📊 Visualizations**: Multi-region line charts, road type comparisons, change rates

### 📊 Combined Analytics
- **🔄 Cross-Dataset Insights**: Transportation ecosystem overview
- **📈 Comparative Metrics**: EV adoption vs traffic volume trends
- **🎯 Portfolio Showcase**: Multiple analytical capabilities demonstration

## 🛠️ Technical Stack

- **🐍 Python 3.11+**: Core data processing and analytics
- **🎨 Streamlit**: Interactive web dashboard framework
- **📊 Plotly**: Professional-grade data visualizations
- **🐼 Pandas**: Time-series data manipulation and analysis
- **🔧 Ruff + Black**: Code quality and formatting
- **🧪 Pytest**: Unit testing and data validation

## 📁 Project Structure

```
real-world-insights-dashboard/
├── src/
│   ├── analysis/
│   │   ├── prepare.py          # Single dataset processor (legacy)
│   │   └── prepare_multi.py    # Multi-dataset processor ⭐
│   ├── app/
│   │   ├── streamlit_app.py    # Single dataset dashboard
│   │   └── streamlit_multi.py  # Multi-dataset dashboard ⭐
│   └── data/
│       └── download.py         # Data acquisition utilities
├── data/
│   ├── raw/
│   │   ├── norwegian_ev_registrations.csv    # EV data ⚡
│   │   └── norwegian_traffic_nvdb.csv        # Traffic data 🚦
│   └── processed/
│       ├── ev_metrics.csv      # Processed EV analytics
│       └── traffic_metrics.csv # Processed traffic analytics
├── notebooks/
│   └── eda.ipynb              # Exploratory data analysis
└── tests/
    └── test_metrics.py        # Unit tests
```

## 📈 Analytics Highlights

### ⚡ Norwegian EV Insights
- **World Leadership**: Norway leads global EV adoption per capita
- **Oslo Focus**: Capital region shows highest adoption rates  
- **Growth Trajectory**: Consistent upward trends across 2020-2024
- **Seasonal Patterns**: Spring/summer peaks in registration activity

### 🚦 NVDB Traffic Insights  
- **Infrastructure Monitoring**: Comprehensive road network analysis
- **Regional Variations**: Oslo (E6) vs Bergen (Rv7) traffic patterns
- **COVID-19 Impact**: Visible traffic reduction in 2020, subsequent recovery
- **Road Categories**: European routes show higher volumes than regional roads

## 🎯 Portfolio Value

This project demonstrates:
- **📊 Multi-dataset analytics**: Handling diverse transportation data sources
- **🔄 Data pipeline engineering**: Automated ETL with pandas and Python modules
- **🎨 Interactive visualization**: Professional Streamlit dashboards with Plotly
- **🇳🇴 Domain expertise**: Norwegian transportation sector knowledge
- **📈 Time-series analysis**: Growth calculations, seasonal decomposition
- **🛠️ Software engineering**: Clean code, testing, Git workflows

## 🚀 Getting Started

1. **Clone and Setup**:
   ```bash
   git clone https://github.com/Semir-Harun/real-world-insights-dashboard.git
   cd real-world-insights-dashboard
   pip install -r requirements.txt
   ```

2. **Process Data**:
   ```bash
   python -m src.analysis.prepare_multi --dataset both
   ```

3. **Launch Dashboard**:
   ```bash
   python -m streamlit run src/app/streamlit_multi.py
   ```

4. **Explore Analytics**: Navigate to `http://localhost:8501` and select:
   - 🚗 **EV Registration Analytics** for adoption trends
   - 🚦 **Traffic Analytics (NVDB)** for road patterns  
   - 📊 **Combined Overview** for cross-dataset insights

## 📝 Data Sources

- **EV Registrations**: Norwegian official statistics (Oslo region, 2020-2024)
- **NVDB Traffic**: National Road Database (E6 Oslo, Rv7 Bergen, 2020-2024)
- **Processing**: Monthly aggregations with growth calculations and seasonal analysis

---

**🎯 Portfolio Project**: Demonstrating multi-dataset Norwegian transportation analytics with professional Python data science workflows