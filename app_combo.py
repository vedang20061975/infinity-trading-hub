import streamlit as st
import requests
import pandas as pd

# =====================================================================
# 🎯 CONFIGURATION LOCK (તમારી નવી ફાઇનલ ગુગલ સ્ક્રિપ્ટ વેબહૂક લિંક)
# =====================================================================
BASE_URL = "https://script.google.com/macros/s/AKfycbzaZQe9sKBWqW0MH_bx42MECBAlvCBz0MjKz_4pbNgB5Rq_kgjzLww9HAlYzo-jVUgW2w/exec"
MASTER_KEY = "bcp"

# Page Settings
st.set_page_config(page_title="Infinity Master Combo Hub", page_icon="⚡", layout="wide")

st.title("⚡ Infinity All-In-One Combo Dashboard")

# =====================================================================
# 🔐 SUBSCRIPTION & SECURITY GATE
# =====================================================================
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    secret_input = st.text_input("🔑 Enter Master Combo Key:", type="password")
    if secret_input == MASTER_KEY:
        st.session_state["authenticated"] = True
        st.success("🔓 ઇન્ફિનિટી ઓલ-ઇન-વન કોમ્બો ડેશબોર્ડ એક્ટિવ!")
        st.rerun()
    elif secret_input != "":
        st.error("❌ Invalid Key! Please enter the correct master key.")
    st.stop()

# =====================================================================
# 📊 DATA FETCHING ENGINE (FROM SHEET1 VIA GET)
# =====================================================================
def get_sheet_data(frame_name):
    try:
        # ગૂગલ સ્ક્રિપ્ટમાંથી ડેટા ફ્રેમ પેરામીટર સાથે ખેંચશે
        response = requests.get(f"{BASE_URL}?frame={frame_name}", timeout=15)
        if response.status_code == 200:
            json_data = response.json()
            if isinstance(json_data, list) and len(json_data) > 0:
                df = pd.DataFrame(json_data)
                
                # 🎯 સ્ટેટસ કોલમના આધારે જે તે ફ્રેમ (1m, 5m, 10m, 30m) નો જ ડેટા ટેબલમાં ફિલ્ટર થશે
                df_filtered = df[df['Status'].str.contains(frame_name, case=False, na=False)]
                return df_filtered
    except:
        pass
    return pd.DataFrame()

# =====================================================================
# 🎛️ MULTI-TIMEFRAME TABS CONFIGURATION
# =====================================================================
tab1, tab2, tab3, tab4 = st.tabs(["⚡ 1-Minute Scalper", "🎯 5-Minute Scalper", "📊 10-Minute Trend", "📈 30-Minute Swing"])

def display_frame_tab(tab_object, frame_label, frame_key):
    with tab_object:
        st.subheader(f"🔥 {frame_label} Signals")
        if st.button(f"🔄 {frame_key.upper()} ડેટા રિફ્રેશ કરો", key=f"btn_{frame_key}"):
            st.rerun()
            
        df_data = get_sheet_data(frame_key)
        if not df_data.empty:
            # શીટની કોલમ્સના પર્ફેક્ટ નામ સાથે મેચિંગ
            expected_cols = ["Stock", "Current Price", "AI KNN Line", "Average Line", "Status", "Timestamp"]
            available_cols = [c for c in expected_cols if c in df_data.columns]
            st.dataframe(df_data[available_cols], use_container_width=True, hide_index=True)
        else:
            st.info(f"📊 {frame_key.upper()} રનર કનેક્ટેડ છે, બુલિશ સેટઅપની રાહ જોવાઈ રહી છે.")

display_frame_tab(tab1, "1-Minute High-Frequency", "1m")
display_frame_tab(tab2, "5-Minute Scalper Intraday", "5m")
display_frame_tab(tab3, "10-Minute Confirm Intraday Trend", "10m")
display_frame_tab(tab4, "30-Minute Swing Trend", "30m")

st.info("ℹ️ માસ્ટર કોમ્બો ડેશબોર્ડ.")
