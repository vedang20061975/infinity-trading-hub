import streamlit as st
import requests
import pandas as pd

# =====================================
# 🎯 PAGE CONFIGURATION & THEME
# =====================================
st.set_page_config(page_title="Infinity Master Combo Hub", layout="wide")

st.markdown("""
    <div style='background-color:#11151c; padding:20px; border-radius:10px; border-left: 8px solid #ffcc00; margin-bottom:20px;'>
        <h1 style='margin:0; color:white;'>🚀 Infinity Master Combo AI Scalping Hub</h1>
        <p style='margin:5px 0 0 0; color:#b2b2b2;'>Multi-Timeframe Unified Intelligence Dashboard • Bharat Sir</p>
    </div>
""", unsafe_allow_html=True)

SECURITY_KEY = "SHARP_KNN_10M_2026"
BASE_URL = "https://script.google.com/macros/s/AKfycbzuL8iv5fbt2oMapI_qTYDKDEuqTvCnAUznmgv0RakGpuV8B29K7itN8qRF4vpyUxD2mw/exec"

# =====================================
# 🔑 SECURITY LOGIN INTERFACE
# =====================================
user_input_key = st.text_input("🔑 પ્રીમિયમ સબસ્ક્રિપ્શન Key દાખલ કરો:", type="password")

if user_input_key == SECURITY_KEY:
    st.success("🔓 ઇન્ફિનિટી ઓલ-ઇન-વન કોમ્બો ડેશબોર્ડ એક્ટિવ!")
    
    tab1, tab2, tab3, tab4 = st.tabs(["⚡ 1-Minute Scalper", "🎯 5-Minute Scalper", "📊 10-Minute Trend", "📈 30-Minute Swing"])
    
    # --- TAB 1: 1-MINUTE ---
    with tab1:
        st.subheader("⚡ 1-Minute High-Frequency Signals")
        if st.button("🔄 1M ડેટા રિફ્રેશ કરો", key="btn_1m"):
            with st.spinner("1M ડેટા લોડ થઈ રહ્યો છે..."):
                try:
                    res = requests.get(f"{BASE_URL}?frame=1m", timeout=15)
                    if res.status_code == 200 and res.json():
                        df = pd.DataFrame(res.json())
                        st.dataframe(df, use_container_width=True)
                    else: st.info("📊 1M રનર કનેક્ટેડ છે, બુલિશ સેટઅપની રાહ જોવાઈ રહી છે.")
                except Exception as e: st.error(f"❌ એરર: {e}")
                
    # --- TAB 2: 5-MINUTE ---
    with tab2:
        st.subheader("🎯 5-Minute Pure Scalping Setup")
        if st.button("🔄 5M ડેટા રિફ્રેશ કરો", key="btn_5m"):
            with st.spinner("5M ડેટા લોડ થઈ રહ્યો છે..."):
                try:
                    res = requests.get(f"{BASE_URL}?frame=5m", timeout=15)
                    if res.status_code == 200 and res.json():
                        df = pd.DataFrame(res.json())
                        
                        # 🎯 ટાઈમ કોલમ ડાયનેમિક ચેક
                        for c in ["Crossover_History", "Timestamp", "cross_time", "Cross_Time"]:
                            if c in df.columns:
                                df["Cross_Time"] = df[c]
                                break
                        
                        display_cols = ["Stock", "Current_Price", "Status", "Cross_Time", "AI_KNN_Line", "Average_Line"]
                        available_cols = [c for c in display_cols if c in df.columns]
                        st.dataframe(df[available_cols], use_container_width=True)
                        if 'Clean_Sync' in df.columns:
                            st.caption(f"📊 છેલ્લો લોકલ પીસી 5M સિંક: {df['Clean_Sync'].iloc[-1]}")
                    else: st.info("📊 5M રનર કનેક્ટેડ છે, બુલિશ સેટઅપની રાહ જોવાઈ રહી છે.")
                except Exception as e: st.error(f"❌ એરર: {e}")
                
    # --- TAB 3: 10-MINUTE ---
    with tab3:
        st.subheader("📊 10-Minute Confirm Intraday Trend")
        if st.button("🔄 10M ડેટા રિફ્રેશ કરો", key="btn_10m"):
            with st.spinner("10M ડેટા લોડ થઈ રહ્યો છે..."):
                try:
                    res = requests.get(f"{BASE_URL}?frame=10m", timeout=15)
                    if res.status_code == 200 and res.json():
                        df = pd.DataFrame(res.json())
                        st.dataframe(df, use_container_width=True)
                    else: st.info("📊 10M રનર કનેક્ટેડ છે, બુલિશ સેટઅપની રાહ જોવાઈ રહી છે.")
                except Exception as e: st.error(f"❌ એરર: {e}")

    # --- TAB 4: 30-MINUTE ---
    with tab4:
        st.subheader("📈 30-Minute Strong Swing Signals")
        if st.button("🔄 30M ડેટા રિફ્રેશ કરો", key="btn_30m"):
            with st.spinner("30M ડેટા લોડ થઈ રહ્યો છે..."):
                try:
                    res = requests.get(f"{BASE_URL}?frame=30m", timeout=15)
                    if res.status_code == 200 and res.json():
                        df = pd.DataFrame(res.json())
                        st.dataframe(df, use_container_width=True)
                    else: st.info("📊 30M રનર કનેક્ટેડ છે, બુલિશ સેટઅપની રાહ જોવાઈ રહી છે.")
                except Exception as e: st.error(f"❌ એરર: {e}")

elif user_input_key != "":
    st.error("❌ ખોટી કી!")

st.markdown("---")
st.caption("ℹ️ આ માસ્ટર કોમ્બો ડેશબોર્ડ ચારેય ટાઈમફ્રેમને તદ્દન અલગ રાખે છે જેથી કોઈ પણ એક ફ્રેમ બંધ કે રીપેર કરવાથી બીજાને કોઈ અસર ન થાય.")
