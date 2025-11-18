import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import yfinance as yf

def format_currency(value: float) -> str:
    """Format a number as currency"""
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.2f}M"
    elif value >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"

def format_percentage(value: float) -> str:
    """Format a number as percentage"""
    return f"{value:.2f}%"

def create_stock_chart(ticker: str, days: int = 30) -> go.Figure:
    """Create a stock price chart using plotly"""
    try:
        # Get stock data
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        hist = stock.history(start=start_date, end=end_date)
        
        if hist.empty:
            st.warning(f"No data available for {ticker}")
            return None
        
        # Create candlestick chart
        fig = go.Figure(data=go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            name=ticker
        ))
        
        fig.update_layout(
            title=f"{ticker} Stock Price ({days} days)",
            yaxis_title="Price ($)",
            xaxis_title="Date",
            xaxis_rangeslider_visible=False,
            height=400
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating stock chart: {str(e)}")
        return None

def create_volume_chart(ticker: str, days: int = 30) -> go.Figure:
    """Create a volume chart"""
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        hist = stock.history(start=start_date, end=end_date)
        
        if hist.empty:
            return None
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=hist.index,
            y=hist['Volume'],
            name='Volume',
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title=f"{ticker} Trading Volume ({days} days)",
            yaxis_title="Volume",
            xaxis_title="Date",
            height=300
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating volume chart: {str(e)}")
        return None

def get_stock_info(ticker: str) -> Dict[str, Any]:
    """Get basic stock information"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            'name': info.get('longName', ticker),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('forwardPE', 0),
            'dividend_yield': info.get('dividendYield', 0),
            'beta': info.get('beta', 0),
            'current_price': info.get('currentPrice', 0),
            'previous_close': info.get('previousClose', 0),
            'day_high': info.get('dayHigh', 0),
            'day_low': info.get('dayLow', 0),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 0),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow', 0),
        }
    except Exception as e:
        st.error(f"Error getting stock info: {str(e)}")
        return {}

def create_metrics_dashboard(stock_info: Dict[str, Any]):
    """Create a metrics dashboard for stock information"""
    if not stock_info:
        return
    
    st.subheader("📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_price = stock_info.get('current_price', 0)
        previous_close = stock_info.get('previous_close', 0)
        change = current_price - previous_close
        change_pct = (change / previous_close * 100) if previous_close else 0
        
        st.metric(
            "Current Price",
            f"${current_price:.2f}",
            delta=f"{change:+.2f} ({change_pct:+.2f}%)"
        )
    
    with col2:
        market_cap = stock_info.get('market_cap', 0)
        st.metric(
            "Market Cap",
            format_currency(market_cap)
        )
    
    with col3:
        pe_ratio = stock_info.get('pe_ratio', 0)
        st.metric(
            "P/E Ratio",
            f"{pe_ratio:.2f}" if pe_ratio else "N/A"
        )
    
    with col4:
        dividend_yield = stock_info.get('dividend_yield', 0)
        st.metric(
            "Dividend Yield",
            format_percentage(dividend_yield * 100) if dividend_yield else "N/A"
        )

def create_risk_gauge(risk_level: str, risk_score: float = 0.5) -> go.Figure:
    """Create a risk gauge chart"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Level"},
        delta = {'reference': 0.5},
        gauge = {
            'axis': {'range': [None, 1]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 0.33], 'color': "lightgreen"},
                {'range': [0.33, 0.66], 'color': "yellow"},
                {'range': [0.66, 1], 'color': "lightcoral"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0.8
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def create_sentiment_pie_chart(sentiment_data: Dict[str, float]) -> go.Figure:
    """Create a pie chart for sentiment analysis"""
    labels = list(sentiment_data.keys())
    values = list(sentiment_data.values())
    
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors,
        textinfo='label+percent',
        textposition='auto'
    )])
    
    fig.update_layout(
        title="Sentiment Analysis",
        height=400
    )
    
    return fig

def export_analysis_to_json(analysis_result: Dict[str, Any]) -> str:
    """Export analysis result to JSON string"""
    try:
        # Create a serializable version
        export_data = {
            'ticker': analysis_result['ticker'],
            'trade_date': analysis_result['trade_date'],
            'timestamp': analysis_result['timestamp'].isoformat(),
            'decision': str(analysis_result['decision']),
            'selected_analysts': analysis_result['selected_analysts'],
            'final_state': {}
        }
        
        # Extract key information from final_state
        final_state = analysis_result['final_state']
        for key in ['market_report', 'sentiment_report', 'news_report', 
                   'fundamentals_report', 'investment_plan', 'trader_investment_plan',
                   'final_trade_decision']:
            if key in final_state and final_state[key]:
                export_data['final_state'][key] = str(final_state[key])
        
        return json.dumps(export_data, indent=2)
        
    except Exception as e:
        st.error(f"Error exporting analysis: {str(e)}")
        return ""

def display_config_summary(config: Dict[str, Any]):
    """Display a summary of the current configuration"""
    st.subheader("⚙️ Current Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**LLM Settings:**")
        st.write(f"- Provider: {config.get('llm_provider', 'N/A')}")
        st.write(f"- Deep Think Model: {config.get('deep_think_llm', 'N/A')}")
        st.write(f"- Quick Think Model: {config.get('quick_think_llm', 'N/A')}")
        
        st.write("**Analysis Settings:**")
        st.write(f"- Max Debate Rounds: {config.get('max_debate_rounds', 'N/A')}")
        st.write(f"- Max Risk Rounds: {config.get('max_risk_discuss_rounds', 'N/A')}")
    
    with col2:
        st.write("**Data Vendors:**")
        data_vendors = config.get('data_vendors', {})
        st.write(f"- Stock Data: {data_vendors.get('core_stock_apis', 'N/A')}")
        st.write(f"- Technical Indicators: {data_vendors.get('technical_indicators', 'N/A')}")
        st.write(f"- Fundamental Data: {data_vendors.get('fundamental_data', 'N/A')}")
        st.write(f"- News Data: {data_vendors.get('news_data', 'N/A')}")

def validate_configuration(config: Dict[str, Any]) -> List[str]:
    """Validate the configuration and return any issues"""
    issues = []
    
    # Check required fields
    required_fields = ['llm_provider', 'deep_think_llm', 'quick_think_llm']
    for field in required_fields:
        if not config.get(field):
            issues.append(f"Missing {field}")
    
    # Check data vendors
    data_vendors = config.get('data_vendors', {})
    required_vendors = ['core_stock_apis', 'technical_indicators', 'fundamental_data', 'news_data']
    for vendor in required_vendors:
        if not data_vendors.get(vendor):
            issues.append(f"Missing data vendor for {vendor}")
    
    return issues

def create_progress_tracker():
    """Create a progress tracking component"""
    progress_container = st.empty()
    return progress_container

def update_agent_status_in_session(agent_name: str, status: str):
    """Update agent status in session state"""
    status_key = f"{agent_name.lower().replace(' ', '_')}_status"
    st.session_state[status_key] = status