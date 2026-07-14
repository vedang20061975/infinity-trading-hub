import streamlit as st
import pandas as pd
import requests

# =====================================
# PAGE & THEME CONFIGURATION
# =====================================
st.set_page_config(page_title="Infinity 4H Trading Hub", layout="wide")

st.markdown("""
    <div style='background-color:#0e1117; padding:20px; border-radius:10px; border-left: 8px solid #00ffcc; margin-bottom:20px;'>
        <h1 style='margin:0; color:white;'>🚀 Infinity 4-Hour Master Trading Hub</h1>
        <p style='margin:5px 0 0 0; color:#b2b2b2;'>Algorithmic 4H Dual Alert Dashboard by Bharat Sir</p>
    </div>
""", unsafe_allow_html=True)

# 🎯 તમારી 4H GOOGLE WEB APP URL
WEBHOOK_URL_4H = "https://script.google.com/macros/s/AKfycbzC6NweI03C3epyrFmc3K_l9uXzebv7OYW9vhx85z9u7w-1dmw6awVQjRp7j9pfg-X29A/exec"

PREMIUM_KEYS = {"4H_ACCESS": "SHARP_KNN_10M_2026"}

st.sidebar.title("🧭 4H Navigation Menu")
selected_scanner = st.sidebar.radio(
    "તમારું સ્કેનર પસંદ કરો:", 
    ["🍏 4-Hour Live Touch Scanner", "🔥 4H Zone + 15M Volumetric Cross"]
)

st.subheader(f"📊 Cloud Window: {selected_scanner}")
user_key = st.text_input("🔑 સબસ્ક્રિપ્શન Key દાખલ કરો:", type="password", key="4h_key")

if user_key == PREMIUM_KEYS["4H_ACCESS"]:
    st.success("🔓 પ્રીમિયમ 4H સબસ્ક્રિપ્શન સક્રિય!")
    
    if st.button("🔄 ડેશબોર્ડ ડેટા રિફ્રેશ કરો"):
        with st.spinner("Fetching 4H data bridge blocks..."):
            try:
                if selected_scanner == "🍏 4-Hour Live Touch Scanner":
                    response = requests.get(f"{WEBHOOK_URL_4H}?scanner=4H_Touch", timeout=15)
                    if response.status_code == 200:
                        data = response.json()
                        if data:
                            df = pd.DataFrame(data)
                            df.columns = ["Stock", "Current Price", "Alert Level", "Status", "Timestamp"]
                            st.success(f"✅ Master Watchlist loaded! Sync Time: {df['Timestamp'].iloc[0]}")
                            st.dataframe(df[["Stock", "Current Price", "Alert Level", "Status"]], height=600)
                        else: st.info("📊 ક્લાઉડ સ્ટોરેજમાં કોઈ ડેટા મળ્યો નથી.")
                
                elif selected_scanner == "🔥 4H Zone + 15M Volumetric Cross":
                    response = requests.get(f"{WEBHOOK_URL_4H}?scanner=4H_Volumetric", timeout=15)
                    if response.status_code == 200:
                        data = response.json()
                        if data:
                            df = pd.DataFrame(data)
                            df.columns = ["Stock", "Current Price", "Alert Level", "Status", "Timestamp"]
                            st.success(f"✅ Master Watchlist loaded! Sync Time: {df['Timestamp'].iloc[0]}")
                            st.dataframe(df[["Stock", "Current Price", "Alert Level", "Status"]], height=600)
                        else: st.info("📊 ક્લાઉડ સ્ટોરેજમાં કોઈ ડેટા મળ્યો નથી.")
                        
            except Exception as e:
                st.error(f"❌ ડેટા સિંક એરર: {str(e)}")
elif user_key != "":
    st.error("❌ ખોટી સબસ્ક્રિપ્શન Key!")
