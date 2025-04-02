import streamlit as st
import random
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide", page_title="Alfred Dashboard v2", page_icon="⚡")

# --- Page Tabs ---
tab1, tab2 = st.tabs(["Dashboard", "Journey Planner"])

# --- Shared Helpers ---
def init_mock(key, generator):
    if key not in st.session_state:
        st.session_state[key] = generator()

locations = [
    {"name": "Salcombe, Devon", "lat": 50.2370, "lon": -3.7766},
    {"name": "Eller How House, Lake District", "lat": 54.2130, "lon": -2.8765},
    {"name": "Ullswater, Lake District", "lat": 54.5870, "lon": -2.8534},
    {"name": "Marymount, Raggleswood, Chislehurst", "lat": 51.4062, "lon": 0.0577},
    {"name": "Stoke Mandeville", "lat": 51.7872, "lon": -0.7934},
]

def get_location(name):
    return next(loc for loc in locations if loc["name"] == name)

def estimate_distance_km(from_loc, to_loc):
    # rough approximation using haversine-like calc
    lat1, lon1 = from_loc["lat"], from_loc["lon"]
    lat2, lon2 = to_loc["lat"], to_loc["lon"]
    return round(((lat1 - lat2)**2 + (lon1 - lon2)**2)**0.5 * 111, 1)  # 111km ≈ 1 degree

def estimate_travel_time_km(distance_km):
    return round(distance_km / 65 * 60)  # assume 65km/h average speed

def estimate_alternator_charge_kwh(travel_minutes):
    return round((travel_minutes / 60) * 0.5, 2)  # 0.5kWh per hour driving

# --- Refresh Mock Button ---
if st.button("🔄 Refresh Mock Data"):
    st.session_state.clear()
    st.rerun()

# ========== TAB 1: DASHBOARD ==========
with tab1:
    st.title("Alfred Dashboard – v2.0")
    st.caption(f"{datetime.now().strftime('%A %d %B %Y, %H:%M:%S')}")

    # --- GPS Mock Location ---
    init_mock("gps_location", lambda: random.choice(locations))
    loc = st.session_state["gps_location"]
    st.markdown(f"**Current GPS Location:** {loc['name']}")
    st.markdown(f"Lat: `{loc['lat']}`, Lon: `{loc['lon']}`")
    st.map(pd.DataFrame([{"lat": loc['lat'], "lon": loc['lon']}]), zoom=10)
    st.divider()

    # --- Power System Data ---
    init_mock("renogy_voltage", lambda: round(random.uniform(12.4, 13.2), 2))
    init_mock("renogy_soc", lambda: random.randint(70, 100))
    init_mock("solar_input", lambda: random.randint(0, 360))
    init_mock("dc_load", lambda: random.randint(30, 80))
    init_mock("ecoflow_soc", lambda: random.randint(50, 90))
    init_mock("ecoflow_output", lambda: random.randint(100, 600))
    init_mock("ecoflow_input", lambda: random.randint(0, 240))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Renogy 12V System")
        st.metric("Battery Voltage", f"{st.session_state['renogy_voltage']}V")
        st.metric("Battery SOC", f"{st.session_state['renogy_soc']}%")
        st.metric("Solar Input", f"{st.session_state['solar_input']}W")
        st.metric("DC Load", f"{st.session_state['dc_load']}W")

    with col2:
        st.subheader("EcoFlow Delta Pro")
        st.metric("Battery SOC", f"{st.session_state['ecoflow_soc']}%")
        st.metric("AC Output", f"{st.session_state['ecoflow_output']}W")
        st.metric("Input Power", f"{st.session_state['ecoflow_input']}W")

    st.divider()

    # --- Starlink Connectivity ---
    init_mock("starlink_download", lambda: random.randint(80, 120))
    init_mock("starlink_upload", lambda: random.randint(10, 20))
    init_mock("wifi_devices", lambda: random.randint(4, 10))

    init_mock("starlink_history", lambda: pd.DataFrame(columns=["Download", "Upload"]))
    new_row = pd.DataFrame({
        "Download": [st.session_state['starlink_download']],
        "Upload": [st.session_state['starlink_upload']]
    })
    st.session_state['starlink_history'] = pd.concat([
        st.session_state['starlink_history'], new_row
    ]).tail(20)

    st.subheader("Connectivity")
    col3, col4 = st.columns(2)
    with col3:
        st.metric("Starlink Status", "Online")
        st.metric("Download Speed", f"{st.session_state['starlink_download']} Mbps")
        st.metric("Upload Speed", f"{st.session_state['starlink_upload']} Mbps")
        st.line_chart(st.session_state['starlink_history'], height=150, use_container_width=True)

    with col4:
        st.metric("Devices on WiFi", st.session_state['wifi_devices'])

    st.divider()

    # --- Environmental Sensors ---
    init_mock("interior_temp", lambda: round(random.uniform(18.5, 23.0), 1))
    init_mock("humidity", lambda: random.randint(35, 60))
    init_mock("water_level", lambda: random.randint(40, 80))

    st.subheader("Environmental Monitoring")
    col5, col6, col7 = st.columns(3)

    with col5:
        st.metric("Interior Temp", f"{st.session_state['interior_temp']}°C")

    with col6:
        st.metric("Humidity", f"{st.session_state['humidity']}%")

    with col7:
        st.metric("Water Tank Level", f"{st.session_state['water_level']}%")

    st.divider()

    # --- Device Controls ---
    st.subheader("Lighting & Device Control")
    lighting_cols = st.columns(3)
    with lighting_cols[0]:
        st.button("Kitchen Lights")
    with lighting_cols[1]:
        st.button("Ceiling Lights")
    with lighting_cols[2]:
        st.button("Bedside Scene")

    device_cols = st.columns(4)
    with device_cols[0]:
        st.button("Fridge Power")
    with device_cols[1]:
        st.button("Roof Fan")
    with device_cols[2]:
        st.button("Inverter")
    with device_cols[3]:
        st.button("Induction Hob")

    st.divider()
    st.subheader("Scenes")
    scene_cols = st.columns(3)
    with scene_cols[0]:
        st.button("Night Mode")
    with scene_cols[1]:
        st.button("Travel Mode")
    with scene_cols[2]:
        st.button("Stealth Mode")

    st.divider()
    st.markdown("##### “It is my pleasure to assist, even if the satnav appears to be more confident than qualified.”")

# ========== TAB 2: JOURNEY PLANNER ==========
with tab2:
    st.title("Journey Planner")

    from_choice = st.selectbox("Start Location", [loc["name"] for loc in locations])
    to_choice = st.selectbox("Destination", [loc["name"] for loc in locations])

    if from_choice != to_choice:
        from_loc = get_location(from_choice)
        to_loc = get_location(to_choice)
        distance_km = estimate_distance_km(from_loc, to_loc)
        travel_time_min = estimate_travel_time_km(distance_km)
        charge_estimate = estimate_alternator_charge_kwh(travel_time_min)

        st.markdown(f"**Distance:** {distance_km} km")
        st.markdown(f"**Estimated Travel Time:** {travel_time_min} minutes")
        st.markdown(f"**Estimated Alternator Charge:** {charge_estimate} kWh (via 40A DC-DC)")

        st.map(pd.DataFrame([
            {"lat": from_loc["lat"], "lon": from_loc["lon"]},
            {"lat": to_loc["lat"], "lon": to_loc["lon"]}
        ]), zoom=5)
    else:
        st.info("Select two different locations to plan a journey.")