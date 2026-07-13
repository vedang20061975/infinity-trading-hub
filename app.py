import streamlit as st
import pandas as pd
import requests

# =====================================
# PAGE & THEME CONFIGURATION
# =====================================
st.set_page_config(page_title="Infinity AI Trading Hub", layout="wide")

st.markdown("""
    <div style='background-color:#0e1117; padding:20px; border-radius:10px; border-left: 8px solid #ff4b4b; margin-bottom:20px;'>
        <h1 style='margin:0; color:white;'>🚀 Infinity AI Commercial Trading Hub</h1>
        <p style='margin:5px 0 0 0; color:#b2b2b2;'>Algorithmic Multi-Timeframe Secure Sync Dashboard by Bharat Sir</p>
    </div>
""", unsafe_allow_html=True)

# 🎯 તમારી GOOGLE SHEET ID અહિયાં પેસ્ટ કરો:
SHEET_ID = "17nlPAO2wtzR-vGSI30df_MQXSUJligvSrtWbPxf3CMA"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

PREMIUM_KEYS = {"10M_KNN": "SHARP_KNN_10M_2026"}

st.sidebar.title("🧭 Navigation Menu")
selected_scanner = st.sidebar.radio("તમારું સ્કેનર પસંદ કરો:", ["🎯 10-Minute AI KNN Intraday"])

if selected_scanner == "🎯 10-Minute AI KNN Intraday":
    st.subheader("🎯 Infinity AI KNN Intraday Gold Cloud Window")
    
    user_key = st.text_input("🔑 સબસ્ક્રિપ્શન Key દાખલ કરો:", type="password", key="key_10m")
    if user_key == PREMIUM_KEYS["10M_KNN"]:
        st.success("🔓 પ્રીમિયમ સબસ્ક્રિપ્શન સક્રિય!")
        
        if st.button("🔄 ડેશબોર્ડ ડેટા રિફ્રેશ કરો"):
            with st.spinner("Fetching secure data bridge blocks..."):
                try:
                    # ડાયરેક્ટ ગૂગલ શીટ CSV રીડ લોજિક
                    df = pd.read_csv(CSV_URL)
                    if not df.empty and len(df) > 0:
                        st.success(f"✅ ડેટા સિંક સક્સેસફુલ! છેલ્લો અપડેટ સમય: {df['Timestamp'].iloc[0]}")
                        st.table(df[["Stock", "Current Price", "AI KNN Line", "Average Line", "Status"]])
                        
                        # Fresh Crossover એલર્ટ
                        if "🔥 Fresh Crossover" in df["Status"].values:
                            st.toast("🔔 ALERT: માર્કેટમાં નવો ફ્રેશ ક્રોસઓવર ડિટેક્ટ થયો છે!", icon="🔥")
                            st.audio("https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg", format="audio/ogg", autoplay=True)
                    else:
                        st.info("📊 અત્યારે માર્કેટ કન્ડિશન મુજબ કોઈ સ્ટોક બુલિશ મોમેન્ટમમાં નથી.")
                except Exception as e:
                    st.info("📊 અત્યારે બ્રિજ ડેટાબેઝ ખાલી છે અથવા પીસી રનર બંધ છે.")
    elif user_key != "":
        st.error("❌ ખોટી સબસ્ક્રિપ્શન Key!")
