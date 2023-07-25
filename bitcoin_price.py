import time
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import requests
import json
from prophet import Prophet
from plotly import graph_objs as go

# Set up the Streamlit layout
st.title('Real-time Bitcoin Price')
price_text = st.empty()
prediction_text = st.empty()
graph_placeholder = st.empty()

# Function to get current bitcoin price

