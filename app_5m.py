import streamlit as st
import requests
import pandas as pd

# =====================================
# 🎯 PAGE CONFIGURATION & THEME
# =====================================
st.set_page_config(page_title="Infinity 5-Min AI Hub", layout="wide")

st.markdown("""
    <div style='background-color:#11151c; padding:20px; border-radius:10px; border-left: 8px solid #00ffcc; margin-bottom:20px;'>
        <h1 style='margin:0; color:white;'>🎯 Infinity 5-Minute AI KNN Scalping Hub</h1>
        <p style='margin:5px 0 0 0; color:#b2b2b2;'>Dedicated Fast Scalping Dashboard by Bharat Sir</p>
    </div>
""", unsafe_allow_html=True)

SECURITY_KEY = "SHARP_KNN_10M_2026"
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzLkp1sb8ZUAoHpXvqc6f85Bh70hwuP6RomyNRhFfyeSY2GL7OQvM9NSi6jxw6o3Tpoag/exec"

# 🎯 ટાઈમને પ્યોર AM/PM માં કન્વર્ટ કરવાનું ફંક્શન
def clean_to_ampm(time_str):
    try:
        time_str = str(time_str)
        # જો ગૂગલ શીટનું 1899-12-30T09:23:50.000Z ફોર્મેટ હોય
        if "T" in time_str:
            time_part = time_str.split("T")[1].split(".")[0] # મળશે "09:23:50"
            t = pd.to_datetime(time_part, format="%H:%M:%S")
            return t.strftime("%I:%M %p") # આઉટપુટ: "09:23 AM"
        # જો નોર્મલ ૨૪ કલાકનું ફોર્મેટ હોય (દા.ત. "15:25")
        elif ":" in time_str:
            t = pd.to_datetime(time_str.strip(), format="%H:%M")
            return t.strftime("%I:%M %p")
        return time_str
    except:
        return time_str

# =====================================
# 🔑 SECURITY LOGIN INTERFACE
# =====================================
user_input_key = st.text_input("🔑 પ્રીમિયમ સબસ્ક્રિપ્શન Key દાખલ કરો:", type="password")

if user_input_key == SECURITY_KEY:
    st.success("🔓 5M પ્યોર સ્કેલ્પિંગ ડેશબોર્ડ એક્ટિવ!")
    
    if st.button("🔄 લાઈવ પીસી ડેટા ફેચ કરો"):
        with st.spinner("લાઈવ ડેટા લોડ થઈ રહ્યો છે..."):
            try:
                res = requests.get(WEBHOOK_URL, timeout=15)
                if res.status_code == 200 and res.json():
                    raw_data = res.json()
                    df = pd.DataFrame(raw_data)
                    
                    if "Status" in df.columns and df["Status"].str.contains("Fresh").any():
                        st.markdown("""
                            <audio autoplay>
                                <source src="https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg" type="audio/ogg">
                            </audio>
                        """, unsafe_allow_html=True)
                        st.warning("🔔 [WEB ALERT] ૫-મિનિટ ફ્રેમ પર ફ્રેશ બ્રેકઆઉટ સ્ટોક પકડાયો છે!")

                    # ડાયનેમિકલી ટાઈમ કોલમ શોધવી
                    time_col_found = None
                    for col in df.columns:
                        if col.lower() in ["timestamp", "cross_time", "time", "sync_time"]:
                            time_col_found = col
                            break
                    
                    if time_col_found:
                        # 🎯 અહીં જાદુ થશે: આખી કોલમને પ્યોર AM/PM ટાઈમમાં કન્વર્ટ કરી દેશે
                        df["Cross_Time"] = df[time_col_found].apply(clean_to_ampm)
                    else:
                        df["Cross_Time"] = "09:15 AM"

                    # 📊 ફાઇનલ ટેબલ લેઆઉટ
                    final_cols = ["Stock", "Current_Price", "Status", "Cross_Time", "AI_KNN_Line", "Average_Line"]
                    available_cols = [c for c in final_cols if c in df.columns]
                    
                    st.dataframe(df[available_cols], use_container_width=True)
                    
                    if 'Sync_Time' in df.columns:
                        st.caption(f"📊 છેલ્લો લોકલ પીસી સિંક સમય: {clean_to_ampm(df['Sync_Time'].iloc[-1])}")
                else:
                    st.info("📊 પીસી રનર કનેક્ટેડ છે, પરંતુ અત્યારે કોઈ બુલિશ કેન્ડલ સેટઅપ નથી.")
            except Exception as e:
                st.error(f"❌ ડેટા સિંક એરર: {str(e)}")
                
elif user_input_key != "":
    st.error("❌ ખોટી કી! સાચી પ્રીમિયમ સબસ્ક્રિપ્શન કી એન્ટર કરો.")

st.markdown("---")
st.caption("ℹ️ આ સ્કેનર પ્યોર ૫-મિનિટના ડેટા પર અસલી ક્રોસઓવર ટાઈમ ડાયનેમિકલી ટ્રેક કરે છે.")
