import streamlit as st
import pandas as pd
import requests
import io
import numpy as np
from datetime import datetime, timedelta

# 🎯 OFFICIAL DHANHQ ABSOLUTE IMPORT
import dhanhq

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

# =====================================
# SIDEBAR MULTI-PAGE MENU
# =====================================
st.sidebar.title("🧭 Navigation Menu")
selected_scanner = st.sidebar.radio(
    "તમારું સ્કેનર પસંદ કરો:",
    [
        "🎯 10-Minute AI KNN Intraday",
        "📈 4-Hour Live Touch Scanner",
        "📊 4H Zone + 15M Volumetric Cross"
    ]
)
st.sidebar.write("---")
st.sidebar.info("💡 **Commercial Note:** 10M સેક્શનમાં હવે ઇન્સ્ટન્ટ રિયલ-ટાઇમ ઓડિયો + વિઝ્યુઅલ એલર્ટ એક્ટિવ છે.")

# =====================================
# CREDENTIALS & DATA MASTER SYNC
# =====================================
CLIENT_ID = "1108096138"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzgzOTMyOTU5LCJpYXQiOjE3ODM4NDY1NTksInRva2VuQ29uc3VtZXJUeXBlIjoiU0VMRiIsIndlYmhvb2tVcmwiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTA4MDk2MTM4In0.k1ykGsggEtd5TRWdjyWYWg2H6wNEizirDOEjDcrfdOvi13i2yJdZDUZdCeMPiTdlaG8GrSyeAPXt23w4G-epsg"

# 🎯 2026 FULLY VALIDATED SERVERS ENGINE CRACK (પેરામીટર કન્ફ્યુઝન સો ટકા સાફ)
dhan = None
try:
    # ઓફિશિયલ કીવર્ડ પ્રોટોકોલ
    dhan = dhanhq.dhanhq(client_id=str(CLIENT_ID), access_token=str(ACCESS_TOKEN))
except Exception as e1:
    try:
        # જો મોડ્યુલ ઓબ્જેક્ટ ઇસ્યુ હોય તો બેઝ ક્લાસથી ડાયરેક્ટ ઇનિશિયલાઇઝેશન
        from dhanhq import dhanhq as CoreDhan
        dhan = CoreDhan(client_id=str(CLIENT_ID), access_token=str(ACCESS_TOKEN))
    except Exception as e2:
        st.error(f"⚠️ Dhan API Initialization Error: {str(e2)}")

WATCHLIST = [
    "ABB", "ACC", "ADANIENT", "ADANIGREEN", "ADANIPORTS", "ADANIPOWER", "AMBUJACEM", "APOLLOHOSP", 
    "ASIANPAINT", "DMART", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV", "BAJFINANCE", "BALKRISIND", "BANKBARODA", 
    "BEL", "BHEL", "BPCL", "BHARTIARTL", "BIOCON", "BOSCHLTD", "BRITANNIA", "CANBK", 
    "CGPOWER", "CIPLA", "COALINDIA", "COFORGE", "COLPAL", "CONCOR", "CUMMINSIND", "DLF", 
    "DABUR", "DIVISLAB", "DRREDDY", "EICHERMOT", "GAIL", "GMRINFRA", "GODREJCP", "GRASIM", 
    "HCLTECH", "HDFCBANK", "HDFCLIFE", "HAVELLS", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", 
    "ICICIGI", "ICICIPRULI", "ITC", "IOC", "IRCTC", "IRFC", "INDUSINDBK", "NAUKRI", 
    "INFY", "INDIGO", "JINDALSTEL", "JSWSTEEL", "JIOFIN", "KOTAKBANK", "LT", "LTIM", 
    "LICHSGFIN", "LICI", "M&M", "MARUTI", "MAXHEALTH", "MUTHOOTFIN", "NTPC", "NESTLEIND", 
    "ONGC", "PIDILITIND", "PFC", "POWERGRID", "PNB", "RELIANCE", "SBICARD", "SBILIFE", 
    "SHREECEM", "SHRIRAMFIN", "SIEMENS", "SRF", "STATEBANK", "SUNPHARMA", "TVSMOTOR", "TATACHEM", 
    "TATACOMM", "TATACONSUM", "TATAELXSI", "TATAMOTORS", "TATAPOWER", "TATASTEEL", "TECHM", "TITAN", 
    "TRENT", "ULTRACEMCO", "UNITDSPR", "VBL", "VEDL", "WIPRO", "ZOMATO",
    "AARTIIND", "ABFRL", "ABBOTINDIA", "ABCAPITAL", "ALKEM", "APLLTD", "APOLLOTYRE", "ASHOKLEY", 
    "ASTRAL", "ATUL", "AUROPHARMA", "BALRAMCHIN", "BANDHANBNK", "BATAINDIA", "BERGEPAINT", "BHARATFORG", 
    "CHAMBLFERT", "CHOLAMANDAL", "COROMANDEL", "CROMPTON", "DEEPAKNTR", "DELTACORP", "ESCORTS", "EXIDEIND", 
    "FEDERALBNK", "GLENMARK", "GODREJPROP", "GRANULES", "GUJGASLTD", "HAL", "HINDCOPPER", "IBULHSGFIN", 
    "IDFCFIRSTB", "IEX", "IGL", "INDHOTEL", "INDIACEM", "INDIAMART", "IPCALAB", "JKCEMENT", 
    "JUBLFOOD", "L&TFH", "LALPATHLAB", "LUPIN", "M&MFIN", "MANAPPURAM", "METROPOLIS", "MFSL", 
    "MGL", "MPHASIS", "MRF", "NATIONALUM", "NAVINFLUOR", "NMDC", "OBEROIRLTY", "OFSS", 
    "PAGEIND", "PEL", "PERSISTENT", "PETRONET", "POLYCAB", "PVRINOX", "RAMCOCEM", "RBLBANK", 
    "SAIL", "SANOFI", "SONACOMS", "SUNTV", "SYNGENE", "TEAMLEASE", "TORNTPOWER", "UBL", 
    "UPL", "VOLTAS", "WHIRLPOOL", "ZEEL"
]

@st.cache_data(ttl=3600)
def load_security_ids_master():
    try:
        url = "https://images.dhan.co/api-data/api-scrip-master.csv"
        s = requests.get(url).content
        master_df = pd.read_csv(io.StringIO(s.decode('utf-8')), low_memory=False)
        master_df = master_df[(master_df['SEM_EXM_EXCH_ID'] == 'NSE') & (master_df['SEM_INSTRUMENT_NAME'] == 'EQUITY')]
        
        mapping = {}
        for _, row in master_df.iterrows():
            sym = str(row['SEM_TRADING_SYMBOL']).replace("-EQ", "")
            if sym in WATCHLIST:
                mapping[sym] = str(row['SEM_SMST_SECURITY_ID'])
        return mapping
    except: 
        return {}

stock_map = load_security_ids_master()

# =====================================
# MATHEMATICAL MATH PACKS
# =====================================
def calculate_pure_rma(series, period):
    return series.ewm(alpha=1.0/period, adjust=False).mean()

def calculate_pure_wma(series, period):
    weights = np.arange(1, period + 1)
    return series.rolling(period).apply(lambda candles: np.dot(candles, weights) / weights.sum(), raw=True)

def mean_of_k_closest(df, num_closest=3, window_size=30, ma_len=5):
    hl2 = (df['high'] + df['low']) / 2
    value_in = hl2.rolling(window=ma_len).mean()
    target_in = calculate_pure_rma(df['close'], period=5)
    knn_ma_out = []
    val_list, tar_list = value_in.tolist(), target_in.tolist()
    for idx in range(len(df)):
        if idx < window_size + 5:
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

def calculate_luxalgo_4h_obs(df, swing_period=5):
    df_len = len(df)
    if df_len < swing_period * 2: return []
    highs, lows, closes, times = df["high"].tolist(), df["low"].tolist(), df["close"].tolist(), df["time_str"].tolist()
    all_bullish_obs = []
    for i in range(swing_period, df_len - swing_period):
        if lows[i] == min(lows[i-swing_period:i+swing_period+1]):
            for k in range(i + 1, df_len):
                if closes[k] > highs[i]:
                    slice_lows = lows[i:k+1]
                    actual_ob_idx = i + slice_lows.index(min(slice_lows))
                    mitigated_before_now = False
                    for j in range(k, df_len - 1):
                        if closes[j] < lows[actual_ob_idx]:
                            mitigated_before_now = True
                            break
                    all_bullish_obs.append({
                        "Origin Time": times[actual_ob_idx], "OB Low": lows[actual_ob_idx], "OB High": highs[actual_ob_idx],
                        "IsActiveBeforeNow": not mitigated_before_now
                    })
                    break
    return all_bullish_obs

def calculate_pure_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# =====================================
# CORE IMPLEMENTATION - ROUTING ENGINE
# =====================================

# 🎯 સેક્શન ૧: 10-MINUTE AI KNN
if selected_scanner == "🎯 10-Minute AI KNN Intraday":
    st.subheader("🎯 10-Minute AI KNN Intraday Gold Scanner")
    st.write("છેલ્લા ટ્રેડિંગ સેશનમાં જનરેટ થયેલા શુદ્ધ બુલિશ મોમેન્ટમ સ્ટોક્સ (૨૪ કલાક એનીટાઇમ એક્ટિવ).")
    
    user_key = st.text_input("🔑 સબસ્ક્રિપ્શન Key દાખલ કરો:", type="password", key="key_10m")
    if user_key == PREMIUM_KEYS["10M_KNN"]:
        st.success("🔓 પ્રીમિયમ સબસ્ક્રિપ્શન સક્રિય!")
        if st.button("🚀 10-Minute AI Gold Momentum સ્કેન કરો"):
            if not dhan:
                st.error("❌ ધન એપીઆઈ કનેક્શન સક્રિય નથી.")
                st.stop()
            results = []
            alert_triggered = False
            progress_bar = st.progress(0)
            
            for idx, stock in enumerate(WATCHLIST):
                progress_bar.progress((idx + 1) / len(WATCHLIST))
                if stock not in stock_map: continue
                try:
                    res = dhan.intraday_minute_data(stock_map[stock], "NSE_EQ", "EQUITY", (datetime.now() - timedelta(days=35)).strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"))
                    if res and res.get("status") == "success" and res.get("data"):
                        raw_df = pd.DataFrame(res["data"])
                        raw_df["datetime"] = pd.to_datetime(raw_df["timestamp"], unit="s").dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
                        df_10m = raw_df.set_index("datetime").sort_index().between_time("09:15", "15:30").resample("10min").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
                        
                        if len(df_10m) < 65: continue
                        knnMA = mean_of_k_closest(df_10m, 3, 30, 5)
                        knnMA_ = calculate_pure_wma(knnMA, 5)
                        MAknn_ = calculate_pure_rma(knnMA, 50)
                        
                        if knnMA_.iloc[-1] > MAknn_.iloc[-1]:
                            cross_at = ""
                            last_date_block = df_10m.index[-1].date()
                            for l_idx in range(len(df_10m) - 1, 0, -1):
                                if df_10m.index[l_idx].date() != last_date_block: break
                                if knnMA_.iloc[l_idx] > MAknn_.iloc[l_idx] and knnMA_.iloc[l_idx-1] <= MAknn_.iloc[l_idx-1]:
                                    cross_at = df_10m.index[l_idx].strftime("%H:%M")
                                    break
                            
                            if cross_at == "":
                                cross_at = df_10m.index[-1].strftime("%H:%M")
                            
                            is_fresh_candle_cross = (knnMA_.iloc[-1] > MAknn_.iloc[-1] and knnMA_.iloc[-3] <= MAknn_.iloc[-3])
                            
                            if is_fresh_candle_cross:
                                st.toast(f"🔔 ALERT: {stock} માં ૧૦ મિનિટ પર બિલકુલ હમણાં ફ્રેશ ક્રોસઓવર થયો છે!", icon="🔥")
                                alert_triggered = True
                                
                            results.append({
                                "Stock": stock, 
                                "Current Price": float(df_10m.iloc[-1]["close"]), 
                                "AI KNN Line": float(round(knnMA_.iloc[-1],2)), 
                                "Average KNN Line": float(round(MAknn_.iloc[-1],2)), 
                                "Cross Time": str(cross_at), 
                                "Status": "🔥 Fresh Crossover" if is_fresh_candle_cross else "🎯 Active Bullish"
                            })
                except: continue
                
            if alert_triggered:
                st.audio("https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg", format="audio/ogg", autoplay=True)
                
            if results: 
                st.success("🔥 10-Minute AI KNN સ્કેન પૂરું થયું!")
                st.table(pd.DataFrame(results).drop_duplicates(subset=["Stock"], keep="last"))
            else: 
                st.info("કોઈ બુલિશ ટ્રેન્ડિંગ સ્ટોક મળ્યો નથી.")
    elif user_key != "": st.error("❌ ખોટી સબસ્ક્રિપ્શન Key!")

# 📈 સેક્શન ૨: 4-HOUR LIVE TOUCH SCANNER
elif selected_scanner == "📈 4-Hour Live Touch Scanner":
    st.subheader("🎯 Smart Money Concepts (LuxAlgo) - 4-Hour Live Touch Scanner Pro")
    user_key = st.text_input("🔑 સબસ્ક્રિપ્શન Key દાખલ કરો:", type="password", key="key_4h")
    if user_key == PREMIUM_KEYS["4H_TOUCH"]:
        st.success("🔓 પ્રીમિયમ સબસ્ક્રિપ્શન સક્રિય!")
        if st.button("🚀 4h Chart પર સ્ટોક્સ સ્કેન કરવાનું ચાલુ કરો"):
            if not dhan:
                st.error("❌ ધન એપીઆઈ કનેક્શન સક્રિય નથી.")
                st.stop()
            results = []
            progress_bar = st.progress(0)
            for idx, stock in enumerate(WATCHLIST):
                progress_bar.progress((idx + 1) / len(WATCHLIST))
                if stock not in stock_map: continue
                try:
                    res = dhan.intraday_minute_data(stock_map[stock], "NSE_EQ", "EQUITY", (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"))
                    if res and res.get("status") == "success" and res.get("data"):
                        raw_df = pd.DataFrame(res["data"])
                        raw_df["datetime"] = pd.to_datetime(raw_df["timestamp"], unit="s").dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
                        df_4h = raw_df.set_index("datetime").sort_index().between_time("09:15", "15:30").resample("4h", offset="15min").agg({"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
                        df_4h["time_str"] = df_4h.index.strftime("%Y-%m-%d %H:%M")
                        
                        if df_4h.empty: continue
                        obs = calculate_luxalgo_4h_obs(df_4h, swing_period=5)
                        for ob in obs:
                            touched = False
                            for k in range(-1, -12, -1): 
                                if abs(k) <= len(df_4h):
                                    if (df_4h["low"].iloc[k] <= ob["OB High"]) and (df_4h["high"].iloc[k] >= ob["OB Low"]):
                                        touched = True
                                        break
                            if touched:
                                results.append({
                                    "Stock": stock, "Current Price": float(df_4h.iloc[-1]["close"]), "OB Status": "Fresh Zone Inside",
                                    "OB Low (Demand)": ob["OB Low"], "OB High (Demand)": ob["OB High"], "OB Date/Time": ob["Origin Time"]
                                })
                except: continue
            if results: st.table(pd.DataFrame(results).drop_duplicates(subset=["Stock"], keep="last"))
            else: st.warning("⚠️ કોઈ સ્ટોક 4h ઓર્ડર બ્લોક ઝોનમાં નથી.")
    elif user_key != "": st.error("❌ ખોટી સબસ્ક્રિપ્શન Key!")

# 📊 સેક્શન ૩: 4H ZONE + 15M VOLUMETRIC CROSS
elif selected_scanner == "📊 4H Zone + 15M Volumetric Cross":
    st.subheader("🎯 Infinity SMC 4H Zone + 15M Volumetric Cross")
    user_key = st.text_input("🔑 સબસ્ક્રિપ્શન Key દાખલ કરો:", type="password", key="key_strict")
    if user_key == PREMIUM_KEYS["4H_ZONE_15M"]:
        st.success("🔓 પ્રીમિયમ સબસ્ક્રિપ્શન સક્રિય!")
        if st.button("🚀 Perfect 5-10 Stocks સ્કેન શરૂ કરો"):
            if not dhan:
                st.error("❌ ધન એપીઆઈ કનેક્શન સક્રિય નથી.")
                st.stop()
            perfect_results = []
            progress_bar = st.progress(0)
            for idx, stock in enumerate(WATCHLIST):
                progress_bar.progress((idx + 1) / len(WATCHLIST))
                if stock not in stock_map: continue
                try:
                    res = dhan.intraday_minute_data(stock_map[stock], "NSE_EQ", "EQUITY", (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"))
                    if res and res.get("status") == "success" and res.get("data"):
                        raw_df = pd.DataFrame(res["data"])
                        raw_df["datetime"] = pd.to_datetime(raw_df["timestamp"], unit="s").dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
                        raw_df = raw_df.set_index("datetime").sort_index().between_time("09:15", "15:30")
                        
                        df_4h = raw_df.resample("4h", offset="15min").agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}).dropna()
                        df_4h["time_str"] = df_4h.index.strftime("%Y-%m-%d %H:%M")
                        df_15m = raw_df.resample("15min").agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}).dropna()
                        
                        if len(df_4h) < 15 or len(df_15m) < 60: continue
                        
                        df_15m['sma20'] = df_15m['close'].rolling(20).mean()
                        df_15m['sma50'] = df_15m['close'].rolling(50).mean()
                        df_15m['rsi'] = calculate_pure_rsi(df_15m['close'], 14)
                        
                        is_fresh_crossover = False
                        for c_idx in range(-1, -15, -1):
                            if df_15m['sma20'].iloc[c_idx] > df_15m['sma50'].iloc[c_idx]:
                                is_fresh_crossover = True
                                break
                        
                        if not is_fresh_crossover: continue
                        
                        obs = calculate_luxalgo_4h_obs(df_4h, swing_period=5)
                        for ob in obs:
                            if (df_4h["low"].iloc[-1] <= ob["OB High"]) and (df_4h["high"].iloc[-1] >= ob["OB Low"]):
                                perfect_results.append({
                                    "Stock": stock, "Current Price": float(df_4h.iloc[-1]["close"]), "OB Status": "Sharp Volumetric Reversal",
                                    "4H OB Low": ob["OB Low"], "4H OB High": ob["OB High"], "15M RSI": round(df_15m['rsi'].iloc[-1],2), "Zone Time": ob["Origin Time"]
                                })
                except: continue
            if perfect_results: st.table(pd.DataFrame(perfect_results).drop_duplicates(subset=["Stock"], keep="last"))
            else: st.info("અત્યારે માર્કેટમાં કોઈ સ્ટોક રેડી નથી.")
    elif user_key != "": st.error("❌ ખોટી સબસ્ક્રિપ્શન Key!")
