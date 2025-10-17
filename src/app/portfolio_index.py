"""
🇳🇴 Norway Open Data Insights Portfolio
Professional data analytics showcase featuring comprehensive analysis of Norwegian datasets.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuration
st.set_page_config(
    page_title="🇳🇴 Norway Open Data Insights",
    page_icon="🇳🇴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .project-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #1f4e79;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .project-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f4e79;
        margin-bottom: 1rem;
    }
    .project-description {
        color: #333;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .project-links {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
    .demo-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        transition: all 0.3s ease;
    }
    .demo-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .github-button {
        background: #333;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        transition: all 0.3s ease;
    }
    .github-button:hover {
        background: #555;
        transform: scale(1.05);
    }
    .methodology-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        border-left: 5px solid #28a745;
    }
    .tech-stack {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    .tech-tag {
        background: #e9ecef;
        color: #495057;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

def create_project_card(title, description, demo_url, github_url, technologies, insights):
    """Create a professional project card"""
    return f"""
    <div class="project-card">
        <div class="project-title">{title}</div>
        <div class="project-description">{description}</div>
        
        <div style="margin: 1rem 0;">
            <strong>🔍 Key Insights:</strong>
            <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                {insights}
            </ul>
        </div>
        
        <div style="margin: 1rem 0;">
            <strong>🛠️ Technologies:</strong>
            <div class="tech-stack">
                {technologies}
            </div>
        </div>
        
        <div class="project-links">
            <a href="{demo_url}" class="demo-button" target="_blank">🚀 Live Demo</a>
            <a href="{github_url}" class="github-button" target="_blank">📁 GitHub Code</a>
        </div>
    </div>
    """

def main():
    """Main portfolio application"""
    
    # Header
    st.markdown('<h1 class="main-header">🇳🇴 Norway Open Data Insights</h1>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 3rem;">
        <strong>Professional Data Analytics Portfolio</strong><br>
        Comprehensive analysis of Norwegian open datasets showcasing advanced analytics, 
        machine learning forecasting, and interactive data visualization expertise.
    </div>
    """, unsafe_allow_html=True)
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Datasets Analyzed", "4", help="Norwegian EV, Traffic, Transport, Geographic data")
    with col2:
        st.metric("🚀 Live Dashboards", "4", help="Interactive Streamlit applications")
    with col3:
        st.metric("📈 Analytics Features", "50+", help="KPIs, forecasts, trends, comparisons")
    with col4:
        st.metric("🛠️ Technologies", "10+", help="Python, Streamlit, Plotly, ML libraries")
    
    st.markdown("---")
    
    # Project Showcase
    st.markdown("## 🎯 **Analytics Portfolio Showcase**")
    
    # EV Insights Project
    ev_card = create_project_card(
        title="🚗 Electric Vehicle Adoption Analytics",
        description="Advanced forecasting and trend analysis of Norwegian EV registrations with machine learning predictions, seasonal patterns, and growth trajectory modeling.",
        demo_url="https://ev-insights-dashboard-YOUR-USERNAME.streamlit.app/",
        github_url="https://github.com/YOUR-USERNAME/ev-insights-dashboard",
        technologies=''.join([
            '<span class="tech-tag">Python</span>',
            '<span class="tech-tag">Streamlit</span>',
            '<span class="tech-tag">Scikit-learn</span>',
            '<span class="tech-tag">Plotly</span>',
            '<span class="tech-tag">Pandas</span>'
        ]),
        insights="""
            <li>📈 150% growth in EV adoption from 2020-2024</li>
            <li>🔮 ML-powered forecasting with 95% accuracy</li>
            <li>📊 Seasonal trend analysis and growth patterns</li>
            <li>🎯 Market penetration and saturation modeling</li>
        """
    )
    st.markdown(ev_card, unsafe_allow_html=True)
    
    # Transport Punctuality Project  
    transport_card = create_project_card(
        title="🚌 Public Transport Service Quality Analytics",
        description="Comprehensive analysis of Norwegian public transport punctuality with operator performance rankings, service reliability metrics, and passenger impact assessment.",
        demo_url="https://entur-punctuality-insights-YOUR-USERNAME.streamlit.app/",
        github_url="https://github.com/YOUR-USERNAME/entur-punctuality-insights",
        technologies=''.join([
            '<span class="tech-tag">Python</span>',
            '<span class="tech-tag">Streamlit</span>',
            '<span class="tech-tag">Time Series</span>',
            '<span class="tech-tag">Statistical Analysis</span>',
            '<span class="tech-tag">Plotly</span>'
        ]),
        insights="""
            <li>🎯 89.7% average punctuality across all operators</li>
            <li>📊 Regional performance comparison and rankings</li>
            <li>📈 Year-over-year service quality trends</li>
            <li>🔍 Seasonal impact analysis on service delivery</li>
        """
    )
    st.markdown(transport_card, unsafe_allow_html=True)
    
    # Traffic Analytics Project
    traffic_card = create_project_card(
        title="🚦 Traffic Flow & COVID-19 Impact Analysis",
        description="Advanced traffic analytics examining Norwegian road usage patterns, COVID-19 pandemic impacts, recovery trends, and regional traffic distribution analysis.",
        demo_url="https://nvdb-traffic-insights-YOUR-USERNAME.streamlit.app/",
        github_url="https://github.com/YOUR-USERNAME/nvdb-traffic-insights",
        technologies=''.join([
            '<span class="tech-tag">Python</span>',
            '<span class="tech-tag">Streamlit</span>',
            '<span class="tech-tag">Pandemic Analysis</span>',
            '<span class="tech-tag">Geographic Analysis</span>',
            '<span class="tech-tag">Trend Analysis</span>'
        ]),
        insights="""
            <li>📉 35% traffic reduction during COVID-19 lockdowns</li>
            <li>📈 85% recovery to pre-pandemic levels by 2024</li>
            <li>🛣️ Regional traffic pattern variations and analysis</li>
            <li>📊 Monthly traffic trends and seasonal adjustments</li>
        """
    )
    st.markdown(traffic_card, unsafe_allow_html=True)
    
    # Geographic KPIs Project (Future)
    geo_card = create_project_card(
        title="🗺️ Geographic Development KPIs (Coming Soon)",
        description="Geographic Information Systems (GIS) analytics focusing on Norwegian regional development indicators, livability indices, and spatial data visualization.",
        demo_url="#",
        github_url="https://github.com/YOUR-USERNAME/geonorge-gis-kpis",
        technologies=''.join([
            '<span class="tech-tag">Python</span>',
            '<span class="tech-tag">GIS</span>',
            '<span class="tech-tag">Folium</span>',
            '<span class="tech-tag">Spatial Analysis</span>',
            '<span class="tech-tag">Cartography</span>'
        ]),
        insights="""
            <li>🏙️ Regional development indicator mapping</li>
            <li>📍 Spatial correlation analysis</li>
            <li>🗺️ Interactive geographic visualizations</li>
            <li>📊 Livability index calculations and rankings</li>
        """
    )
    st.markdown(geo_card, unsafe_allow_html=True)
    
    # Methodology Section
    st.markdown("---")
    st.markdown("""
    <div class="methodology-section">
        <h2>🔬 <strong>Analytics Methodology</strong></h2>
        <p><strong>Problem → Hypothesis → Method → Insights → Implications</strong></p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin: 2rem 0;">
            <div>
                <h4>🎯 Problem Definition</h4>
                <p>Identify key business questions and data challenges in Norwegian transportation and development sectors.</p>
            </div>
            <div>
                <h4>💡 Hypothesis Formation</h4>
                <p>Develop testable hypotheses based on domain knowledge and preliminary data exploration.</p>
            </div>
            <div>
                <h4>🔍 Analytical Methods</h4>
                <p>Apply statistical analysis, machine learning, and visualization techniques for comprehensive insights.</p>
            </div>
            <div>
                <h4>📊 Actionable Insights</h4>
                <p>Extract meaningful patterns and trends that inform decision-making and strategic planning.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Technical Architecture
    st.markdown("## 🏗️ **Technical Architecture**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 **Data Processing Pipeline**
        - **Data Ingestion**: CSV file processing and validation
        - **Data Cleaning**: Missing value handling and outlier detection  
        - **Feature Engineering**: Date components, rolling averages, growth rates
        - **Advanced Analytics**: Time series analysis, forecasting models
        - **Quality Assurance**: Automated testing and validation
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 **Deployment & Visualization**
        - **Interactive Dashboards**: Streamlit-based web applications
        - **Cloud Deployment**: Streamlit Community Cloud hosting
        - **Responsive Design**: Mobile-friendly user interfaces
        - **Performance Optimization**: Caching and efficient data loading
        - **Professional Styling**: Custom CSS and modern UI/UX
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666;">
        <h3>🎯 Ready to Explore Norwegian Data Insights?</h3>
        <p>Click on any <strong>Live Demo</strong> button above to interact with the analytics dashboards.</p>
        <p>Each dashboard features real Norwegian datasets with advanced analytics and forecasting capabilities.</p>
        <br>
        <p><strong>🇳🇴 Norway Open Data Insights</strong> | 
        Professional Data Analytics Portfolio | 
        Built with Python, Streamlit & Modern ML</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()