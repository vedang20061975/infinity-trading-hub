import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# =====================================
# 🎯 PAGE CONFIGURATION & THEME
# =====================================
st.set_page_config(page_title="Infinity 1-Min Scalper", layout="wide")

st.markdown("""
    <div style='background-color:#0d1117; padding:20px; border-radius:10px; border-left: 8px solid #ff3366; margin-bottom:20px;'>
        <h1 style='margin:0; color:white;'>⚡ Infinity 1-Minute Ultra-Fast AI Scalper</h1>
        <p style='margin:5px 0 0 0; color:#b2b2b2;'>High-Frequency 1-Min Pure KNN Flow • Bharat Sir</p>
    </div>
""", unsafe_allow_html=True)

SECURITY_KEY = "SHARP_KNN_10M_2026"
# ⚠️ અહીં તમારી નવી કોપી કરેલી ૧-મિનિટ વાળી ગૂગલ વેબહૂક લિંક પેસ્ટ કરો
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwbnwfNHwBfpNWOAfdlh7Pc9I28WcavuRV8gqg4Z_n6g-sViBVfzgnajggI5YM4mjPllg/exec"

user_input_key = st.text_input("🔑 પ્રીમિયમ સબસ્ક્રિપ્શન Key દાખલ કરો:", type="password")

if user_input_key == SECURITY_KEY:
    st.success("🔓 1M અલ્ટ્રા-સ્કેલ્પિંગ ડેશબોર્ડ એક્ટિવ!")
    
    if st.button("⚡ લાઈવ ૧-મિનિટ ડેટા રિફ્રેશ કરો"):
        with st.spinner("૧-મિનિટ સ્કેનરમાંથી ડેટા લોડ થઈ રહ્યો છે..."):
            try:
                res = requests.get(WEBHOOK_URL, timeout=15)
                if res.status_code == 200 and res.json():
                    df = pd.DataFrame(res.json())
                    
                    if "Status" in df.columns and df["Status"].str.contains("Fresh").any():
                        st.markdown("""
                            <audio autoplay>
                                <source src="https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg" type="audio/ogg">
                            </audio>
                        """, unsafe_allow_html=True)
                        st.warning("🔔 [⚡ QUICK ALERT] ૧-મિનિટ ચાર્ટ પર ફ્રેશ સ્કેલ્પિંગ ક્રોસઓવર!")

                    if "Crossover_History" in df.columns:
                        df["Cross_Time"] = df["Crossover_History"]
                    else:
                        df["Cross_Time"] = "⏱️ Prior"

                    display_cols = ["Stock", "Current_Price", "Status", "Cross_Time", "AI_KNN_Line", "Average_Line"]
                    available_cols = [c for c in display_cols if c in df.columns]
                    
                    st.dataframe(df[available_cols], use_container_width=True)
                    
                    if 'Clean_Sync' in df.columns:
                        st.caption(f"📊 છેલ્લો હાઈ-સ્પીડ સિંક સમય: {df['Clean_Sync'].iloc[-1]}")
                else:
                    st.info("📊 ૧-મિનિટ રનર એક્ટિવ છે, બુલિશ સેટઅપની રાહ જોવાઈ રહી છે.")
            except Exception as e:
                st.error(f"❌ ડેટા સિંક એરર: {str(e)}")
                
elif user_input_key != "":
    st.error("❌ ખોટી કી!")

st.markdown("---")
st.caption("ℹ️ આ સ્કેનર ૧-મિનિટની હાઈ-સ્પીડ ફ્રીક્વન્સી પર રન થાય છે. રેપિડ ટ્રેડિંગ માટે બેસ્ટ છે.")
