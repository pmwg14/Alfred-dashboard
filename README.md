# Alfred-dashboard

# Alfred Dashboard

**Prototype interface for in-van system control and monitoring**

Alfred Dashboard is a Streamlit-based web app designed to run on an iPad Mini mounted in a campervan. It displays live (mocked) system data and includes interactive buttons to control lighting, devices, and scenes.

> This is a prototype build – buttons and displays are not yet connected to real devices. Each item includes a tooltip describing the planned integration.

---

## Features

- **Renogy 12V System monitoring**
- **EcoFlow Delta Pro status**
- **Starlink connectivity check**
- **Wi-Fi device count**
- **Temperature, humidity, water tank levels**
- **Lighting & device control buttons**
- **Scene presets (e.g. Night Mode, Travel Mode)**
- **Tooltips on all controls to describe future functionality**

---

## Usage

To run the dashboard locally:

```bash
streamlit run alfred_dashboard.py