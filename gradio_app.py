import gradio as gr
import pandas as pd
import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import TradingAgents
try:
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    from tradingagents.default_config import DEFAULT_CONFIG
    TRADING_AGENTS_AVAILABLE = True
except ImportError:
    TRADING_AGENTS_AVAILABLE = False

def run_trading_analysis(ticker, date_str, selected_analysts):
    """Run trading analysis and return formatted results"""
    
    if not TRADING_AGENTS_AVAILABLE:
        return "❌ TradingAgents framework not available", "", ""
    
    if not ticker:
        return "❌ Please enter a stock ticker", "", ""
    
    try:
        # Create config
        config = DEFAULT_CONFIG.copy()
        config["deep_think_llm"] = "gpt-4o-mini"
        config["quick_think_llm"] = "gpt-4o-mini"
        config["max_debate_rounds"] = 1
        
        # Initialize TradingAgents
        ta = TradingAgentsGraph(
            selected_analysts=selected_analysts,
            debug=False,
            config=config
        )
        
        # Run analysis
        final_state, decision = ta.propagate(ticker, date_str)
        
        # Format results
        summary = f"""
## 🎯 Final Decision for {ticker}
**Decision:** {decision}
**Date:** {date_str}
**Analysis Time:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        # Extract reports
        reports = []
        if 'market_report' in final_state and final_state['market_report']:
            reports.append(f"## 📊 Market Analysis\n{final_state['market_report']}\n")
        if 'sentiment_report' in final_state and final_state['sentiment_report']:
            reports.append(f"## 💭 Sentiment Analysis\n{final_state['sentiment_report']}\n")
        if 'news_report' in final_state and final_state['news_report']:
            reports.append(f"## 📰 News Analysis\n{final_state['news_report']}\n")
        if 'fundamentals_report' in final_state and final_state['fundamentals_report']:
            reports.append(f"## 📈 Fundamentals Analysis\n{final_state['fundamentals_report']}\n")
        
        detailed_reports = "\n".join(reports)
        
        # Trading decision
        trading_info = ""
        if 'investment_plan' in final_state and final_state['investment_plan']:
            trading_info += f"## 🔬 Research Team Decision\n{final_state['investment_plan']}\n\n"
        if 'trader_investment_plan' in final_state and final_state['trader_investment_plan']:
            trading_info += f"## 💼 Trading Plan\n{final_state['trader_investment_plan']}\n\n"
        if 'final_trade_decision' in final_state and final_state['final_trade_decision']:
            trading_info += f"## 📋 Final Trade Decision\n{final_state['final_trade_decision']}\n"
        
        return summary, detailed_reports, trading_info
        
    except Exception as e:
        error_msg = f"❌ Analysis failed: {str(e)}"
        return error_msg, "", ""

def create_gradio_interface():
    """Create and return Gradio interface"""
    
    with gr.Blocks(
        title="🤖 TradingAgents - Multi-Agent Trading Analysis",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .gr-button-primary {
            background: linear-gradient(90deg, #1f4e79 0%, #2e7d9a 100%);
        }
        """
    ) as app:
        
        # Header
        gr.Markdown("""
        # 🤖 TradingAgents - Multi-Agent Trading Framework
        
        **Comprehensive stock analysis powered by AI agents**
        
        This system uses multiple specialized AI agents to analyze stocks from different perspectives:
        - 📊 **Market Analyst**: Technical indicators and price analysis
        - 💭 **Social Analyst**: Sentiment from social media and forums  
        - 📰 **News Analyst**: Latest news impact assessment
        - 📈 **Fundamentals Analyst**: Financial health and metrics
        - 🔬 **Research Team**: Bull vs Bear debate analysis
        - 💼 **Trader**: Final investment recommendations
        - ⚠️ **Risk Management**: Multi-perspective risk assessment
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                # Input section
                gr.Markdown("## 🚀 Analysis Configuration")
                
                ticker_input = gr.Textbox(
                    label="Stock Ticker",
                    placeholder="Enter stock symbol (e.g., NVDA, AAPL, TSLA)",
                    value="NVDA",
                    info="Stock symbol to analyze"
                )
                
                date_input = gr.Textbox(
                    label="Analysis Date",
                    placeholder="YYYY-MM-DD",
                    value="2024-11-17",
                    info="Date for historical analysis"
                )
                
                analysts_input = gr.CheckboxGroup(
                    choices=["market", "social", "news", "fundamentals"],
                    value=["market", "social", "news", "fundamentals"],
                    label="Select Analysts",
                    info="Choose which AI agents to include in analysis"
                )
                
                analyze_btn = gr.Button(
                    "🔍 Run Multi-Agent Analysis",
                    variant="primary",
                    size="lg"
                )
                
                # Status and info
                gr.Markdown("""
                ### ℹ️ About the Analysis
                - **Duration**: 2-5 minutes depending on complexity
                - **Models**: GPT-4o-mini for cost efficiency
                - **Data Sources**: yfinance, Alpha Vantage
                - **Security**: API keys embedded securely
                """)
            
            with gr.Column(scale=2):
                # Results section
                gr.Markdown("## 📊 Analysis Results")
                
                with gr.Tabs():
                    with gr.TabItem("🎯 Summary & Decision"):
                        summary_output = gr.Markdown(
                            "Click 'Run Analysis' to see the final trading decision and summary",
                            label="Analysis Summary"
                        )
                    
                    with gr.TabItem("📋 Detailed Reports"):
                        reports_output = gr.Markdown(
                            "Detailed analysis from each AI agent will appear here",
                            label="Agent Reports"
                        )
                    
                    with gr.TabItem("💼 Trading & Risk"):
                        trading_output = gr.Markdown(
                            "Trading recommendations and risk assessment will appear here",
                            label="Trading Analysis"
                        )
        
        # Connect the button to the function
        analyze_btn.click(
            fn=run_trading_analysis,
            inputs=[ticker_input, date_input, analysts_input],
            outputs=[summary_output, reports_output, trading_output],
            show_progress=True
        )
        
        # Footer
        gr.Markdown("""
        ---
        **⚠️ Disclaimer**: This is for research and educational purposes only. Not financial advice.
        
        **🔗 Links**: [GitHub Repository](https://github.com/Arvindraj799/trading-agent) | [Original Framework](https://github.com/TauricResearch/TradingAgents)
        """)
    
    return app

if __name__ == "__main__":
    # Check API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ Warning: OPENAI_API_KEY not found in environment")
    if not os.getenv("ALPHA_VANTAGE_API_KEY"):
        print("⚠️ Warning: ALPHA_VANTAGE_API_KEY not found in environment")
    
    # Launch the app
    app = create_gradio_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,  # Creates public URL
        show_error=True
    )