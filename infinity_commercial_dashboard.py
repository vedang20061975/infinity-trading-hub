import streamlit as st
from dhanhq import dhanhq
import pandas as pd
import requests
import io
import numpy as np
from datetime import datetime, timedelta

# =====================================
# PAGE & THEME CONFIGURATION
# =====================================
st.set_page_config(page_title="Infinity AI Trading Hub", layout="wide")

st.markdown("""
    <div style='background-color:#0e1117; padding:20px; border-radius:10px; border-left: 8px solid #ff4b4b; margin-bottom:20px;'>
        <h1 style='margin:0; color:white;'>🚀 Infinity AI Commercial Trading Hub</h1>
        <p style='margin:5px 0 0 0; color:#b2b2b2;'>Algorithmic Multi-Timeframe Scanners by Bharat Sir (Real-time Alerts Live)</p>
    </div>
""", unsafe_allow_html=True)

# =====================================
# MASTER SUBSCRIPTION KEYS
# =====================================
PREMIUM_KEYS = {
    "10M_KNN": "SHARP_KNN_10M_2026",     
    "4H_TOUCH": "MACRO_TOUCH_4H_2026",   
    "4H_ZONE_15M": "ZONE_CROSS_15M_2026"  
}

# =====================================
# SIDEBAR MULTI-PAGE MENU
# =====================================
st.sidebar.title("🧭 Navigation Menu")
selected_scanner = st.sidebar.radio(
    "તમારું સ્કેનર પસંદ કરો:",
    [
        "🎯 10-Minute AI KNN Intraday",
        "📈 4-Hour Live Touch Scanner",
        "📊 4H Zone + 15M Volumetric Cross"
    ]
)
st.sidebar.write("---")
st.sidebar.info("💡 **Commercial Note:** 10M સેક્શનમાં હવે ઇન્સ્ટન્ટ રિયલ-ટાઇમ ઓડિયો + વિઝ્યુઅલ એલર્ટ એક્ટિવ છે.")

# =====================================
# CREDENTIALS & DATA MASTER SYNC
# =====================================
CLIENT_ID = "1108096138"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzgzODU5MDEwLCJpYXQiOjE3ODM3NzI2MTAsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTA4MDk2MTM4In0.rk9JEQRmoYKmB5pQ9PWrY9KmYLJYW7jAqDt-EeGFCKIDw0OwMiDa0cJzAbI81YzX92FkrTEIdChtiATxZrJ1CQ"

# 🎯 FIXED POSITION CONNECTION (NO TYPE ERROR PROOF)
dhan = dhanhq(str(CLIENT_ID), str(ACCESS_TOKEN))

WATCHLIST = [
    "ABB", "ACC", "ADANIENT", "ADANIGREEN", "ADANIPORTS", "ADANIPOWER", "AMBUJACEM", "APOLLOHOSP", 
    "ASIANPAINT", "DMART", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV", "BAJFINANCE", "BALKRISIND", "BANKBARODA", 
    "BEL", "BHEL", "BPCL", "BHARTIARTL", "BIOCON", "BOSCHLTD", "BRITANNIA", "CANBK", 
    "CGPOWER", "CIPLA", "COALINDIA", "COFORGE", "COLPAL", "CONCOR", "CUMMINSIND", "DLF", 
    "DABUR", "DIVISLAB", "DRREDDY", "EICHERMOT", "GAIL", "GMRINFRA", "GODREJCP", "GRASIM", 
    "HCLTECH", "HDFCBANK", "HDFCLIFE", "HAVELLS", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", 
    "ICICIGI", "ICICIPRULI", "ITC", "IOC", "IRCTC", "IRFC", "INDUSINDBK", "NAUKRI", 
    "INFY", "INDIGO", "JINDALSTEL", "JSWSTEEL", "JIOFIN", "KOTAKBANK", "LT", "LTIM", 
    "LICHSGFIN", "LICI", "M&M", "MARUTI", "MAXHEALTH", "MUTHOOTFIN", "NTPC", "NESTLEIND", 
    "ONGC", "PIDILITIND", "PFC", "POWERGRID", "PNB", "RELIANCE", "SBICARD", "SBILIFE", 
    "SHREECEM", "SHRIRAMFIN", "SIEMENS", "SRF", "STATEBANK", "SUNPHARMA", "TVSMOTOR", "TATACHEM", 
    "TATACOMM", "TATACONSUM", "TATAELXSI", "TATAMOTORS", "TATAPOWER", "TATASTEEL", "TECHM", "TITAN", 
    "TRENT", "ULTRACEMCO", "UNITDSPR", "VBL", "VEDL", "WIPRO", "ZOMATO",
    "AARTIIND", "ABFRL", "ABBOTINDIA", "ABCAPITAL", "ALKEM", "APLLTD", "APOLLOTYRE", "ASHOKLEY", 
    "ASTRAL", "ATUL", "AUROPHARMA", "BALRAMCHIN", "BANDHANBNK", "BATAINDIA", "BERGEPAINT", "BHARATFORG", 
    "CHAMBLFERT", "CHOLAMANDAL", "COROMANDEL", "CROMPTON", "DEEPAKNTR", "DELTACORP", "ESCORTS", "EXIDEIND", 
    "FEDERALBNK", "GLENMARK", "GODREJPROP", "GRANULES", "GUJGASLTD", "HAL", "HINDCOPPER", "IBULHSGFIN", 
    "IDFCFIRSTB", "IEX", "IGL", "INDHOTEL", "INDIACEM", "INDIAMART", "IPCALAB", "JKCEMENT", 
    "JUBLFOOD", "L&TFH", "LALPATHLAB", "LUPIN", "M&MFIN", "MANAPPURAM", "METROPOLIS", "MFSL", 
    "MGL", "MPHASIS", "MRF", "NATIONALUM", "NAVINFLUOR", "NMDC", "OBEROIRLTY", "OFSS", 
    "PAGEIND", "PEL", "PERSISTENT", "PETRONET", "POLYCAB", "PVRINOX", "RAMCOCEM", "RBLBANK", 
    "SAIL", "SANOFI", "SONACOMS", "SUNTV", "SYNGENE", "TEAMLEASE", "TORNTPOWER", "UBL", 
    "UPL", "VOLTAS", "WHIRLPOOL", "ZEEL"
]

@st.cache_data(ttl=3600)
def load_security_ids_master():
    try:
        url = "https://images.dhan.co/api-data/api-scrip-master.csv"
        s = requests.get(url).content
        master_df = pd.read_csv(io.StringIO(s.decode('utf-8')), low_memory=False)
        master_df = master_df[(master_df['SEM_EXM_EXCH_ID'] == 'NSE') & (master_df['SEM_INSTRUMENT_NAME'] == 'EQUITY')]
        mapping = {str(row['SEM_TRADING_SYMBOL']).
