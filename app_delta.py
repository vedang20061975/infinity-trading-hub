import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# =====================================================================
# 🎯 CONFIGURATION LOCK & WEBHOOK LINK
# =====================================================================
# અહીં તમારી એ જ સાચી ગૂગલ સ્ક્રિપ્ટ લિંક પેસ્ટ કરેલી છે જે પીસી રનરમાં છે
BASE_URL = "https://script.google.com/macros/s/AKfycbxVQND0d04u8usPc4_V7nvasVgmIaLfvzRPEHONGv4Z2afgaz-HIhQY_nvAfekusioQ1g/exec"
MASTER_KEY = "BharatSir@Infinity"

# Page Settings
st.set_page_config(page_title="Infinity Delta Volume Hub", page_icon="📊", layout="wide")

# Custom CSS for Dark Premium Theme
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .stDeployButton { display:none; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    div.block-container { padding-top: 2rem; }
    </style>
""", unsafe_allowed_html=True)

st.title("⚡ Infinity Delta Volume Hub (24/7 Live)")

# =====================================================================
# 🔐 SUBSCRIPTION & SECURITY GATE
# =====================================================================
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    secret_input = st.text_input("🔑 Enter Delta Hub Subscription Key:", type="password")
    if secret_input == MASTER_KEY:
        st.session_state["authenticated"] = True
        st.success("🔓 ડેલ્ટા વોલ્યુમ હબ સક્રિય! (Welcome, Bharat Sir (Master))")
        st.rerun()
    elif secret_input != "":
        st.error("❌ Invalid Key! Please enter the correct master key.")
    st.stop()

# =====================================================================
# 📊 DATA FETCHING ENGINE
# =====================================================================
def get_delta_data(frame_name):
    try:
        response = requests.get(f"{BASE_URL}?frame={frame_name}", timeout=15)
        if response.status_code == 200:
            json_data = response.json()
            if isinstance(json_data, list) and len(json_data) > 0:
                return pd.DataFrame(json_data)
    except:
        pass
    return pd.DataFrame()

# =====================================================================
# 🎛️ MULTI-TIMEFRAME TABS CONFIGURATION
# =====================================================================
tab1, tab2, tab3, tab4 = st.tabs(["⚡ 1M Discount", "🎯 5M Discount", "📊 10M Confirm", "📈 30M Swing"])

# --- TAB 1: 1M TIMEFRAME ---
with tab1:
    st.subheader("💎 1M Discount Range & Positive Delta Signals")
    if st.button("🔄 1M રિફ્રેશ કરો", key="refresh_1m"):
        st.rerun()
        
    df_1m = get_delta_data("1m")
    if not df_1m.empty:
        # Filter columns for professional view
        df_show = df_1m[["Stock", "Current_Price", "SR_Delta_Vol", "Macro_Delta_Vol", "Discount_Zone", "Timestamp", "Status"]]
        st.dataframe(df_show, use_container_width=True, hide_index=True)
    else:
        st.info("📊 આ ટાઇમફ્રેમમાં કોઈ સ્ટોક અત્યારે ડિસ્કાઉન્ટ ઝોનમાં પોઝિટિવ ડેલ્ટા સાથે નથી.")

# --- TAB 2: 5M TIMEFRAME ---
with tab2:
    st.subheader("💎 5M Discount Range & Positive Delta Signals")
    if st.button("🔄 5M રિફ્રેશ કરો", key="refresh_5m"):
        st.rerun()
        
    df_5m = get_delta_data("5m")
    if not df_5m.empty:
        df_show = df_5m[["Stock", "Current_Price", "SR_Delta_Vol", "Macro_Delta_Vol", "Discount_Zone", "Timestamp", "Status"]]
        st.dataframe(df_show, use_container_width=True, hide_index=True)
    else:
        st.info("📊 આ ટાઇમફ્રેમમાં કોઈ સ્ટોક અત્યારે ડિસ્કાઉન્ટ ઝોનમાં પોઝિટિવ ડેલ્ટા સાથે નથી.")

# --- TAB 3: 10M TIMEFRAME ---
with tab3:
    st.subheader("💎 10M Discount Range & Positive Delta Signals")
    if st.button("🔄 10M રિફ્રેશ કરો", key="refresh_10m"):
        st.rerun()
        
    df_10m = get_delta_data("10m")
    if not df_10m.empty:
        df_show = df_10m[["Stock", "Current_Price", "SR_Delta_Vol", "Macro_Delta_Vol", "Discount_Zone", "Timestamp", "Status"]]
        st.dataframe(df_show, use_container_width=True, hide_index=True)
    else:
        st.info("📊 આ ટાઇમફ્રેમમાં કોઈ સ્ટોક અત્યારે ડિસ્કાઉન્ટ ઝોનમાં પોઝિટિવ ડેલ્ટા સાથે નથી.")

# --- TAB 4: 30M TIMEFRAME ---
with tab4:
    st.subheader("💎 30M Discount Range & Positive Delta Signals")
    if st.button("🔄 30M રિફ્રેશ કરો", key="refresh_30m"):
        st.rerun()
        
    df_30m = get_delta_data("30m")
    if not df_30m.empty:
        df_show = df_30m[["Stock", "Current_Price", "SR_Delta_Vol", "Macro_Delta_Vol", "Discount_Zone", "Timestamp", "Status"]]
        st.dataframe(df_show, use_container_width=True, hide_index=True)
    else:
        st.info("📊 આ ટાઇમફ્રેમમાં કોઈ સ્ટોક અત્યારે ડિસ્કાઉન્ટ ઝોનમાં પોઝિટિવ ડેલ્ટા સાથે નથી.")
