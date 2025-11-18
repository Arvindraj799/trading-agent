#!/usr/bin/env python3
"""
TradingAgents Streamlit Application Runner

This script provides an easy way to start the TradingAgents Streamlit UI
with proper environment setup and error handling.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'plotly', 
        'pandas',
        'yfinance',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_env_setup():
    """Check if environment variables are properly set"""
    load_dotenv()
    
    required_env_vars = ['OPENAI_API_KEY', 'ALPHA_VANTAGE_API_KEY']
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("Please set them in your .env file or as environment variables.")
        print("You can also enter them in the Streamlit UI sidebar.")
        return False
    
    return True

def main():
    """Main function to run the Streamlit app"""
    print("🤖 TradingAgents Streamlit Application")
    print("=" * 50)
    
    # Check current directory
    current_dir = Path.cwd()
    streamlit_app_path = current_dir / "streamlit_app.py"
    
    if not streamlit_app_path.exists():
        print(f"❌ streamlit_app.py not found in {current_dir}")
        print("Please run this script from the TradingAgents project directory.")
        sys.exit(1)
    
    print(f"📁 Running from: {current_dir}")
    
    # Check requirements
    print("🔍 Checking requirements...")
    if not check_requirements():
        sys.exit(1)
    print("✅ Requirements check passed")
    
    # Check environment setup
    print("🔍 Checking environment setup...")
    env_ok = check_env_setup()
    if env_ok:
        print("✅ Environment variables configured")
    else:
        print("⚠️  Some environment variables missing (you can set them in the UI)")
    
    # Start Streamlit
    print("\n🚀 Starting Streamlit application...")
    print("The application will open in your default web browser.")
    print("If it doesn't open automatically, go to: http://localhost:8501")
    print("\n" + "=" * 50)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(streamlit_app_path),
            "--server.address", "localhost",
            "--server.port", "8501"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it using: pip install streamlit")
        sys.exit(1)

if __name__ == "__main__":
    main()