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
        <p style='margin:5px 0 0 0; color:#b2b2b2;'>Algorithmic Secure Webhook Sync Dashboard by Bharat Sir</p>
    </div>
""", unsafe_allow_html=True)

# 🎯 તમારી GOOGLE WEB APP URL અહિયાં પેસ્ટ કરો:
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzLkp1sb8ZUAoHpXvqc6f85Bh70hwuP6RomyNRhFfyeSY2GL7OQvM9NSi6jxw6o3Tpoag/exec"

PREMIUM_KEYS = {"10M_KNN": "SHARP_KNN_10M_2026"}

st.sidebar.title("🧭 Navigation Menu")
selected_scanner = st.sidebar.radio("તમારું સ્કેનર પસંદ કરો:", ["🎯 10-Minute AI KNN Intraday"])

if selected_scanner == "🎯 10-Minute AI KNN Intraday":
    st.subheader("🎯 Infinity AI KNN Intraday Cloud Window")
    user_key = st.text_input("🔑 સબસ્ક્રિપ્શન Key દાખલ કરો:", type="password", key="key_10m")
    
    if user_key == PREMIUM_KEYS["10M_KNN"]:
        st.success("🔓 પ્રીમિયમ સબસ્ક્રિપ્શન સક્રિય!")
        
        if st.button("🔄 ડેશબોર્ડ ડેટા રિફ્રેશ કરો"):
            with st.spinner("Fetching data bridge blocks..."):
                try:
                    response = requests.get(WEBHOOK_URL, timeout=15)
                    if response.status_code == 200:
                        data = response.json()
                        if data and len(data) > 0:
                            df = pd.DataFrame(data)
                            
                            # 🎯 કૉલમ ઇન્ડેક્સિંગ ફિક્સ (જેથી ઇન્ડેક્સ એરર ક્યારેય ન આવે)
                            df.columns = ["Stock", "Current Price", "AI KNN Line", "Average Line", "Status", "Timestamp"]
                            
                            st.success(f"✅ ડેટા સિંક સક્સેસફુલ! છેલ્લો અપડેટ સમય: {df['Timestamp'].iloc[0]}")
                            st.table(df[["Stock", "Current Price", "AI KNN Line", "Average Line", "Status"]])
                            
                            # Fresh Crossover એલર્ટ ચેક
                            if "🔥 Fresh Crossover" in df["Status"].values:
                                st.toast("🔔 ALERT: માર્કેટમાં નવો ફ્રેશ ક્રોસઓવર ડિટેક્ટ થયો છે!", icon="🔥")
                        else:
                            st.info("📊 અત્યારે માર્કેટ કન્ડિશન મુજબ કોઈ સ્ટોક બુલિશ મોમેન્ટમમાં નથી.")
                    else:
                        st.error("❌ ગૂગલ બ્રિજ સાથે કનેક્ટ થઈ શકાયું નથી.")
                except Exception as e:
                    st.error(f"❌ ડેટા લોડિંગ એરર: {str(e)}")
    elif user_key != "":
        st.error("❌ ખોટી સબસ્ક્રિપ્શન Key!")
