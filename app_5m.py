import streamlit as st
import requests
import pandas as pd

# =====================================
# 🎯 PAGE CONFIGURATION & THEME
# =====================================
st.set_page_config(page_title="Infinity 5-Min AI Hub", layout="wide")

# સુંદર ડાર્ક મોડ હેડર પટ્ટી
st.markdown("""
    <div style='background-color:#11151c; padding:20px; border-radius:10px; border-left: 8px solid #00ffcc; margin-bottom:20px;'>
        <h1 style='margin:0; color:white;'>🎯 Infinity 5-Minute AI KNN Scalping Hub</h1>
        <p style='margin:5px 0 0 0; color:#b2b2b2;'>Dedicated Fast Scalping Dashboard by Bharat Sir</p>
    </div>
""", unsafe_allow_html=True)

# 🔑 સબસ્ક્રિપ્શન સિક્યોરિટી લોક
SECURITY_KEY = "ved5"

# ⚠️ તમારી GOOGLE SHEET WEBHOOK LINK
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzLkp1sb8ZUAoHpXvqc6f85Bh70hwuP6RomyNRhFfyeSY2GL7OQvM9NSi6jxw6o3Tpoag/exec"

# =====================================
# 🔑 SECURITY LOGIN INTERFACE
# =====================================
user_input_key = st.text_input("🔑 પ્રીમિયમ સબસ્ક્રિપ્શન Key દાખલ કરો:", type="password")

if user_input_key == SECURITY_KEY:
    st.success("🔓 5M પ્યોર સ્કેલ્પિંગ ડેશબોર્ડ એક્ટિવ!")
    
    # રિફ્રેશ બટન
    if st.button("🔄 લાઈવ પીસી ડેટા ફેચ કરો"):
        with st.spinner("ગૂગલ શીટ બ્રિજમાંથી ૫-મિનિટનો ડેટા લોડ થઈ રહ્યો છે..."):
            try:
                res = requests.get(WEBHOOK_URL, timeout=15)
                if res.status_code == 200 and res.json():
                    df = pd.DataFrame(res.json())
                    
                    # 🎯 ઓડિયો એલર્ટ લોજિક
                    if "Status" in df.columns and df["Status"].str.contains("Fresh").any():
                        st.markdown("""
                            <audio autoplay>
                                <source src="https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg" type="audio/ogg">
                            </audio>
                        """, unsafe_allow_html=True)
                        st.warning("🔔 [WEB ALERT] ૫-મિનિટ ફ્રેમ પર ફ્રેશ બ્રેકઆઉટ સ્ટોક પકડાયો છે!")

                    # 🎯 સુધારો: જો કોલમના નામમાં નાની-મોટી ભૂલ હોય તો તેને ડાયનેમિકલી ચેક કરી લેશે
                    possible_time_cols = ["Cross_Time", "cross_time", "Cross Time", "Time"]
                    actual_time_col = None
                    for col in possible_time_cols:
                        if col in df.columns:
                            actual_time_col = col
                            break
                    
                    # જો ટાઈમ કોલમ મળી જાય, તો તેને લિસ્ટમાં ઉમેરો
                    display_cols = ["Stock", "Current_Price", "Status"]
                    if actual_time_col:
                        display_cols.append(actual_time_col)
                    display_cols.extend(["AI_KNN_Line", "Average_Line"])
                    
                    # લાઈવ ડેટા પ્રિન્ટ
                    st.dataframe(df[display_cols], use_container_width=True)
                    
                    if 'Timestamp' in df.columns:
                        st.caption(f"📊 છેલ્લો લોકલ પીસી સિંક સમય: {df['Timestamp'].iloc[-1]}")
                else:
                    st.info("📊 પીસી રનર કનેક્ટેડ છે, પરંતુ અત્યારે કોઈ બુલિશ કેન્ડલ સેટઅપ નથી.")
            except Exception as e:
                st.error(f"❌ ડેટા સિંક એરર: {str(e)}")
                
elif user_input_key != "":
    st.error("❌ ખોટી કી! સાચી પ્રીમિયમ સબસ્ક્રિપ્શન કી એન્ટર કરો.")

st.markdown("---")
st.caption("ℹ️ આ સ્કેનર પ્યોર ૫-મિનિટના ડેટા પર અસલી ક્રોસઓવર ટાઈમ ટ્રેક કરે છે.")
