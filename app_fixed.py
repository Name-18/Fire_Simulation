from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import math
import random

# Optional geospatial deps (used only if available)
try:
    import rasterio
    from rasterio.transform import rowcol
    from pyproj import Transformer
except Exception:  # Modules might be missing on the user's machine
    rasterio = None
    rowcol = None
    Transformer = None

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)
CORS(app)

# Try to open rasters if they exist; fall back to synthetic mode.
landcover_path = os.path.join(BASE_DIR, "data", "landcover.tif")
elevation_path = os.path.join(BASE_DIR, "data", "elevation.tif")

HAVE_RASTERS = False
if rasterio is not None and os.path.exists(landcover_path) and os.path.exists(elevation_path):
    try:
        landcover_dataset = rasterio.open(landcover_path)
        elevation_dataset = rasterio.open(elevation_path)
        HAVE_RASTERS = True
    except Exception:
        HAVE_RASTERS = False

@app.get("/")
def home():
    # Renders the included demo UI at simulate_dir/templates/index.html
    return render_template("index.html")

def km_to_deg_lat(km: float) -> float:
    return km / 111.0  # approx

def km_to_deg_lon(km: float, lat_deg: float) -> float:
    return km / (111.320 * math.cos(math.radians(lat_deg)) + 1e-9)

def synthetic_fire_ring(lat: float, lon: float, hour: int, points: int = 60):
    """Return a 'ring' of lat/lon points expanding each hour.
    This lets the front-end visualize something even without rasters.
    """
    radius_km = max(0.1, 0.5 * hour)  # expand ~0.5 km per hour
    ring = []
    for i in range(points):
        ang = 2 * math.pi * i / points
        # small random wobble
        r = random.uniform(0.8, 1.2) * radius_km
        dlat = km_to_deg_lat(r) * math.sin(ang)
        dlon = km_to_deg_lon(r, lat) * math.cos(ang)
        ring.append({"lat": round(lat + dlat, 6), "lon": round(lon + dlon, 6)})
    return ring

import traceback

@app.post("/simulate")
def simulate():
    try:
        data = request.get_json(force=True) or {}
        lat = float(data.get("lat"))
        lon = float(data.get("lng"))
        hours = int(data.get("hours", 1))

        if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
            return jsonify({"error": "Invalid coordinates."}), 400

        # Your simulation logic
        burned_pixels = synthetic_fire_ring(lat, lon, hours, points=80)

        return jsonify({
            "burned_pixels": burned_pixels,
            "total_burned": len(burned_pixels),
            "hours_passed": hours
        })

    except Exception as e:
        print("🔥 Error in /simulate route:")
        traceback.print_exc()  # show full error in console
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Bind to 0.0.0.0 for cross-device testing; change as you like.
    app.run(host="0.0.0.0", port=5000, debug=True)