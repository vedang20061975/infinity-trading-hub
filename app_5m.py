import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# =====================================
# 🎯 PAGE CONFIGURATION & THEME
# =====================================
st.set_page_config(page_title="Infinity 5-Min AI Hub", layout="wide")

st.markdown("""
    <div style='background-color:#11151c; padding:20px; border-radius:10px; border-left: 8px solid #00ffcc; margin-bottom:20px;'>
        <h1 style='margin:0; color:white;'>🎯 Infinity 5-Minute AI KNN Multi-Crossover Hub</h1>
        <p style='margin:5px 0 0 0; color:#b2b2b2;'>Track Every Single Crossover Time of the Day • Bharat Sir</p>
    </div>
""", unsafe_allow_html=True)

SECURITY_KEY = "SHARP_KNN_10M_2026"
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzLkp1sb8ZUAoHpXvqc6f85Bh70hwuP6RomyNRhFfyeSY2GL7OQvM9NSi6jxw6o3Tpoag/exec?frame=5m"

# =====================================
# 🔑 SECURITY LOGIN INTERFACE
# =====================================
user_input_key = st.text_input("🔑 પ્રીમિયમ સબસ્ક્રિપ્શન Key દાખલ કરો:", type="password")

if user_input_key == SECURITY_KEY:
    st.success("🔓 5M મલ્ટી-સ્કેલ્પિંગ ડેશબોર્ડ એક્ટિવ!")
    
    if st.button("🔄 લાઈવ પીસી ડેટા ફેચ કરો"):
        with st.spinner("પીસી રનરમાંથી આખા દિવસના બ્રેકઆઉટ્સ લોડ થઈ રહ્યા છે..."):
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
                        st.warning("🔔 [WEB ALERT] ૫-મિનિટ ફ્રેમ પર ફ્રેશ બ્રેકઆઉટ સ્ટોક પકડાયો છે!")

                    # 🎯 અલ્ટીમેટ કન્વર્ઝન સેફ્ટી ગાર્ડ
                    time_col = None
                    for c in ["Crossover_History", "Timestamp", "cross_time", "Sync_Time", "time"]:
                        if c in df.columns:
                            time_col = c
                            break
                    
                    if time_col and df[time_col].dropna().astype(str).str.strip().str.len().gt(0).any():
                        df["Cross_Time"] = df[time_col]
                    else:
                        df["Cross_Time"] = "⏱️ " + datetime.now().strftime("%I:%M %p")

                    # 📊 ફાઇનલ ટેબલ લેઆઉટ
                    display_cols = ["Stock", "Current_Price", "Status", "Cross_Time", "AI_KNN_Line", "Average_Line"]
                    available_cols = [c for c in display_cols if c in df.columns]
                    
                    st.dataframe(df[available_cols], use_container_width=True)
                    
                    if 'Clean_Sync' in df.columns:
                        st.caption(f"📊 છેલ્લો લોકલ પીસી સિંક સમય: {df['Clean_Sync'].iloc[-1]}")
                else:
                    st.info("📊 પીસી રનર કનેક્ટેડ છે, પરંતુ અત્યારે કોઈ લાઈવ ક્રોસઓવર ડેટા નથી.")
            except Exception as e:
                st.error(f"❌ ડેટા સિંક એરર: {str(e)}")
                
elif user_input_key != "":
    st.error("❌ ખોટી કી! સાચી પ્રીમિયમ સબસ્ક્રિપ્શન કી એન્ટર કરો.")

st.markdown("---")
st.caption("ℹ️ આ સ્કેનર આજના દિવસમાં જેટલી વાર સ્ટોક બુલિશ ઝોનમાં ક્રોસ થયો હશે તે બધી જ ટાઈમસ્ટિમ્પ હિસ્ટ્રી સેવ રાખે છે.")
