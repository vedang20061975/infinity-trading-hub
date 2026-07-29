import streamlit as st
import requests
import pandas as pd

# =====================================================================
# 🎯 2 SEPARATE WEBHOOK URLS
# =====================================================================
SIGNAL_BASE_URL = "https://script.google.com/macros/s/AKfycbxJxtQPy5EkPpgqCfer0R0ZKkm1SB_uYNS0q7KKKxXG7ae5z4v3NRLjawcLrkgPXRlxoQ/exec"
AUTH_BASE_URL = "https://script.google.com/macros/s/AKfycbyTBKtigj35OjqfsfwD4dK3saPOHxcdx78fOaJnwgdq6xiaHbgB2G9VPZmplNWOLpU0/exec"

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
    if secret_key == "bcp":
        return True, "Bharat Sir (Master)"
        
    try:
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
# 📊 DATA FETCHING ENGINE (TIMESTAMP DISPLAY FIX)
# =====================================================================
@st.cache_data(ttl=5)
def get_sheet_data(frame_name):
    try:
        clean_frame = str(frame_name).upper().strip()
        url = f"{SIGNAL_BASE_URL}?frame={clean_frame}"
        
        response = requests.get(url, timeout=12)
        if response.status_code == 200:
            json_data = response.json()
            
            if isinstance(json_data, dict):
                json_data = json_data.get("data", json_data.get("result", []))
                
            if isinstance(json_data, list) and len(json_data) > 0:
                df = pd.DataFrame(json_data)
                
                if "Stock" in df.columns:
                    df = df[df["Stock"].astype(str).str.strip() != ""]
                    
                # 🎯 1899 તારીખવાળો કચરો દૂર કરીને અસલી સમય જ બતાવો
                if "Timestamp" in df.columns:
                    df["Timestamp"] = df["Timestamp"].astype(str)
                    df["Timestamp"] = df["Timestamp"].apply(lambda x: x.split("T")[1][:5] if "T" in x else x)
                    
                return df
    except Exception as e:
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
            st.cache_data.clear()
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
            expected_cols = ["Stock", "Current Price", "AI KNN Line", "Average Line", "Status", "Timestamp"]
            available_cols = [c for c in expected_cols if c in df_data.columns]
            
            # Timestamp કોલમને Plain Text દર્શાવવું
            st.dataframe(
                df_data[available_cols], 
                use_container_width=True, 
                hide_index=True,
                column_config={"Timestamp": st.column_config.TextColumn("Timestamp")}
            )
        else:
            st.info(f"📊 {frame_key.upper()} રનર કનેક્ટેડ છે, બુલિશ સેટઅપની રાહ જોવાઈ રહી છે.")

display_frame_tab(tab1, "1-Minute High-Frequency", "1m")
display_frame_tab(tab2, "5-Minute Scalper Intraday", "5m")
display_frame_tab(tab3, "10-Minute Confirm Intraday Trend", "10m")
display_frame_tab(tab4, "30-Minute Swing Trend", "30m")

st.info(f"ℹ️ માસ્ટર કોમ્બો ડેશબોર્ડ | Logged in as: {st.session_state.get('client_name', 'Active User')}")
