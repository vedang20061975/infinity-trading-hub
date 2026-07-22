import streamlit as st
import requests
import pandas as pd

# =====================================================================
# 🎯 2 SEPARATE WEBHOOK URLS (સિગ્નલ્સ અને ઓથેન્ટિકેશન માટે સાવ અલગ)
# =====================================================================
# 1️⃣ જૂની શીટ લિંક (સિગ્નલ્સ ફેચ કરવા માટે - Infinity_Live_Data)
SIGNAL_BASE_URL = "https://script.google.com/macros/s/AKfycbzEBG3jgZIxSriCNeBz2GqrF8UA22bwrwrQpB1YoWCOiLAg-6-AnHRCLlL2QvWfCmi9yQ/exec"

# 2️⃣ 🎯 નવી શીટ લિંક (ક્લાયન્ટ કી ચકાસવા અને લૉગ્સ નોંધવા માટે - Infinity_Client_Auth_Logs)
# ⚠️ અહીં તમારી નવી શીટની Apps Script Web App URL મૂકો:
AUTH_BASE_URL = "https://script.google.com/macros/s/AKfycbyTBKtigj35OjqfsfwD4dK3saPOHxcdx78fOaJnwgdq6xiaHbgB2G9VPZmplNWOLpU0/exec"

# Page Settings
st.set_page_config(page_title="Infinity Master Combo Hub", page_icon="⚡", layout="wide")

st.title("⚡ Infinity All-In-One Combo Dashboard")

# =====================================================================
# 🔐 SUBSCRIPTION & DYNAMIC KEY VERIFICATION ENGINE
# =====================================================================
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "client_name" not in st.session_state:
    st.session_state["client_name"] = ""

def verify_client_key(secret_key):
    try:
        # નવી ઓથેન્ટિકેશન સ્ક્રિપ્ટ પર રિક્વેસ્ટ મોકલશે
        response = requests.post(
            AUTH_BASE_URL,
            params={"action": "verify_key", "client_key": secret_key},
            timeout=10
        )
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get("status") == "success":
                return True, res_json.get("client_name", "Valued Client")
            else:
                return False, res_json.get("message", "Invalid Key")
    except Exception as e:
        # જો નવી શીટ લિંક સેટ ન હોય તો માસ્ટર બેકઅપ કી (bcp) ચાલશે
        if secret_key == "bcp":
            return True, "Bharat Sir (Master)"
        return False, f"Connection Error: {e}"
    return False, "Invalid Key"

if not st.session_state["authenticated"]:
    secret_input = st.text_input("🔑 Enter Master Combo Key:", type="password")
    if secret_input != "":
        is_valid, name_or_msg = verify_client_key(secret_input)
        if is_valid:
            st.session_state["authenticated"] = True
            st.session_state["client_name"] = name_or_msg
            st.success(f"🔓 ગ્રાહક: {name_or_msg} - ઇન્ફિનિટી ઓલ-ઇન-વન કોમ્બો ડેશબોર્ડ એક્ટિવ!")
            st.rerun()
        else:
            st.error(f"❌ {name_or_msg}")
    st.stop()

# =====================================================================
# 📊 DATA FETCHING ENGINE (FROM SIGNAL_BASE_URL - ૧૦૦% સુરક્ષિત)
# =====================================================================
def get_sheet_data(frame_name):
    try:
        # જૂની શીટ સ્ક્રિપ્ટમાંથી જ ડેટા લાવશે
        response = requests.get(f"{SIGNAL_BASE_URL}?frame={frame_name}", timeout=15)
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
            # રિફ્રેશ એક્ટિવિટી પણ નવી શીટમાં લોગ કરશે
            try:
                requests.post(
                    AUTH_BASE_URL, 
                    params={
                        "action": "log_activity", 
                        "client_name": st.session_state.get("client_name", "User"), 
                        "frame": frame_key
                    }, 
                    timeout=5
                )
            except:
                pass
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

st.info(f"ℹ️ માસ્ટર કોમ્બો ડેશબોર્ડ | Logged in as: {st.session_state.get('client_name', 'Active User')}")
