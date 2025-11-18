# TradingAgents Streamlit UI

A comprehensive web-based user interface for the TradingAgents multi-agent trading framework, built with Streamlit.

## 🌟 Features

### 🤖 Multi-Agent Analysis
- **Analyst Team**: Market, Social, News, and Fundamentals analysts
- **Research Team**: Bull/Bear researchers with debate functionality  
- **Trading Team**: AI-powered trader for decision making
- **Risk Management**: Multi-perspective risk assessment
- **Portfolio Management**: Final decision approval

### 📊 Interactive Interface
- **Real-time Configuration**: Adjust LLM settings, data vendors, and analysis parameters
- **Progress Tracking**: Monitor agent status and analysis progress
- **Rich Visualizations**: Stock charts, sentiment analysis, risk gauges
- **Export Options**: Download analysis results as JSON

### 📈 Stock Analysis Features
- **Stock Price Charts**: Interactive candlestick charts with 30-day history
- **Volume Analysis**: Trading volume visualization
- **Key Metrics**: Real-time stock metrics (price, market cap, P/E ratio, etc.)
- **Risk Assessment**: Visual risk gauges and metrics

### 🔧 Configuration Options
- **LLM Providers**: OpenAI, Anthropic, Google
- **Model Selection**: Choose deep-thinking and quick-thinking models
- **Data Vendors**: Configure data sources for different analysis types
- **Analysis Settings**: Customize debate rounds and discussion depth

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- Required API Keys:
  - OpenAI API Key (for LLM inference)
  - Alpha Vantage API Key (for financial data)

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the Application**
   ```bash
   # Option 1: Using the runner script (recommended)
   python run_streamlit.py
   
   # Option 2: Direct streamlit command
   streamlit run streamlit_app.py
   ```

4. **Open in Browser**
   - The application will automatically open at `http://localhost:8501`
   - If not, navigate to the URL manually

## 📖 Usage Guide

### 1. Configuration Setup
- **API Keys**: Enter your OpenAI and Alpha Vantage API keys in the sidebar
- **LLM Settings**: Choose your preferred models and provider
- **Analysis Settings**: Select which analysts to include and debate rounds
- **Data Vendors**: Configure data sources for different analysis types

### 2. Running Analysis
- **Stock Ticker**: Enter the stock symbol (e.g., NVDA, AAPL, TSLA)
- **Analysis Date**: Select the date for analysis
- **Run Analysis**: Click the "🔍 Run Analysis" button
- **Monitor Progress**: Watch agent status updates in real-time

### 3. Viewing Results
Navigate through the tabs to explore different aspects of the analysis:

#### 📊 Summary Tab
- Company information and key metrics
- Final trading decision with color-coded display
- Analysis metadata and confidence metrics

#### 🔍 Analyst Reports Tab
- Market analysis from technical indicators
- Social sentiment analysis
- News analysis and impact assessment
- Fundamentals analysis with financial data

#### 🔬 Research Debate Tab
- Bull vs Bear researcher debates
- Research manager synthesis
- Multi-round discussion history

#### 💼 Trading Decision Tab
- Trader's investment plan
- Final trade decision rationale
- Risk-adjusted recommendations

#### ⚠️ Risk Assessment Tab
- Multi-perspective risk analysis
- Risk metrics and gauges
- Liquidity, volatility, and market risk scores

#### 📈 Charts Tab
- Interactive stock price charts (30-day candlestick)
- Trading volume analysis
- Risk gauge visualization
- Sentiment pie charts

#### 💾 Export Tab
- Configuration summary
- JSON export functionality
- Download analysis results

### 4. Analysis History
- View previous analyses in a tabular format
- Select and re-examine historical results
- Track analysis performance over time

## 🛠️ Advanced Configuration

### Custom Model Selection
The UI supports various LLM models:
- **OpenAI**: GPT-4o, GPT-4o-mini, o1-preview, o1-mini
- **Anthropic**: Claude-3.5-Sonnet
- **Google**: Gemini models

### Data Vendor Options
Configure different data sources:
- **Stock Data**: yfinance, Alpha Vantage
- **Technical Indicators**: yfinance, Alpha Vantage  
- **Fundamental Data**: Alpha Vantage, OpenAI
- **News Data**: Alpha Vantage, OpenAI, Google

### Customization Options
- **Debate Rounds**: 1-5 rounds of bull/bear debates
- **Risk Discussion Rounds**: 1-5 rounds of risk assessment
- **Analyst Selection**: Choose specific analysts to include

## 🔧 Troubleshooting

### Common Issues

1. **Missing API Keys**
   - Ensure OpenAI and Alpha Vantage API keys are set
   - Check .env file or enter keys in the UI sidebar

2. **Import Errors**
   - Run `pip install -r requirements.txt` 
   - Ensure all dependencies are installed

3. **Connection Issues**
   - Check internet connection for API calls
   - Verify API key validity and rate limits

4. **Analysis Failures**
   - Check logs in the Streamlit interface
   - Verify ticker symbol is valid
   - Ensure analysis date is a trading day

### Performance Tips
- Use `gpt-4o-mini` models for faster, cost-effective analysis
- Reduce debate rounds for quicker results
- Select fewer analysts for simpler analysis

## 📁 File Structure

```
TradingAgents/
├── streamlit_app.py          # Main Streamlit application
├── streamlit_utils.py        # Utility functions for UI
├── run_streamlit.py          # Application runner script
├── STREAMLIT_README.md       # This documentation
├── requirements.txt          # Dependencies (updated)
├── .env.example             # Environment variables template
└── tradingagents/           # Core TradingAgents framework
```

## 🤝 Contributing

To contribute to the UI:
1. Fork the repository
2. Create a feature branch
3. Add new features or improvements
4. Test thoroughly with different stocks and configurations
5. Submit a pull request

## 📄 License

This UI is part of the TradingAgents framework and follows the same license terms.

## ⚠️ Disclaimer

This application is for research and educational purposes only. Trading decisions should not be based solely on AI analysis. Always consult with financial professionals and conduct your own research before making investment decisions.

---

**Happy Trading!** 📈🤖