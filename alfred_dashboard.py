# file: alfred_dashboard.py
import streamlit as st
from datetime import datetime

st.set_page_config(layout="wide", page_title="Alfred Dashboard", page_icon="⚡")

# --- HEADER ---
st.markdown("## Alfred Dashboard – v1.0 (Prototype)")
st.markdown(f"**Date & Time:** {datetime.now().strftime('%A %d %B %Y, %H:%M:%S')}")
st.markdown("**Location:** Approximate location via GPS module (planned)")
st.markdown("---")

# --- POWER SYSTEM SECTION ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Renogy 12V System")
    st.metric(label="Battery Voltage", value="12.8V", help="Live data via Renogy One Core")
    st.metric(label="Battery SOC", value="92%", help="State of charge from Renogy batteries")
    st.metric(label="Solar Input", value="240W", help="MPPT controller solar wattage input")
    st.metric(label="DC Load", value="45W", help="Total 12V system draw")

with col2:
    st.subheader("EcoFlow Delta Pro")
    st.metric(label="Battery SOC", value="76%", help="EcoFlow battery state of charge")
    st.metric(label="AC Output", value="340W", help="AC devices draw")
    st.metric(label="Input Power", value="120W", help="Via solar or EV charging")

st.markdown("---")

# --- CONNECTIVITY SECTION ---
st.subheader("Connectivity")
col3, col4 = st.columns(2)

with col3:
    st.metric(label="Starlink Status", value="Online", help="Ping to satellite and WAN")
    st.metric(label="Download Speed", value="98 Mbps", help="Polled via Starlink local API")
    st.metric(label="Upload Speed", value="14 Mbps", help="Polled via Starlink local API")

with col4:
    st.metric(label="Devices on WiFi", value="7", help="Connected devices to local router")

st.markdown("---")

# --- ENVIRONMENT SECTION ---
st.subheader("Environmental Monitoring")
col5, col6, col7 = st.columns(3)

with col5:
    st.metric("Interior Temp", "21.6°C", help="From BME280 sensor in van cabin")

with col6:
    st.metric("Humidity", "48%", help="From DHT22 or BME280 sensor")

with col7:
    st.metric("Water Tank Level", "62%", help="From analogue tank sensor")

st.markdown("---")

# --- CONTROL PANEL ---
st.subheader("Lighting & Device Control")

lighting_cols = st.columns(3)
with lighting_cols[0]:
    st.button("Kitchen Lights", help="Toggle 12V strip lights via relay")
with lighting_cols[1]:
    st.button("Ceiling Lights", help="Toggle puck lights, possibly dimmable")
with lighting_cols[2]:
    st.button("Bedside Scene", help="Toggle between reading, chill, off")

device_cols = st.columns(4)
with device_cols[0]:
    st.button("Fridge Power", help="Enable/disable 12V fridge")
with device_cols[1]:
    st.button("Roof Fan", help="Toggle Maxxair or Fiamma fan")
with device_cols[2]:
    st.button("Inverter", help="Switch AC inverter on/off")
with device_cols[3]:
    st.button("Induction Hob", help="Toggle AC hob power relay")

st.markdown("---")

# --- SCENE BUTTONS ---
st.subheader("Scenes")
scene_cols = st.columns(3)
with scene_cols[0]:
    st.button("Night Mode", help="Turns off lights, powers down inverter")
with scene_cols[1]:
    st.button("Travel Mode", help="Disables AC, fridge to eco mode")
with scene_cols[2]:
    st.button("Stealth Mode", help="Disables all external lights & sound")

st.markdown("---")

# --- FOOTER ---
st.markdown("##### Alfred is always watching over your off-grid adventures.")
st.caption("v1.0.0 | Codename: ‘Dashboard Dawn’")

git init
git remote add origin https://github.com/your-username/alfred-dashboard.git
git add .
git commit -m "Initial prototype dashboard"
git push -u origin main