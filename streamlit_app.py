import streamlit as st
import requests
import time

# ==========================================
# CONFIGURATION
# ==========================================
# This acts as your "Cloud Channel" name. No signup or database required.
DEVICE_NAME = "iot_dashboard_esp32_unique_9923" 

# ==========================================
# STREAMLIT UI SETUP
# ==========================================
st.set_page_config(page_title="Cloud IoT Dashboard", page_icon="🌐", layout="centered")

st.markdown("""
<style>
    .stApp { background: #0e1117; }
    div[data-testid="stMetricValue"] { color: #00d4ff; font-weight: 700; font-size: 3rem; }
    .stHeader { color: #f0f2f6; }
    .stButton>button {
        width: 100%;
        background-color: #ef4444;
        color: white;
        border-radius: 12px;
        height: 3em;
        font-weight: bold;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌐 Cloud IoT Dashboard")
st.write(f"Connected to Device: **{DEVICE_NAME}**")
st.info("Operating in Cloud Mode (No local database required).")

# ==========================================
# FETCH DATA FROM CLOUD (Dweet.io)
# ==========================================
try:
    url = f"https://dweet.io/get/latest/dweet/for/{DEVICE_NAME}"
    response = requests.get(url, timeout=5)
    
    if response.status_code == 200:
        res_json = response.json()
        if res_json.get("this") == "succeeded" and len(res_json.get("with", [])) > 0:
            data = res_json["with"][0]["content"]
            
            # Display Metrics
            st.subheader("Current Counts")
            st.metric("People Entered", data.get("entered", 0))
            st.metric("People Left", data.get("left", 0))
            st.metric("Present Number", data.get("present", 0))
        else:
            st.warning("📡 Waiting for device data...")
            st.caption("Check if your Simulator or ESP32 is running.")
    else:
        st.error("Could not reach cloud.")
except Exception as e:
    st.error(f"Cloud Error: {e}")

st.divider()

# ==========================================
# SEND COMMAND TO CLOUD
# ==========================================
st.subheader("Remote Action")
if st.button("Reset Dashboard and ESP32"):
    command_payload = {
        "entered": 0, 
        "left": 0, 
        "present": 0,
        "command": "reset",
        "timestamp": time.time()
    }
    requests.post(f"https://dweet.io/dweet/for/{DEVICE_NAME}", json=command_payload)
    st.success("✅ Reset command sent to Cloud!")

# Auto-refresh UI
time.sleep(3)
st.rerun()
