import streamlit as st
import random
import pandas as pd
import pydeck as pdk
from datetime import datetime
import openrouteservice

# OpenRouteService client
ors_client = openrouteservice.Client(key="5b3ce3597851110001cf6248faab8eb43c574edea6693d9d1d5b05ef")

# Set up layout
st.set_page_config(layout="wide", page_title="Alfred Dashboard v2.1", page_icon="⚡")

# Tabs
tab1, tab2 = st.tabs(["Dashboard", "Journey Planner"])

# Shared functions
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

def estimate_distance_miles(from_loc, to_loc):
    lat1, lon1 = from_loc["lat"], from_loc["lon"]
    lat2, lon2 = to_loc["lat"], to_loc["lon"]
    return round(((lat1 - lat2)**2 + (lon1 - lon2)**2)**0.5 * 69, 1)

def estimate_travel_time_mins(distance_miles):
    return round(distance_miles / 40 * 60)

def estimate_alternator_charge_kwh(travel_minutes):
    return round((travel_minutes / 60) * 0.5, 2)

# Refresh button
if st.button("🔧 Refresh Mock Data"):
    st.session_state.clear()
    st.rerun()

# ---------------- Dashboard Tab ---------------- #
with tab1:
    st.title("Alfred Dashboard – v2.2")
    st.caption(f"{datetime.now().strftime('%A %d %B %Y, %H:%M:%S')}")

    init_mock("gps_location", lambda: random.choice(locations))
    loc = st.session_state["gps_location"]

    # Sunrise/Sunset placeholder for June 18
    next_event = "Sunrise: 04:39 | Sunset: 21:23 (18 June)"

    st.markdown(f"**Current GPS Location:** {loc['name']} | {next_event}")
    st.markdown(f"Lat: `{loc['lat']}`, Lon: `{loc['lon']}`")

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=loc["lat"], longitude=loc["lon"], zoom=6),
        layers=[
            pdk.Layer("ScatterplotLayer", data=[loc], get_position='[lon, lat]',
                      get_color='[200, 30, 0, 160]', get_radius=10000)
        ],
    ))

    st.divider()

    # Power system
    init_mock("renogy_voltage", lambda: round(random.uniform(12.4, 13.2), 2))
    init_mock("renogy_soc", lambda: random.randint(70, 100))
    init_mock("solar_input", lambda: random.randint(0, 360))
    init_mock("dc_load", lambda: random.randint(30, 80))
    init_mock("ecoflow_soc", lambda: random.randint(40, 80))
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

    st.subheader("Device Controls (Prototype)")

    colA, colB, colC = st.columns(3)

    with colA:
        light_on = st.button("Toggle Lights", help="This will eventually control 12V LED circuits via a Raspberry Pi relay.")
    with colB:
        fan_on = st.button("Toggle Vent Fan", help="Will trigger an inline 12V fan connected via a smart switch or GPIO.")
    with colC:
        heater_on = st.button("Toggle Diesel Heater", help="Will send signal to heater controller via GPIO or smart relay.")

    st.caption("These buttons are not connected yet — Alfred will command relays via Raspberry Pi or a home automation bridge in a future version.")

    # Connectivity
    init_mock("starlink_download", lambda: random.randint(80, 120))
    init_mock("starlink_upload", lambda: random.randint(10, 20))
    init_mock("wifi_devices", lambda: random.randint(4, 10))
    init_mock("starlink_history", lambda: pd.DataFrame(columns=["🛜 Download", "Upload"]))

    new_row = pd.DataFrame({
        "🛜 Download": [st.session_state['starlink_download']],
        "Upload": [st.session_state['starlink_upload']]
    })
    st.session_state['starlink_history'] = pd.concat([
        st.session_state['starlink_history'], new_row
    ]).tail(20)

    st.subheader("Connectivity")
    col3, col4 = st.columns(2)
    with col3:
        st.metric("Starlink Status", "Online")
        st.metric("🛜 Download Speed", f"{st.session_state['starlink_download']} Mbps")
        st.metric("Upload Speed", f"{st.session_state['starlink_upload']} Mbps")
        st.line_chart(st.session_state['starlink_history'], height=150, use_container_width=True)
    with col4:
        st.metric("Devices on WiFi", st.session_state['wifi_devices'])

    st.divider()

    # Environment
    init_mock("interior_temp", lambda: round(random.uniform(18.5, 23.0), 1))
    init_mock("humidity", lambda: random.randint(35, 60))
    init_mock("water_level", lambda: random.randint(40, 80))

    st.subheader("Environmental Monitoring")
    col5, col6, col7 = st.columns(3)
    with col5:
        st.metric("🌡️ Interior Temp", f"{st.session_state['interior_temp']}°C")
    with col6:
        st.metric("💦 Humidity", f"{st.session_state['humidity']}%")
    with col7:
        st.metric("Water Tank Level", f"{st.session_state['water_level']}%")

    st.divider()
    st.markdown("##### “It is my pleasure to assist, even if the satnav appears to be more confident than qualified.”")

import openrouteservice

import openrouteservice

# ---------------- Journey Planner Tab ---------------- #
with tab2:
    st.title("Journey Planner")

    st.markdown("Estimated fuel cost is based on a Ford Transit Mk8 (35 mpg UK).")
    diesel_price = st.number_input("Diesel Price (£/L)", min_value=1.00, max_value=2.50, value=1.65, step=0.01)

    from_choice = st.selectbox("Start Location", [loc["name"] for loc in locations])
    to_choice = st.selectbox("Destination", [loc["name"] for loc in locations])

    if from_choice != to_choice:
        from_loc = get_location(from_choice)
        to_loc = get_location(to_choice)

        # OpenRouteService client
        ors_client = openrouteservice.Client(key="5b3ce3597851110001cf6248faab8eb43c574edea6693d9d1d5b05ef")

        # Get route data
        try:
            route = ors_client.directions(
                coordinates=[[from_loc["lon"], from_loc["lat"]], [to_loc["lon"], to_loc["lat"]]],
                profile='driving-car',
                format='geojson'
            )

            summary = route['features'][0]['properties']['summary']
            distance_km = summary['distance'] / 1000
            distance_miles = round(distance_km * 0.621371, 1)
            duration_min = round(summary['duration'] / 60)
            hours, mins = divmod(duration_min, 60)

            # Fuel cost
            mpg = 35
            litres_per_mile = 4.546 / mpg
            fuel_cost = round(litres_per_mile * diesel_price * distance_miles, 2)

            # Alternator charging estimates
            added_kwh = estimate_alternator_charge_kwh(duration_min)
            added_percent = round((added_kwh / 7.2) * 100, 1)

            # SOC estimates
            renogy_soc = st.session_state['renogy_soc']
            ecoflow_soc = st.session_state['ecoflow_soc']
            renogy_after = min(100, round(renogy_soc + added_percent, 1))
            ecoflow_after = min(100, round(ecoflow_soc + added_percent, 1))
            recommend = "Renogy" if renogy_after < ecoflow_after else "EcoFlow Delta Pro"

            st.markdown(f"**Distance:** {distance_miles} miles")
            st.markdown(f"**Estimated Travel Time:** {hours}h {mins}m")
            st.markdown(f"**Estimated Fuel Cost:** £{fuel_cost}")
            st.markdown(f"**Alternator Charge Estimate:** {added_kwh} kWh")

            st.markdown(f"**Renogy SOC: {renogy_soc}% → {renogy_after}%**")
            st.markdown(f"**EcoFlow SOC: {ecoflow_soc}% → {ecoflow_after}%**")
            st.success(f"**Recommended system to charge via alternator:** {recommend}")

            # Mock weather
            mock_weather = random.choice(["Sunny", "Overcast", "Light Rain", "Windy", "Partly Cloudy"])
            temp = round(random.uniform(12, 22), 1)
            wind = random.randint(5, 25)
            st.markdown(f"**Weather at destination:** {mock_weather}, {temp}°C, Wind {wind} km/h")

            # Route map using OpenRouteService geometry
            coords = route['features'][0]['geometry']['coordinates']
            route_path = [{"path": coords}]
            route_df = pd.DataFrame(route_path)

            st.pydeck_chart(pdk.Deck(
                initial_view_state=pdk.ViewState(
                    latitude=(from_loc["lat"] + to_loc["lat"]) / 2,
                    longitude=(from_loc["lon"] + to_loc["lon"]) / 2,
                    zoom=6,
                ),
                layers=[
                    pdk.Layer(
                        "PathLayer",
                        data=route_df,
                        get_path="path",
                        get_width=4,
                        get_color=[0, 100, 255],
                        width_min_pixels=2
                    ),
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=[from_loc, to_loc],
                        get_position='[lon, lat]',
                        get_color='[255, 0, 0, 160]',
                        get_radius=8000
                    ),
                ],
            ))

        except Exception as e:
            st.error("Route calculation failed. Error: {e}")

    else:
        st.info("Select two different locations to plan a journey.")
