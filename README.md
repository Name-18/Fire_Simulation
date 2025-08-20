# 🔥 Wildfire Simulation

An interactive wildfire spread simulation web app built with **Flask**, **Leaflet.js**, and **Geospatial Libraries** (`rasterio`, `pyproj`).  
Users can click anywhere on the map to set an ignition point, then watch the simulated fire spread hour by hour.  

---

## 🚀 Features
- 🌍 **Interactive Map** (Leaflet + Google Satellite tiles)  
- 📍 **Ignition Point Selection** by clicking anywhere on the map  
- 🔄 **Real-time Fire Spread Simulation**  
- 🎨 **Fading Fire Effect** (red → orange → dull red) to mimic real fire dynamics  
- 📊 **Live Stats**:  
  - Area burned (km²)  
  - Hours passed since ignition  
- ⚡ **REST API Backend** (`/simulate`) built with Flask + Gunicorn  
- 🖥️ **Frontend-Backend Integration** for smooth user experience  

---

## 🛠️ Tech Stack
- **Backend**: Flask, Gunicorn, Rasterio, PyProj  
- **Frontend**: Leaflet.js, Vanilla JS, HTML/CSS  
- **Deployment**: Render (or any other cloud platform)  
- **Language**: Python 3.10+  


