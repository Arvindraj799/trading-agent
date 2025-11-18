# 🤖 TradingAgents - Multi-Agent Trading Framework with Streamlit UI

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/Arvindraj799/trading-agent)

A comprehensive multi-agent trading framework powered by LLMs, now with a **beautiful Streamlit web interface** for easy access and sharing!

## 🌟 **NEW: Streamlit Web UI**

### 🚀 **Quick Access**
- **Live Demo**: [Deploy on Streamlit Cloud](https://share.streamlit.io) 
- **Local Usage**: `streamlit run streamlit_app.py`
- **GitHub**: https://github.com/Arvindraj799/trading-agent

### ✨ **Web UI Features**
- 🎨 **Professional Interface**: Clean, intuitive design
- 📱 **Mobile Responsive**: Works on all devices  
- 🔄 **Real-time Progress**: Watch agents work in real-time
- 📊 **Interactive Charts**: Candlestick charts and volume analysis
- 📈 **Multi-Agent Visualization**: Collapsible status groups
- 💾 **Export Options**: Download analysis as JSON
- 🎯 **7-Tab Interface**: Organized analysis sections
- 🔐 **Secure**: API keys safely managed

## 🎯 **How It Works**

### Multi-Agent System
```
📊 Analyst Team → 🔬 Research Team → 💼 Trading Team → ⚠️ Risk Management → 👔 Portfolio Manager
```

1. **📊 Analysts** gather data (Market, Social, News, Fundamentals)
2. **🔬 Researchers** debate Bull vs Bear perspectives  
3. **💼 Trader** makes informed decisions
4. **⚠️ Risk Team** assesses risks from multiple angles
5. **👔 Portfolio Manager** gives final approval

## 🚀 **Getting Started**

### Option 1: Use Live Web App (Recommended)
1. Go to the deployed Streamlit app *(link coming soon)*
2. Enter your API keys in the sidebar:
   - OpenAI API Key
   - Alpha Vantage API Key
3. Select stock ticker and date
4. Click "Run Analysis" and watch the magic! ✨

### Option 2: Run Locally
```bash
# Clone repository
git clone https://github.com/Arvindraj799/trading-agent.git
cd trading-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run Streamlit app
streamlit run streamlit_app.py
```

### Option 3: Deploy Your Own
1. Fork the repository
2. Deploy to Streamlit Cloud
3. Configure secrets in Streamlit Cloud dashboard
4. Share with your team!

## 🎨 **UI Screenshots**

### Main Interface
- Clean form for stock analysis
- Real-time agent status monitoring
- Professional styling with custom CSS

### Analysis Results  
- **Summary Tab**: Key metrics and final decision
- **Reports Tab**: Detailed analyst findings
- **Debate Tab**: Research team discussions  
- **Trading Tab**: Investment recommendations
- **Risk Tab**: Multi-perspective risk assessment
- **Charts Tab**: Interactive stock visualizations
- **Export Tab**: Download and configuration

## 🛠️ **Configuration Options**

### LLM Models
- **OpenAI**: GPT-4o, GPT-4o-mini, o1-preview, o1-mini
- **Anthropic**: Claude-3.5-Sonnet
- **Google**: Gemini models

### Data Sources
- **Stock Data**: yfinance, Alpha Vantage
- **News**: Alpha Vantage, OpenAI, Google
- **Fundamentals**: Alpha Vantage, OpenAI

### Analysis Settings
- **Analyst Selection**: Choose specific analysts
- **Debate Rounds**: 1-5 rounds of discussion
- **Risk Assessment**: Configurable depth

## 💰 **Cost Optimization**

For budget-friendly analysis:
- Use `gpt-4o-mini` models (95% cost reduction)
- Set debate rounds to 1
- Select fewer analysts
- Monitor OpenAI usage dashboard

## 📊 **Example Analysis**

```python
# What the system analyzes:
Ticker: NVDA
Date: 2024-11-18

Agents Working:
✅ Market Analyst: Technical indicators analysis
✅ News Analyst: Latest news impact assessment  
✅ Social Analyst: Sentiment from social media
✅ Fundamentals Analyst: Financial health review
✅ Bull Researcher: Positive case arguments
✅ Bear Researcher: Risk case arguments  
✅ Trader: Investment recommendation
✅ Risk Manager: Risk assessment
✅ Portfolio Manager: Final decision

Result: Comprehensive multi-perspective trading analysis
```

## 📁 **Project Structure**

```
trading-agent/
├── streamlit_app.py          # 🎨 Main Streamlit UI
├── streamlit_utils.py        # 🛠️ UI utility functions  
├── run_streamlit.py          # 🚀 Easy app launcher
├── requirements.txt          # 📦 Updated dependencies
├── .streamlit/config.toml    # ⚙️ Streamlit configuration
├── STREAMLIT_README.md       # 📖 Detailed UI docs
├── DEPLOYMENT.md             # 🌐 Deployment guide
└── tradingagents/            # 🤖 Core framework
```

## 🌐 **Deployment Options**

### Streamlit Cloud (Free)
- Connect GitHub repository
- Automatic deployments on push
- Built-in secrets management
- Perfect for sharing demos

### Local Development
- Full control over environment
- Faster iteration and testing
- Private API key management

### Custom Hosting
- Deploy on any cloud provider
- Scale based on usage
- Custom domain options

## 🤝 **Contributing**

We welcome contributions!
- 🐛 Bug fixes and improvements
- ✨ New features and agents
- 📚 Documentation updates
- 🎨 UI/UX enhancements

## 📄 **License & Disclaimer**

- **License**: Same as original TradingAgents framework  
- **Disclaimer**: For research and educational use only
- **Not Financial Advice**: Always consult professionals

## 🔗 **Links**

- **GitHub Repository**: https://github.com/Arvindraj799/trading-agent
- **Original Framework**: [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)
- **Streamlit Documentation**: [docs.streamlit.io](https://docs.streamlit.io)
- **OpenAI API**: [platform.openai.com](https://platform.openai.com)
- **Alpha Vantage API**: [alphavantage.co](https://www.alphavantage.co)

---

**Made with ❤️ for the trading community** | **Powered by AI Agents** 🤖📈