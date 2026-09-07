from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ai.recommendations import recommend

app = FastAPI(title="HeatScape API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("data/sample_hotspots.json") as f:
    hotspots = json.load(f)


@app.get("/")
def home():
    return {"message": "HeatScape API is running"}


@app.get("/hotspots")
def get_hotspots():
    return hotspots


@app.get("/hotspots/{hotspot_id}")
def get_hotspot(hotspot_id: int):

    hotspot = next(
        (h for h in hotspots if h["id"] == hotspot_id),
        None
    )

    if not hotspot:
        return {"error": "Hotspot not found"}

    recommendations = recommend({
        "heat": hotspot["heat"],
        "vegetation": hotspot["vegetation"],
        "built_up": hotspot["built_up"],
        "population": hotspot["population"],
        "road_density": hotspot["road_density"]
    })

    return {
        **hotspot,
        "recommendations": recommendations
    }
