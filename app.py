# Hugging Face Spaces entry point
# This is the main file for Hugging Face Spaces deployment

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the main Streamlit app
if __name__ == "__main__":
    # This will be executed when the app starts on Hugging Face Spaces
    exec(open('streamlit_app.py').read())