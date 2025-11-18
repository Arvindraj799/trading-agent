# TradingAgents - Streamlit Cloud Deployment Guide

## 🌐 Live Demo
Access the live application at: [Your Streamlit Cloud URL will be here]

## 🚀 Quick Start for Users

### Step 1: Get API Keys
You'll need two API keys to use the application:

1. **OpenAI API Key**
   - Visit: https://platform.openai.com/api-keys
   - Create an account and generate an API key
   - Keep this key secure

2. **Alpha Vantage API Key** 
   - Visit: https://www.alphavantage.co/support/#api-key
   - Sign up for a free account
   - Get your API key (free tier includes good rate limits)

### Step 2: Use the Application
1. Open the Streamlit app
2. In the sidebar, enter your API keys
3. Configure your analysis settings
4. Enter a stock ticker (e.g., NVDA, AAPL, TSLA)
5. Select a date and click "Run Analysis"
6. Watch the multi-agent system analyze the stock!

## 🛠️ For Developers: Deploying Your Own Instance

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)

### Deployment Steps

1. **Fork this repository**
   ```bash
   # Clone your fork
   git clone https://github.com/YOUR_USERNAME/trading-agent.git
   cd trading-agent
   ```

2. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your forked repository
   - Main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Set Environment Variables** (Optional)
   If you want to pre-configure API keys:
   - In Streamlit Cloud app settings
   - Go to "Secrets"
   - Add:
     ```toml
     OPENAI_API_KEY = "your_key_here"
     ALPHA_VANTAGE_API_KEY = "your_key_here"
     ```

### Configuration Options

The app supports various configurations through the UI:
- **LLM Models**: OpenAI (GPT-4o, GPT-4o-mini, o1-series), Anthropic, Google
- **Data Sources**: yfinance, Alpha Vantage, OpenAI
- **Analysis Depth**: Configurable debate rounds and analyst selection
- **Export Options**: JSON download and clipboard export

### Cost Optimization Tips

For cost-effective usage:
- Use `gpt-4o-mini` for both deep and quick thinking models
- Set debate rounds to 1
- Use fewer analysts for simpler analysis
- Monitor your OpenAI usage dashboard

## 📊 Features Available in Live Demo

### Multi-Agent Analysis
- **📊 Analyst Team**: Market, Social, News, Fundamentals analysts
- **🔬 Research Team**: Bull/Bear researchers with debates
- **💼 Trading Team**: AI-powered trading decisions
- **⚠️ Risk Management**: Multi-perspective risk assessment
- **👔 Portfolio Management**: Final decision validation

### Interactive Features
- **Real-time Charts**: Stock price and volume visualization
- **Progress Tracking**: Live agent status monitoring
- **Export Options**: Download analysis as JSON
- **History Tracking**: Review previous analyses
- **Mobile Responsive**: Works on all devices

## 🔧 Troubleshooting

### Common Issues
1. **API Key Errors**: Ensure keys are valid and have sufficient credits
2. **Rate Limits**: Wait a few seconds between requests
3. **Invalid Ticker**: Use valid stock symbols (e.g., AAPL not Apple)
4. **Date Issues**: Select trading days (not weekends/holidays)

### Performance
- First analysis may take 2-3 minutes as agents initialize
- Subsequent analyses are typically faster
- Progress is shown in real-time

## 📞 Support

For issues or questions:
- Check the [STREAMLIT_README.md](STREAMLIT_README.md) for detailed documentation
- Open an issue on GitHub
- Review the original TradingAgents documentation

---

**Disclaimer**: This application is for research and educational purposes only. Not financial advice.