import streamlit as st
import random
from datetime import datetime

st.set_page_config(layout="wide", page_title="Alfred Dashboard", page_icon="⚡")

st.title("Alfred Dashboard – v1.0 (Prototype)")
st.caption(f"{datetime.now().strftime('%A %d %B %Y, %H:%M:%S')}")
st.markdown("**Location:** Approximate location via GPS module (planned)")

st.divider()

# --- REFRESH BUTTON ---
if st.button("🔄 Refresh Mock Data"):
    st.session_state.clear()
    st.rerun()

# --- INIT MOCK DATA ---
def init_mock(key, generator):
    if key not in st.session_state:
        st.session_state[key] = generator()

# Power values
init_mock("renogy_voltage", lambda: round(random.uniform(12.4, 13.2), 2))
init_mock("renogy_soc", lambda: random.randint(70, 100))
init_mock("solar_input", lambda: random.randint(0, 360))
init_mock("dc_load", lambda: random.randint(30, 80))

init_mock("ecoflow_soc", lambda: random.randint(50, 90))
init_mock("ecoflow_output", lambda: random.randint(100, 600))
init_mock("ecoflow_input", lambda: random.randint(0, 240))

# Connectivity
init_mock("starlink_download", lambda: random.randint(80, 120))
init_mock("starlink_upload", lambda: random.randint(10, 20))
init_mock("wifi_devices", lambda: random.randint(4, 10))

# Environment
init_mock("interior_temp", lambda: round(random.uniform(18.5, 23.0), 1))
init_mock("humidity", lambda: random.randint(35, 60))
init_mock("water_level", lambda: random.randint(40, 80))

# --- POWER SYSTEM SECTION ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Renogy 12V System")
    st.metric("Battery Voltage", f"{st.session_state['renogy_voltage']}V", help="Live data via Renogy One Core")
    st.metric("Battery SOC", f"{st.session_state['renogy_soc']}%", help="State of charge from Renogy batteries")
    st.metric("Solar Input", f"{st.session_state['solar_input']}W", help="MPPT controller solar wattage input")
    st.metric("DC Load", f"{st.session_state['dc_load']}W", help="Total 12V system draw")

with col2:
    st.subheader("EcoFlow Delta Pro")
    st.metric("Battery SOC", f"{st.session_state['ecoflow_soc']}%", help="EcoFlow battery state of charge")
    st.metric("AC Output", f"{st.session_state['ecoflow_output']}W", help="AC devices draw")
    st.metric("Input Power", f"{st.session_state['ecoflow_input']}W", help="Via solar or EV charging")

st.divider()

# --- CONNECTIVITY SECTION ---
st.subheader("Connectivity")
col3, col4 = st.columns(2)

with col3:
    st.metric("Starlink Status", "Online", help="Ping to satellite and WAN")
    st.metric("Download Speed", f"{st.session_state['starlink_download']} Mbps", help="Polled via Starlink local API")
    st.metric("Upload Speed", f"{st.session_state['starlink_upload']} Mbps", help="Polled via Starlink local API")

with col4:
    st.metric("Devices on WiFi", st.session_state['wifi_devices'], help="Connected devices to local router")

st.divider()

# --- ENVIRONMENT SECTION ---
st.subheader("Environmental Monitoring")
col5, col6, col7 = st.columns(3)

with col5:
    st.metric("Interior Temp", f"{st.session_state['interior_temp']}°C", help="From BME280 sensor in van cabin")

with col6:
    st.metric("Humidity", f"{st.session_state['humidity']}%", help="From DHT22 or BME280 sensor")

with col7:
    st.metric("Water Tank Level", f"{st.session_state['water_level']}%", help="From analogue tank sensor")

st.divider()

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

st.divider()

# --- SCENE BUTTONS ---
st.subheader("Scenes")
scene_cols = st.columns(3)
with scene_cols[0]:
    st.button("Night Mode", help="Turns off lights, powers down inverter")
with scene_cols[1]:
    st.button("Travel Mode", help="Disables AC, fridge to eco mode")
with scene_cols[2]:
    st.button("Stealth Mode", help="Disables all external lights & sound")

st.divider()

# --- FOOTER ---
st.markdown("##### Alfred is always watching over your off-grid adventures.")
st.caption("v1.0.0 | Codename: ‘Dashboard Dawn’")