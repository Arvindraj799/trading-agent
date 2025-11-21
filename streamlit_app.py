import streamlit as st
import pandas as pd
import datetime
import json
import os
from typing import Dict, Any, Optional
import traceback

# Handle optional imports gracefully
try:
    from dotenv import load_dotenv
except ImportError:
    st.warning("python-dotenv not available. Environment variables must be set manually.")
    def load_dotenv():
        pass

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    st.error("Plotly not available. Charts will be disabled.")
    PLOTLY_AVAILABLE = False
    go = None
    px = None

# Load environment variables
load_dotenv()

# Import TradingAgents components
try:
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG
    TRADINGAGENTS_AVAILABLE = True
except ImportError as e:
    st.error(f"TradingAgents import error: {e}")
    TRADINGAGENTS_AVAILABLE = False
    class TradingAgentsGraph:
        pass
    DEFAULT_CONFIG = {}

# Import utility functions with fallback
try:
    from streamlit_utils import (
        create_stock_chart, create_volume_chart, get_stock_info,
        create_metrics_dashboard, create_risk_gauge, create_sentiment_pie_chart,
        export_analysis_to_json, display_config_summary, validate_configuration,
        format_currency, format_percentage
    )
    UTILS_AVAILABLE = True
except ImportError as e:
    st.error(f"Streamlit utilities not available: {e}. Some features will be disabled.")
    UTILS_AVAILABLE = False
    # Create dummy functions
    def create_stock_chart(*args, **kwargs): return None
    def create_volume_chart(*args, **kwargs): return None
    def get_stock_info(*args, **kwargs): return {}
    def create_metrics_dashboard(*args, **kwargs): pass
    def create_risk_gauge(*args, **kwargs): return None
    def create_sentiment_pie_chart(*args, **kwargs): return None
    def export_analysis_to_json(*args, **kwargs): return ""
    def display_config_summary(*args, **kwargs): pass
    def validate_configuration(*args, **kwargs): return []
    def format_currency(value): return f"${value:.2f}"
    def format_percentage(value): return f"{value:.2f}%"

# Page configuration
st.set_page_config(
    page_title="TradingAgents - Multi-Agent Trading Framework",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1f4e79 0%, #2e7d9a 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .report-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid #007bff;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None
    if 'analysis_running' not in st.session_state:
        st.session_state.analysis_running = False
    if 'config' not in st.session_state:
        st.session_state.config = DEFAULT_CONFIG.copy()

def create_sidebar():
    """Create the configuration sidebar"""
    st.sidebar.title("⚙️ Configuration")
    
    # API Keys status (read-only display)
    openai_key_set = bool(os.getenv("OPENAI_API_KEY"))
    alpha_vantage_key_set = bool(os.getenv("ALPHA_VANTAGE_API_KEY"))
    
    if openai_key_set and alpha_vantage_key_set:
        st.sidebar.success("✅ API Keys Configured")
        st.sidebar.info("🔒 Keys loaded from environment")
    else:
        st.sidebar.error("❌ API Keys Missing")
        st.sidebar.warning("⚠️ Please configure API keys in environment variables")
    
    # LLM Configuration
    st.sidebar.subheader("🤖 LLM Settings")
    
    llm_provider = st.sidebar.selectbox(
        "LLM Provider",
        ["openai", "anthropic", "google"],
        index=0,
        help="Choose your LLM provider"
    )
    
    deep_think_model = st.sidebar.selectbox(
        "Deep Thinking Model",
        ["o1-preview", "o1-mini", "gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet-20241022"],
        index=3,
        help="Model for complex reasoning tasks"
    )
    
    quick_think_model = st.sidebar.selectbox(
        "Quick Thinking Model", 
        ["gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet-20241022"],
        index=1,
        help="Model for rapid inference tasks"
    )
    
    # Analysis Configuration
    st.sidebar.subheader("🔍 Analysis Settings")
    
    selected_analysts = st.sidebar.multiselect(
        "Select Analysts",
        ["market", "social", "news", "fundamentals"],
        default=["market", "social", "news", "fundamentals"],
        help="Choose which analysts to include in the analysis"
    )
    
    max_debate_rounds = st.sidebar.slider(
        "Max Debate Rounds",
        min_value=1,
        max_value=5,
        value=1,
        help="Number of debate rounds between researchers"
    )
    
    max_risk_rounds = st.sidebar.slider(
        "Max Risk Discussion Rounds",
        min_value=1,
        max_value=5, 
        value=1,
        help="Number of risk assessment rounds"
    )
    
    # Data Vendor Configuration
    st.sidebar.subheader("📊 Data Vendors")
    
    core_stock_vendor = st.sidebar.selectbox(
        "Stock Data",
        ["yfinance", "alpha_vantage"],
        index=0
    )
    
    technical_vendor = st.sidebar.selectbox(
        "Technical Indicators",
        ["yfinance", "alpha_vantage"],
        index=0
    )
    
    fundamental_vendor = st.sidebar.selectbox(
        "Fundamental Data",
        ["alpha_vantage", "openai"],
        index=0
    )
    
    news_vendor = st.sidebar.selectbox(
        "News Data",
        ["alpha_vantage", "openai", "google"],
        index=0
    )
    
    # Update session state config
    st.session_state.config.update({
        "llm_provider": llm_provider,
        "deep_think_llm": deep_think_model,
        "quick_think_llm": quick_think_model,
        "max_debate_rounds": max_debate_rounds,
        "max_risk_discuss_rounds": max_risk_rounds,
        "data_vendors": {
            "core_stock_apis": core_stock_vendor,
            "technical_indicators": technical_vendor,
            "fundamental_data": fundamental_vendor,
            "news_data": news_vendor,
        }
    })
    
    return selected_analysts

def display_agent_status():
    """Display the status of all agents in a clean, organized layout"""
    st.subheader("🎯 Agent Status")
    
    # Define agent groups with emojis and colors
    agent_groups = {
        "📊 Analysts": {
            "agents": ["Market Analyst", "Social Analyst", "News Analyst", "Fundamentals Analyst"],
            "color": "#e3f2fd"
        },
        "🔬 Researchers": {
            "agents": ["Bull Researcher", "Bear Researcher", "Research Manager"],
            "color": "#f3e5f5"
        },
        "💼 Trading": {
            "agents": ["Trader"],
            "color": "#e8f5e8"
        },
        "⚠️ Risk Mgmt": {
            "agents": ["Risky Analyst", "Neutral Analyst", "Safe Analyst"],
            "color": "#fff3e0"
        },
        "👔 Portfolio": {
            "agents": ["Portfolio Manager"],
            "color": "#fce4ec"
        }
    }
    
    # Create a more compact layout
    for group_name, group_data in agent_groups.items():
        with st.expander(f"{group_name} ({len(group_data['agents'])} agents)", expanded=False):
            cols = st.columns(min(len(group_data['agents']), 3))  # Max 3 columns
            
            for idx, agent in enumerate(group_data['agents']):
                col_idx = idx % 3
                with cols[col_idx]:
                    status = st.session_state.get(f'{agent.lower().replace(" ", "_")}_status', 'pending')
                    
                    # Status styling
                    status_config = {
                        'pending': {'emoji': '⏳', 'color': '#6c757d', 'bg': '#f8f9fa'},
                        'running': {'emoji': '🔄', 'color': '#856404', 'bg': '#fff3cd'},
                        'completed': {'emoji': '✅', 'color': '#155724', 'bg': '#d4edda'},
                        'error': {'emoji': '❌', 'color': '#721c24', 'bg': '#f8d7da'}
                    }
                    
                    config = status_config.get(status, status_config['pending'])
                    
                    st.markdown(
                        f'<div style="'
                        f'background-color: {config["bg"]}; '
                        f'color: {config["color"]}; '
                        f'padding: 0.5rem; '
                        f'border-radius: 5px; '
                        f'margin: 0.2rem 0; '
                        f'text-align: center; '
                        f'font-size: 0.9rem; '
                        f'border: 1px solid {config["color"]}20;'
                        f'">'
                        f'{config["emoji"]} {agent.replace(" ", "<br>")}<br>'
                        f'<small><i>{status.title()}</i></small>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

def run_analysis(ticker: str, trade_date: str, selected_analysts: list):
    """Run the trading agents analysis"""
    
    try:
        # Validate inputs
        if not ticker or not trade_date:
            st.error("Please provide both ticker symbol and trade date")
            return None
            
        # API keys are loaded from environment (.env file)
        
        # Initialize progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Create TradingAgents instance
        status_text.text("Initializing TradingAgents...")
        progress_bar.progress(10)
        
        ta = TradingAgentsGraph(
            selected_analysts=selected_analysts,
            debug=False,
            config=st.session_state.config
        )
        
        progress_bar.progress(20)
        status_text.text("Running analysis...")
        
        # Run the analysis
        final_state, decision = ta.propagate(ticker, trade_date)
        
        progress_bar.progress(100)
        status_text.text("Analysis completed!")
        
        # Store results
        analysis_result = {
            'ticker': ticker,
            'trade_date': trade_date,
            'final_state': final_state,
            'decision': decision,
            'timestamp': datetime.datetime.now(),
            'selected_analysts': selected_analysts
        }
        
        st.session_state.analysis_history.append(analysis_result)
        st.session_state.current_analysis = analysis_result
        
        return analysis_result
        
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        st.error(f"Details: {traceback.format_exc()}")
        return None

def display_analysis_results(analysis_result: Dict[str, Any]):
    """Display the analysis results in organized tabs"""
    
    if not analysis_result:
        return
        
    final_state = analysis_result['final_state']
    decision = analysis_result['decision']
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Summary", "🔍 Analyst Reports", "🔬 Research Debate", 
        "💼 Trading Decision", "⚠️ Risk Assessment", "📈 Charts", "💾 Export"
    ])
    
    with tab1:
        st.subheader(f"Analysis Summary for {analysis_result['ticker']}")
        st.write(f"**Date:** {analysis_result['trade_date']}")
        st.write(f"**Analysis Time:** {analysis_result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Get and display stock information
        stock_info = get_stock_info(analysis_result['ticker'])
        if stock_info:
            st.write(f"**Company:** {stock_info.get('name', 'N/A')}")
            st.write(f"**Sector:** {stock_info.get('sector', 'N/A')} | **Industry:** {stock_info.get('industry', 'N/A')}")
            
            # Create metrics dashboard
            create_metrics_dashboard(stock_info)
        
        # Display final decision prominently
        if decision:
            st.markdown("### 🎯 Final Trading Decision")
            decision_color = "green" if "buy" in str(decision).lower() else "red" if "sell" in str(decision).lower() else "gray"
            st.markdown(f'<div style="background-color: {decision_color}; color: white; padding: 1rem; border-radius: 5px; text-align: center; font-size: 1.2rem; font-weight: bold;">{decision}</div>', unsafe_allow_html=True)
        
        # Analysis metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Analysts Used", len(analysis_result['selected_analysts']))
        with col2:
            st.metric("Confidence Level", "High")  # Could be derived from analysis
        with col3:
            st.metric("Risk Level", "Medium")  # Could be derived from analysis
    
    with tab2:
        st.subheader("📊 Analyst Team Reports")
        
        # Market Analysis
        if 'market_report' in final_state and final_state['market_report']:
            with st.expander("📈 Market Analysis", expanded=True):
                st.markdown(final_state['market_report'])
        
        # Sentiment Analysis  
        if 'sentiment_report' in final_state and final_state['sentiment_report']:
            with st.expander("💭 Social Sentiment Analysis", expanded=True):
                st.markdown(final_state['sentiment_report'])
        
        # News Analysis
        if 'news_report' in final_state and final_state['news_report']:
            with st.expander("📰 News Analysis", expanded=True):
                st.markdown(final_state['news_report'])
        
        # Fundamentals Analysis
        if 'fundamentals_report' in final_state and final_state['fundamentals_report']:
            with st.expander("📊 Fundamentals Analysis", expanded=True):
                st.markdown(final_state['fundamentals_report'])
    
    with tab3:
        st.subheader("🔬 Research Team Analysis")
        
        if 'investment_plan' in final_state and final_state['investment_plan']:
            st.markdown("### Research Team Recommendation")
            st.markdown(final_state['investment_plan'])
        
        # Display debate history if available
        if 'debate_history' in final_state:
            st.markdown("### Debate History")
            for round_num, debate in enumerate(final_state['debate_history'], 1):
                with st.expander(f"Debate Round {round_num}"):
                    st.markdown(debate)
    
    with tab4:
        st.subheader("💼 Trading Team Decision")
        
        if 'trader_investment_plan' in final_state and final_state['trader_investment_plan']:
            st.markdown("### Trader Analysis")
            st.markdown(final_state['trader_investment_plan'])
        
        if 'final_trade_decision' in final_state and final_state['final_trade_decision']:
            st.markdown("### Final Trade Decision")
            st.markdown(final_state['final_trade_decision'])
    
    with tab5:
        st.subheader("⚠️ Risk Management Assessment")
        
        if 'risk_assessment' in final_state and final_state['risk_assessment']:
            st.markdown("### Risk Analysis")
            st.markdown(final_state['risk_assessment'])
        
        # Risk metrics visualization
        st.markdown("### Risk Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Market Risk", "Medium", delta="0.2")
        with col2:
            st.metric("Volatility Risk", "High", delta="-0.1") 
        with col3:
            st.metric("Liquidity Risk", "Low", delta="0.0")
    
    with tab6:
        st.subheader("📈 Stock Charts and Analysis")
        
        if PLOTLY_AVAILABLE and UTILS_AVAILABLE:
            # Stock price chart
            price_chart = create_stock_chart(analysis_result['ticker'], days=30)
            if price_chart:
                st.plotly_chart(price_chart, use_container_width=True)
            
            # Volume chart
            volume_chart = create_volume_chart(analysis_result['ticker'], days=30)
            if volume_chart:
                st.plotly_chart(volume_chart, use_container_width=True)
            
            # Risk gauge (example)
            col1, col2 = st.columns(2)
            with col1:
                risk_gauge = create_risk_gauge("Medium", 0.6)
                if risk_gauge:
                    st.plotly_chart(risk_gauge, use_container_width=True)
            
            with col2:
                # Sentiment pie chart (example data)
                sentiment_data = {"Positive": 40, "Negative": 30, "Neutral": 30}
                sentiment_chart = create_sentiment_pie_chart(sentiment_data)
                if sentiment_chart:
                    st.plotly_chart(sentiment_chart, use_container_width=True)
        else:
            st.warning("📈 Charts are disabled due to missing dependencies (plotly). Core analysis functionality remains available.")
            st.info("Stock analysis and agent reports are still fully functional in other tabs.")
    
    with tab7:
        st.subheader("💾 Export Analysis")
        
        # Configuration summary
        display_config_summary(st.session_state.config)
        
        st.markdown("---")
        
        # Export options
        st.markdown("### Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 Copy Analysis to Clipboard", use_container_width=True):
                json_data = export_analysis_to_json(analysis_result)
                if json_data:
                    st.code(json_data[:500] + "..." if len(json_data) > 500 else json_data)
                    st.success("Analysis data ready for copying!")
        
        with col2:
            json_data = export_analysis_to_json(analysis_result)
            if json_data:
                st.download_button(
                    label="💾 Download as JSON",
                    data=json_data,
                    file_name=f"{analysis_result['ticker']}_{analysis_result['trade_date']}_analysis.json",
                    mime="application/json",
                    use_container_width=True
                )

def display_analysis_history():
    """Display historical analyses"""
    st.subheader("📚 Analysis History")
    
    if not st.session_state.analysis_history:
        st.info("No previous analyses found. Run your first analysis above!")
        return
    
    # Display as a table
    history_data = []
    for analysis in st.session_state.analysis_history:
        history_data.append({
            'Ticker': analysis['ticker'],
            'Date': analysis['trade_date'],
            'Analysis Time': analysis['timestamp'].strftime('%Y-%m-%d %H:%M'),
            'Decision': str(analysis['decision'])[:50] + '...' if len(str(analysis['decision'])) > 50 else str(analysis['decision']),
            'Analysts': ', '.join(analysis['selected_analysts'])
        })
    
    df = pd.DataFrame(history_data)
    
    # Add selection for detailed view
    selected_analysis = st.selectbox(
        "Select analysis to view details:",
        range(len(st.session_state.analysis_history)),
        format_func=lambda x: f"{st.session_state.analysis_history[x]['ticker']} - {st.session_state.analysis_history[x]['trade_date']}"
    )
    
    if st.button("View Selected Analysis"):
        st.session_state.current_analysis = st.session_state.analysis_history[selected_analysis]
    
    st.dataframe(df, use_container_width=True)

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 TradingAgents</h1>
        <h3>Multi-Agent LLM Financial Trading Framework</h3>
        <p>Powered by specialized AI agents for comprehensive market analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create sidebar
    selected_analysts = create_sidebar()
    
    # Main content area
    st.subheader("🚀 Run Analysis")
    
    # Input form
    with st.form("analysis_form"):
        col_ticker, col_date, col_submit = st.columns([2, 2, 1])
        
        with col_ticker:
            ticker = st.text_input(
                "Stock Ticker",
                value="NVDA",
                help="Enter stock symbol (e.g., AAPL, TSLA, NVDA)"
            ).upper()
        
        with col_date:
            trade_date = st.date_input(
                "Analysis Date",
                value=datetime.date.today() - datetime.timedelta(days=1),
                help="Select date for analysis"
            )
        
        with col_submit:
            st.write("")  # Add some spacing
            st.write("")  # Add some spacing
            submitted = st.form_submit_button(
                "🔍 Run Analysis",
                type="primary",
                use_container_width=True
            )
        
        if submitted:
            st.session_state.analysis_running = True
            result = run_analysis(ticker, str(trade_date), selected_analysts)
            st.session_state.analysis_running = False
            
            if result:
                st.success(f"✅ Analysis completed for {ticker}!")
                st.rerun()
    
    # Agent status in its own section
    st.markdown("---")
    display_agent_status()
    
    # Display current analysis results
    if st.session_state.current_analysis:
        st.markdown("---")
        display_analysis_results(st.session_state.current_analysis)
    
    # Analysis history
    if st.session_state.analysis_history:
        st.markdown("---")
        display_analysis_history()

if __name__ == "__main__":
    main()