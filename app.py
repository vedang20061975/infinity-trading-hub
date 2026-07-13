import streamlit as st
import pandas as pd
import requests
import io
import numpy as np
from datetime import datetime, timedelta

# =====================================
# PAGE & THEME CONFIGURATION
# =====================================
st.set_page_config(page_title="Infinity AI Trading Hub", layout="wide")

st.markdown("""
    <div style='background-color:#0e1117; padding:20px; border-radius:10px; border-left: 8px solid #ff4b4b; margin-bottom:20px;'>
        <h1 style='margin:0; color:white;'>🚀 Infinity AI Commercial Trading Hub</h1>
        <p style='margin:5px 0 0 0; color:#b2b2b2;'>Algorithmic Multi-Timeframe Scanners by Bharat Sir (Real-time Alerts Live)</p>
    </div>
""", unsafe_allow_html=True)

# =====================================
# MASTER SUBSCRIPTION KEYS
# =====================================
PREMIUM_KEYS = {
    "10M_KNN": "SHARP_KNN_10M_2026",     
    "4H_TOUCH": "MACRO_TOUCH_4H_2026",   
    "4H_ZONE_15M": "ZONE_CROSS_15M_2026"  
}

st.sidebar.title("🧭 Navigation Menu")
selected_scanner = st.sidebar.radio(
    "તમારું સ્કેનર પસંદ કરો:",
    ["🎯 10-Minute AI KNN Intraday", "📈 4-Hour Live Touch Scanner", "📊 4H Zone + 15M Volumetric Cross"]
)

ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzg0MDMzNzExLCJpYXQiOjE3ODM5NDczMTEsInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTA4MDk2MTM4In0.w1DEUgR62f4LXj2Uiha83DzuW57pLB7nV2tLw4CsGLD0xgySYE6w--Xu82U_92KEaXK6zR2dCP4asnN6cfRSsw"

# સ્કેનિંગ ફાસ્ટ કરવા માટે લિમિટેડ પ્રીમિયમ વૉચલિસ્ટ
WATCHLIST = ["RELIANCE", "TATAMOTORS", "HDFCBANK", "INFY", "STATEBANK", "ICICIBANK", "ITC", "BHARTIARTL", "TATASTEEL", "AXISBANK", "TRENT", "ZOMATO", "M&M", "LT"]

@st.cache_data(ttl=1800)
def load_security_ids_master():
    try:
        url = "https://images.dhan.co/api-data/api-scrip-master.csv"
        s = requests.get(url).content
        master_df = pd.read_csv(io.StringIO(s.decode('utf-8')), low_memory=False)
        master_df = master_df[(master_df['SEM_EXM_EXCH_ID'] == 'NSE') & (master_df['SEM_INSTRUMENT_NAME'] == 'EQUITY')]
        return {str(row['SEM_TRADING_SYMBOL']).replace("-EQ", ""): str(row['SEM_SMST_SECURITY_ID']) for _, row in master_df.iterrows() if str(row['SEM_TRADING_SYMBOL']).replace("-EQ", "") in WATCHLIST}
    except: return {}

stock_map = load_security_ids_master()

def get_dhan_paid_candles(security_id):
    try:
        # સર્વર માટે છેલ્લા ૭ દિવસનો ડેટા પૂરતો છે (સેફ વિન્ડો)
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
        
        headers = {"access-token": ACCESS_TOKEN, "Content-Type": "application/json"}
        payload = {
            "securityId": str(security_id), "exchangeSegment": "NSE_EQ", "instrument": "EQUITY",
            "interval": "1", "fromDate": str(start_date), "toDate": str(end_date)
        }
        res = requests.post("https://api.dhan.co/v2/charts/intraday", headers=headers, json=payload, timeout=10)
        if res.status_code == 200 and res.json().get("status") == "success":
            return res.json().get("data")
    except: pass
    return None

def calculate_pure_rma(series, period):
    return series.ewm(alpha=1.0/period, adjust=False).mean()

def calculate_pure_wma(series, period):
    weights = np.arange(1, period + 1)
    return series.rolling(period).apply(lambda candles: np.dot(candles, weights) / weights.sum(), raw=True)

def mean_of_k_closest(df, num_closest=3, window_size=15, ma_len=3):
    hl2 = (df['high'] + df['low']) / 2
    value_in = hl2.rolling(window=ma_len).mean()
    target_in = calculate_pure_rma(df['close'], period=3)
    knn_ma_out = []
    val_list, tar_list = value_in.tolist(), target_in.tolist()
    for idx in range(len(df)):
        if idx < window_size + ma_len:
            knn_ma_out.append(df['close'].iloc[idx])
            continue
        current_target = tar_list[idx]
        distances, values_slice = [], []
        for lookback in range(1, window_size + 1):
            val = val_list[idx - lookback]
            if not np.isnan(val) and not np.isnan(current_target):
                distances.append(abs(current_target - val))
                values_slice.append(val)
        if len(distances) < num_closest:
            knn_ma_out.append(df['close'].iloc[idx])
            continue
        sorted_indices = np.argsort(distances)[:num_closest]
        knn_ma_out.append(sum(values_slice[i] for i in sorted_indices) / num_closest)
    return pd.Series(knn_ma_out, index=df.index)

# =====================================
# RUNNING SCANNER ENGINE
# =====================================
if selected_scanner == "🎯 10-Minute AI KNN Intraday":
    st.subheader("🎯 10-Minute AI KNN Intraday Cloud Scanner")
    user_key = st.text_input("🔑 સબસ્ક્રિપ્શન Key દાખલ કરો:", type="password", key="key_10m")
    if user_key == PREMIUM_KEYS["10M_KNN"]:
        st.success("🔓 પ્રીમિયમ સબસ્ક્રિપ્શન સક્રિય!")
        if st.button("🚀 Live Market સ્કેન શરૂ કરો"):
            results = []
            progress_bar = st.progress(0)
            
            for idx, stock in enumerate(WATCHLIST):
                progress_bar.progress((idx + 1) / len(WATCHLIST))
                if stock not in stock_map: continue
                
                chart_data = get_dhan_paid_candles(stock_map[stock])
                if chart_data and len(chart_data) > 0:
                    try:
                        raw_df = pd.DataFrame(chart_data)
                        raw_df["datetime"] = pd.to_datetime(raw_df["timestamp"], unit="s").dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
                        df_10m = raw_df.set_index("datetime").sort_index().between_time("09:15", "15:30").resample("10min").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
                        
                        # ક્લાઉડ સર્વર ફિક્સ: લિમિટ ૪૦ માંથી ઘટાડીને ૧૫ કરી દીધી છે
                        if len(df_10m) < 15: continue
                        
                        knnMA = mean_of_k_closest(df_10m, 3, 10, 3)
                        knnMA_ = calculate_pure_wma(knnMA, 3)
                        MAknn_ = calculate_pure_rma(knnMA, 15)
                        
                        if knnMA_.iloc[-1] > MAknn_.iloc[-1]:
                            is_fresh = "🔥 Fresh Crossover" if (knnMA_.iloc[-1] > MAknn_.iloc[-1] and knnMA_.iloc[-2] <= MAknn_.iloc[-2]) else "🎯 Active Bullish"
                            results.append({
                                "Stock": stock, 
                                "Current Price": float(df_10m.iloc[-1]["close"]), 
                                "AI KNN Line": float(round(knnMA_.iloc[-1],2)), 
                                "Average Line": float(round(MAknn_.iloc[-1],2)), 
                                "Status": is_fresh
                            })
                    except: continue
                    
            if results: 
                st.success("🔥 સ્કેન પૂરું થયું!")
                st.table(pd.DataFrame(results))
            else: 
                st.info("📊 અત્યારે લાઇવ માર્કેટની શરત મુજબ કોઈ સ્ટોક બુલિશ ઝોનમાં નથી.")
