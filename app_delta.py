import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Infinity Premium & Discount Delta Hub", layout="wide")

st.markdown("""
    <div style='background-color:#0d1f2d; padding:20px; border-radius:10px; border-left: 8px solid #79c1f1; margin-bottom:20px;'>
        <h1 style='margin:0; color:#79c1f1;'>💎 Infinity Premium & Discount Delta Volume Hub</h1>
        <p style='margin:5px 0 0 0; color:#b2b2b2;'>Advanced Volume Delta Support Scalper • Bharat Sir</p>
    </div>
""", unsafe_allow_html=True)

# ⚠️ અહીં તમારી નવી સ્ક્રિપ્ટની URL લોક કરો
BASE_URL = "https://script.google.com/macros/s/AKfycbyVQND0d04u8usPc4_V7nvasVgmIaLfvzRpEHONGv4Z2afgaz-HIhQY_nvAfekusioQ1g/exec"

USER_KEYS = {
    "DELTA_MASTER_2026": "Bharat Sir (Master)",
    "DELTA_VIP_01": "Hiten Bhai",
    "DELTA_VIP_02": "Rajesh Patel"
}

user_input_key = st.text_input("🔑 Enter Delta Hub Subscription Key:", type="password")

if user_input_key in USER_KEYS:
    client_name = USER_KEYS[user_input_key]
    st.success(f"🔓 ડેલ્ટા વોલ્યુમ હબ સક્રિય! (Welcome, {client_name})")
    
    if "delta_logged" not in st.session_state:
        try:
            requests.get(f"{BASE_URL}?frame=login&client={client_name}", timeout=5)
            st.session_state["delta_logged"] = True
        except: pass
        
    t1, t2, t3, t4 = st.tabs(["⚡ 1M Discount", "🎯 5M Discount", "📊 10M Confirm", "📈 30M Swing"])
    
    frames = {"1m": t1, "5m": t2, "10m": t3, "30m": t4}
    
    for f_name, tab_obj in frames.items():
        with tab_obj:
            st.subheader(f"💎 {f_name.upper()} Discount Range & Positive Delta Signals")
            if st.button(f"🔄 {f_name.upper()} રિફ્રેશ કરો", key=f"btn_{f_name}"):
                with st.spinner("ડેટા લોડ થઈ રહ્યો છે..."):
                    try:
                        res = requests.get(f"{BASE_URL}?frame={f_name}", timeout=15)
                        if res.status_code == 200 and res.json():
                            df = pd.DataFrame(res.json())
                            display_cols = ["Stock", "Current_Price", "Status", "SR_Delta_Vol", "Macro_Delta_Vol", "Discount_Zone", "Timestamp"]
                            available_cols = [c for c in display_cols if c in df.columns]
                            st.dataframe(df[available_cols], use_container_width=True)
                        else:
                            st.info("📊 આ ટાઇમફ્રેમમાં કોઈ સ્ટોક અત્યારે ડિસ્કાઉન્ટ ઝોનમાં પોઝિટિવ ડેલ્ટા સાથે નથી.")
                    except Exception as e:
                        st.error(f"❌ સિંક એરર: {e}")
                        
elif user_input_key != "":
    st.error("❌ ખોટી સિક્યોરિટી કી!")
