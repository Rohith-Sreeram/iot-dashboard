# Implementation Plan - Streamlit IoT Dashboard

This plan outlines the migration from a pure Flask app to a **Streamlit** based IoT Dashboard while maintaining compatibility with ESP32 communication.

## 1. Architecture Overview
- **Data Store**: `iot_data.json` will act as a shared state between the Streamlit UI and the API bridge.
- **Frontend**: Streamlit app providing real-time metrics and control inputs.
- **API Bridge**: A lightweight Flask server specifically for the ESP32 to send/receive data.

## 2. Components

### A. Streamlit Dashboard (`streamlit_app.py`)
- **Metric Cards**: Displaying "Entered", "Left", and "Present" people.
- **Remote Control**: Forms to set new values for the ESP32 variables.
- **Auto-polling**: Using Streamlit's fragment or reload mechanism to keep data fresh.
- **Visuals**: A simple bar/line chart showing the current breakdown.

### B. API Bridge (`api_bridge.py`)
- **Endpoint `POST /api/iot`**: 
    - Receives: `{"entered": x, "left": y, "present": z}`
    - Returns: `{"refresh": {"entered": a, "left": b, "present": c, "pending": bool}}`
- **Shared Access**: Reads and writes to `iot_data.json` with basic locking.

## 3. Implementation Steps

1. **Setup Shared State**: Initialize `iot_data.json` with default values.
2. **Develop Streamlit UI**: 
    - Layout with `st.columns` for metrics.
    - Sidebar or bottom section for "Cloud Sync Settings".
    - "Sync to ESP32" button that updates the JSON state.
3. **Develop API Bridge**:
    - Build a small Flask app to handle the hardware-level communication.
4. **Testing**: 
    - Run the API and Dashboard simultaneously.
    - Simulate ESP32 requests using `curl` or Postman.

## 4. Aesthetic Design (Premium Look)
- Custom CSS for glassmorphism effect in Streamlit.
- Using `st.metric` with delta indicators.
- High-contrast dark theme.
