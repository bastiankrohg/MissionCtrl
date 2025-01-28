# Mission Control for AutoPi Rover Project

Welcome to the Mission Control component of the AutoPi Rover project! This module acts as the ground station for monitoring telemetry data, video feeds, and controlling the rover's operations. Designed to work alongside the rover hardware, this application provides a centralized dashboard for all mission-critical insights.

---

## Features

### 1. **Telemetry Monitoring**
- Receive telemetry data from the rover, such as position, heading, battery level, CPU usage, and sensor measurements.
- Display telemetry data in real-time on an interactive dashboard.
- Visualize historical data trends for battery, ultrasound, and CPU usage.

### 2. **Live Video Feed**
- Stream MJPEG video from the rover's camera to the dashboard.
- Automatically updates and displays the feed within the dashboard interface.

### 3. **Proximity and System State Indicators**
- Show real-time ultrasound proximity measurements.
- Monitor rover system health, including CPU usage, memory availability, and disk usage.

### 4. **Interactive Dashboard**
- Built with Dash and Plotly for rich visualizations and a responsive UI.
- Includes graphs, indicators, and the live feed integrated into a single interface.

---

## System Architecture

The Mission Control application communicates with the rover and Coral retransmission system via TCP. It processes telemetry data and displays it in real-time for mission operators.

### Components:
1. **TCP Listener**
   - Receives telemetry data from the Coral device.
   - Ensures reliable data transmission using a queue mechanism.

2. **Dashboard**
   - A Dash-based web application for displaying telemetry data, graphs, and the video feed.

3. **Video Feed Integration**
   - Uses an MJPEG stream embedded directly into the dashboard.
   - Displays the live camera feed from the rover.

---

## Installation

### Prerequisites
1. **Python 3.10+**
2. **Virtual Environment (Optional)**
   ```bash
   python3 -m venv missionctrl_env
   source missionctrl_env/bin/activate
   ```
3. **Required Python Packages**
   ```bash
   pip install -r requirements.txt
   ```

### Clone the Repository
```bash
git clone https://github.com/bastiankrohg/AutoPi.git
cd AutoPi/MissionCtrl
```

### MJPEG Stream Configuration
Ensure that the rover's MJPEG server is running and accessible. Update the video feed URL in `dashboard_layout.py` to match the rover's IP address and port:
```python
VIDEO_SOURCE = "http://<ROVER_IP>:8080/stream"
```

---

## Usage

### Run the Mission Control Dashboard
Start the application with:
```bash
python app.py
```

Access the dashboard in your browser:
```
http://127.0.0.1:8050/
```

---

## Files Overview

### `app.py`
- The main entry point for Mission Control.
- Starts the dashboard, TCP listener, and video stream integration.

### `dashboard_layout.py`
- Defines the layout and components of the Dash application.
- Includes telemetry graphs, live feed, and system state displays.

### `tcp_listener.py`
- Handles incoming telemetry data via TCP.
- Buffers data for real-time and historical visualization.

### `requirements.txt`
- Specifies the dependencies needed for the project.

---

## Dashboard Layout

### **Top Section**
- **Backend Status:** Shows connection status with the rover.
- **Path Trace:** Real-time visualization of the rover's movements.

### **Middle Section**
- **Live Video Feed:** Displays the rover's camera feed.
- **System State Indicators:** Shows CPU usage, memory, disk usage, and battery levels.

### **Bottom Section**
- **Graphs:** Historical data for battery, ultrasound, and CPU usage over time.

---

## Troubleshooting

### 1. **No Telemetry Data**
- Ensure the Coral retransmission server is running and the TCP connection is correctly configured.
- Check network connectivity between the rover, Coral, and Mission Control.

### 2. **Video Feed Not Displaying**
- Confirm the MJPEG stream URL is correct.
- Ensure the rover's camera server is running.

---

## Future Enhancements
1. **Link Monitoring:**
   - Add status indicators for the connection between the rover, Coral, and Mission Control.
2. **Command Center:**
   - Include rover control options directly in the dashboard.
3. **Customizable Metrics:**
   - Allow operators to define which telemetry data to display.

