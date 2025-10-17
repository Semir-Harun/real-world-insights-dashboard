# Real-World Data Insights Dashboard

A professional, portfolio-ready **Python data analysis + Streamlit dashboard** showcasing real-world insights with clean structure, tests, and CI.

## Quickstart
```bash
git clone https://github.com/yourusername/real-world-insights-dashboard.git
cd real-world-insights-dashboard
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.data.download       # optional if DATA_URL is set
python -m src.analysis.prepare    # builds processed metrics
streamlit run src/app/streamlit_app.py
```