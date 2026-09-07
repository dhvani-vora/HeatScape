import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import requests
import numpy as np
import math
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="HeatScape",
    page_icon="🌍",
    layout="wide"
)

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0b0f14;
}

.block-container {
    padding-top: 1.5rem;
}

h1, h2, h3 {
    color: white;
}

p, label {
    color: #b8c1cc;
}

.recommendation {
    background: #14251b;
    border: 1px solid #32734a;
    padding: 22px;
    border-radius: 15px;
}

.livebox {
    background: #111d28;
    border: 1px solid #28506d;
    padding: 18px;
    border-radius: 15px;
}

.costbox {
    background: #171b22;
    border: 1px solid #303744;
    padding: 20px;
    border-radius: 15px;
}

.small {
    color: #8e9aaa;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOCALITIES
# =========================================================

localities = {

    "Anna Nagar": {
        "lat": 13.0850,
        "lon": 80.2101,
        "lst": 39.7,
        "ndvi": 0.25,
        "built": 82,
        "population": 78
    },

    "T Nagar": {
        "lat": 13.0418,
        "lon": 80.2341,
        "lst": 40.4,
        "ndvi": 0.20,
        "built": 88,
        "population": 86
    },

    "Adyar": {
        "lat": 13.0063,
        "lon": 80.2574,
        "lst": 38.1,
        "ndvi": 0.43,
        "built": 64,
        "population": 68
    },

    "Velachery": {
        "lat": 12.9750,
        "lon": 80.2212,
        "lst": 39.5,
        "ndvi": 0.29,
        "built": 76,
        "population": 80
    },

    "Perungudi": {
        "lat": 12.9600,
        "lon": 80.2400,
        "lst": 40.1,
        "ndvi": 0.24,
        "built": 79,
        "population": 74
    },

    "Sholinganallur": {
        "lat": 12.9010,
        "lon": 80.2279,
        "lst": 38.8,
        "ndvi": 0.34,
        "built": 69,
        "population": 72
    },

    "Tambaram": {
        "lat": 12.9249,
        "lon": 80.1000,
        "lst": 37.8,
        "ndvi": 0.42,
        "built": 63,
        "population": 67
    },

    "Guindy": {
        "lat": 13.0067,
        "lon": 80.2206,
        "lst": 39.6,
        "ndvi": 0.31,
        "built": 75,
        "population": 75
    },

    "Nungambakkam": {
        "lat": 13.0569,
        "lon": 80.2425,
        "lst": 40.0,
        "ndvi": 0.23,
        "built": 84,
        "population": 82
    },

    "Mylapore": {
        "lat": 13.0339,
        "lon": 80.2676,
        "lst": 39.2,
        "ndvi": 0.29,
        "built": 80,
        "population": 83
    },

    "Royapuram": {
        "lat": 13.1167,
        "lon": 80.2947,
        "lst": 41.0,
        "ndvi": 0.16,
        "built": 86,
        "population": 89
    },

    "Washermanpet": {
        "lat": 13.1150,
        "lon": 80.2800,
        "lst": 41.1,
        "ndvi": 0.15,
        "built": 87,
        "population": 91
    },

    "Perambur": {
        "lat": 13.1167,
        "lon": 80.2333,
        "lst": 40.5,
        "ndvi": 0.20,
        "built": 82,
        "population": 87
    },

    "Ambattur": {
        "lat": 13.1143,
        "lon": 80.1548,
        "lst": 40.2,
        "ndvi": 0.23,
        "built": 79,
        "population": 76
    },

    "Avadi": {
        "lat": 13.1147,
        "lon": 80.1017,
        "lst": 39.7,
        "ndvi": 0.31,
        "built": 70,
        "population": 73
    }
}


# =========================================================
# FUNCTIONS
# =========================================================

def normalize(value, minimum, maximum):

    return max(
        0,
        min(
            100,
            ((value - minimum) / (maximum - minimum)) * 100
        )
    )


def calculate_risk(lst, ndvi, built, population):

    heat = normalize(lst, 30, 45)

    vegetation_deficit = 100 - (ndvi * 100)

    risk = (
        0.45 * heat +
        0.25 * built +
        0.20 * vegetation_deficit +
        0.10 * population
    )

    return max(0, min(100, risk))


def get_category(risk):

    if risk < 25:
        return "Low"

    if risk < 50:
        return "Moderate"

    if risk < 75:
        return "High"

    return "Critical"


def get_contributions(lst, ndvi, built, population):

    heat = normalize(lst, 30, 45)

    vegetation_deficit = 100 - (ndvi * 100)

    return {
        "Surface Heat": 0.45 * heat,
        "Built-up Area": 0.25 * built,
        "Vegetation Deficit": 0.20 * vegetation_deficit,
        "Population Exposure": 0.10 * population
    }


def get_recommendation(lst, ndvi, built, population):

    contributions = get_contributions(
        lst,
        ndvi,
        built,
        population
    )

    dominant = max(
        contributions,
        key=contributions.get
    )

    if dominant == "Vegetation Deficit":

        return (
            "🌳 Tree Planting / Green Corridor",
            "Vegetation deficit is the dominant contributor. "
            "Increase tree cover along streets and connect existing green spaces."
        )

    if dominant == "Built-up Area":

        return (
            "🏠 Cool Roofs + Shade",
            "Dense built-up surfaces are absorbing significant heat. "
            "Prioritize reflective roofs and shaded public areas."
        )

    if dominant == "Population Exposure":

        return (
            "🚶 Shaded Public Corridor",
            "High population exposure makes pedestrian cooling infrastructure "
            "the most important first intervention."
        )

    return (
        "🌳 Green Corridor + Cool Roofs",
        "Surface heat is the dominant contributor. "
        "Combine vegetation with reflective built surfaces."
    )


# =========================================================
# LIVE WEATHER
# =========================================================

@st.cache_data(ttl=600)
def get_live_weather(lat, lon):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,"
        "apparent_temperature,wind_speed_10m"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        return data["current"]

    except:

        return None


# =========================================================
# OPENSTREETMAP ROADS
# =========================================================

@st.cache_data(ttl=3600)
def get_osm_roads(lat, lon):

    query = f"""
    [out:json][timeout:25];

    (
      way["highway"]
      (around:1800,{lat},{lon});
    );

    out geom;
    """

    url = "https://overpass-api.de/api/interpreter"

    try:

        response = requests.post(
            url,
            data=query,
            headers={
                "User-Agent":
                "HeatScape/1.0 urban-heat-hackathon"
            },
            timeout=30
        )

        return response.json()["elements"]

    except:

        return []


# =========================================================
# ROAD COLOR
# =========================================================

def road_color(highway):

    major = [
        "motorway",
        "trunk",
        "primary"
    ]

    medium = [
        "secondary",
        "tertiary"
    ]

    if highway in major:
        return "#ff5b5b"

    if highway in medium:
        return "#ffad42"

    return "#66717f"


# =========================================================
# THERMAL PLUME
# =========================================================

def create_heat_plume(lat, lon, risk):

    points = []

    radius = 0.018

    grid = 16

    for i in range(-grid, grid + 1):

        for j in range(-grid, grid + 1):

            dx = i / grid
            dy = j / grid

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            intensity = math.exp(
                -(distance ** 2) * 3
            )

            intensity *= risk / 100

            if intensity > 0.03:

                points.append(
                    [
                        lat + dx * radius,
                        lon + dy * radius,
                        intensity
                    ]
                )

    return points


# =========================================================
# ANIMATED HEAT CIRCLE
# =========================================================

def add_animated_circle(map_object, lat, lon, before, after):

    circle = folium.Circle(
        location=[lat, lon],
        radius=900,
        color="#ff0000",
        fill=True,
        fill_color="#ff0000",
        fill_opacity=0.22,
        weight=2
    )

    circle.add_to(map_object)

    circle_name = circle.get_name()

    script = f"""

    <script>

    (function() {{

        const circle = {circle_name};

        const start = {before};
        const end = {after};

        const duration = 2200;

        let startTime = null;

        function interpolate(a, b, t) {{
            return a + (b - a) * t;
        }}

        function riskColor(value) {{

            let r;
            let g;
            let b = 0;

            if (value >= 75) {{

                r = 255;
                g = Math.round(
                    interpolate(0, 80, (100-value)/25)
                );

            }} else if (value >= 50) {{

                r = 255;
                g = Math.round(
                    interpolate(165, 255, (75-value)/25)
                );

            }} else if (value >= 25) {{

                r = 255;
                g = Math.round(
                    interpolate(255, 255, (50-value)/25)
                );

                g = Math.round(
                    interpolate(165, 255, (50-value)/25)
                );

            }} else {{

                r = Math.round(
                    interpolate(255, 50, (25-value)/25)
                );

                g = 200;

            }}

            return `rgb(${{r}},${{g}},${{b}})`;
        }}

        function animate(timestamp) {{

            if (!startTime)
                startTime = timestamp;

            let progress =
                (timestamp - startTime) / duration;

            if (progress > 1)
                progress = 1;

            const value =
                interpolate(start, end, progress);

            const color =
                riskColor(value);

            circle.setStyle({{
                color: color,
                fillColor: color
            }});

            if (progress < 1) {{

                requestAnimationFrame(animate);

            }} else {{

                startTime = null;

                setTimeout(function() {{
                    requestAnimationFrame(animate);
                }}, 500);

            }}
        }}

        requestAnimationFrame(animate);

    }})();

    </script>
    """

    map_object.get_root().html.add_child(
        folium.Element(script)
    )


# =========================================================
# COST MODEL
# =========================================================

def calculate_costs(
    trees,
    roof_area,
    shade_structures
):

    # TREE COSTS

    tree_planting = trees * 650

    tree_first_year = trees * 300

    tree_annual_maintenance = trees * 250

    # COOL ROOF COSTS

    roof_installation = roof_area * 300

    roof_annual_maintenance = roof_area * 30

    # SHADE STRUCTURES

    shade_installation = shade_structures * 25000

    shade_annual_maintenance = shade_structures * 2500

    implementation = (
        tree_planting +
        tree_first_year +
        roof_installation +
        shade_installation
    )

    annual_maintenance = (
        tree_annual_maintenance +
        roof_annual_maintenance +
        shade_annual_maintenance
    )

    five_year_maintenance = annual_maintenance * 5

    five_year_total = (
        implementation +
        five_year_maintenance
    )

    return {
        "tree_planting": tree_planting,
        "tree_first_year": tree_first_year,
        "tree_maintenance": tree_annual_maintenance,
        "roof_installation": roof_installation,
        "roof_maintenance": roof_annual_maintenance,
        "shade_installation": shade_installation,
        "shade_maintenance": shade_annual_maintenance,
        "implementation": implementation,
        "annual_maintenance": annual_maintenance,
        "five_year_maintenance": five_year_maintenance,
        "five_year_total": five_year_total
    }


# =========================================================
# SIMULATION
# =========================================================

def simulate_risk(
    risk,
    trees,
    roof_area,
    shade_structures
):

    tree_effect = min(
        (trees / 2000) * 12,
        12
    )

    roof_effect = min(
        (roof_area / 50000) * 10,
        10
    )

    shade_effect = min(
        (shade_structures / 100) * 5,
        5
    )

    reduction = (
        tree_effect +
        roof_effect +
        shade_effect
    )

    return max(
        0,
        risk - reduction
    )


# =========================================================
# HEADER
# =========================================================

st.title("🌍 HeatScape")

st.write(
    "### Urban Heat Reduction Planner"
)

st.write(
    "Locality → Live conditions → Heat plume → Road-level planning → "
    "Intervention → Lifecycle cost"
)

st.divider()


# =========================================================
# LOCALITY SELECTOR
# =========================================================

st.sidebar.title("📍 Locality")

selected = st.sidebar.selectbox(
    "Choose a Chennai locality",
    list(localities.keys())
)

data = localities[selected]

lat = data["lat"]
lon = data["lon"]


# =========================================================
# LIVE WEATHER
# =========================================================

weather = get_live_weather(
    lat,
    lon
)

live_temperature = None

if weather:

    live_temperature = weather["temperature_2m"]

    live_humidity = weather["relative_humidity_2m"]

    live_apparent = weather["apparent_temperature"]

    live_wind = weather["wind_speed_10m"]

else:

    live_temperature = data["lst"]

    live_humidity = 0

    live_apparent = data["lst"]

    live_wind = 0


# =========================================================
# LIVE HEAT ADJUSTMENT
# =========================================================

live_heat_component = normalize(
    live_temperature,
    25,
    45
)

base_heat_component = normalize(
    data["lst"],
    30,
    45
)

combined_heat = (
    0.65 * base_heat_component +
    0.35 * live_heat_component
)

vegetation_deficit = 100 - (
    data["ndvi"] * 100
)

risk = (
    0.45 * combined_heat +
    0.25 * data["built"] +
    0.20 * vegetation_deficit +
    0.10 * data["population"]
)

risk = max(
    0,
    min(100, risk)
)

category = get_category(risk)


# =========================================================
# LIVE DATA PANEL
# =========================================================

st.subheader(f"📍 {selected}")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Heat Risk",
        f"{risk:.0f}/100"
    )

with col2:

    st.metric(
        "Live Temperature",
        f"{live_temperature:.1f} °C"
    )

with col3:

    st.metric(
        "Feels Like",
        f"{live_apparent:.1f} °C"
    )

with col4:

    st.metric(
        "Humidity",
        f"{live_humidity:.0f}%"
    )

st.markdown(
    f"""
    <div class="livebox">

    🟢 <b>LIVE ENVIRONMENTAL DATA</b><br>

    Temperature: {live_temperature:.1f} °C<br>
    Apparent temperature: {live_apparent:.1f} °C<br>
    Humidity: {live_humidity:.0f}%<br>
    Wind: {live_wind:.1f} km/h

    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Live atmospheric conditions are retrieved from Open-Meteo. "
    "Satellite-derived surface heat remains a separate data layer."
)

st.write(
    f"**Current Heat Risk:** {category}"
)

st.divider()


# =========================================================
# THERMAL PLUME MAP
# =========================================================

st.subheader("🔥 Local Thermal Plume + Road Network")

st.write(
    "The red/yellow plume shows the modeled spatial spread of heat risk. "
    "Roads are pulled from OpenStreetMap for planning at street level."
)

m = folium.Map(
    location=[lat, lon],
    zoom_start=13,
    tiles="OpenStreetMap"
)


# Thermal plume

plume = create_heat_plume(
    lat,
    lon,
    risk
)

HeatMap(
    plume,
    radius=28,
    blur=25,
    max_zoom=15,
    min_opacity=0.25
).add_to(m)


# OSM roads

roads = get_osm_roads(
    lat,
    lon
)

road_layer = folium.FeatureGroup(
    name="OpenStreetMap Roads"
)

for road in roads:

    geometry = road.get(
        "geometry",
        []
    )

    tags = road.get(
        "tags",
        {}
    )

    highway = tags.get(
        "highway",
        "road"
    )

    name = tags.get(
        "name",
        "Unnamed road"
    )

    if len(geometry) < 2:
        continue

    coordinates = [
        [
            point["lat"],
            point["lon"]
        ]
        for point in geometry
    ]

    folium.PolyLine(
        coordinates,
        color=road_color(highway),
        weight=4 if highway in [
            "motorway",
            "trunk",
            "primary"
        ] else 2,
        opacity=0.75,
        tooltip=f"{name} — {highway}"
    ).add_to(road_layer)

road_layer.add_to(m)


# Locality centre

folium.Marker(
    [lat, lon],
    popup=f"{selected} — Risk {risk:.0f}/100",
    tooltip=selected,
    icon=folium.Icon(
        color="red",
        icon="fire"
    )
).add_to(m)


folium.LayerControl().add_to(m)


st_folium(
    m,
    width=1200,
    height=600
)

st.caption(
    "© OpenStreetMap contributors. Road data is retrieved from OpenStreetMap."
)


# =========================================================
# HEAT FINGERPRINT
# =========================================================

st.divider()

st.subheader("🧬 Heat Fingerprint")

contributions = get_contributions(
    data["lst"],
    data["ndvi"],
    data["built"],
    data["population"]
)

for name, value in sorted(
    contributions.items(),
    key=lambda x: x[1],
    reverse=True
):

    st.write(
        f"**{name} — {value:.1f} points**"
    )

    st.progress(
        min(100, int(value))
    )


# =========================================================
# RECOMMENDATION
# =========================================================

st.divider()

recommendation, reason = get_recommendation(
    data["lst"],
    data["ndvi"],
    data["built"],
    data["population"]
)

st.subheader("💡 Recommended First Intervention")

st.markdown(
    f"""
    <div class="recommendation">

    <h2>{recommendation}</h2>

    <p>{reason}</p>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# INTERVENTION SIMULATOR
# =========================================================

st.divider()

st.subheader("🔬 Intervention Simulator")

st.write(
    "Move the sliders and watch the modeled thermal plume transition "
    "from 🔴 critical → 🟡 moderate → 🟢 lower risk."
)

col1, col2, col3 = st.columns(3)

with col1:

    trees = st.slider(
        "🌳 Trees planted",
        0,
        2000,
        500,
        100
    )

with col2:

    roof_area = st.slider(
        "🏠 Cool roof area (m²)",
        0,
        50000,
        10000,
        5000
    )

with col3:

    shade_structures = st.slider(
        "🚶 Shade structures",
        0,
        100,
        10,
        5
    )


new_risk = simulate_risk(
    risk,
    trees,
    roof_area,
    shade_structures
)

reduction = risk - new_risk


# =========================================================
# BEFORE AFTER
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Before",
        f"{risk:.0f}/100"
    )

with col2:

    st.metric(
        "After",
        f"{new_risk:.0f}/100"
    )

with col3:

    st.metric(
        "Risk Reduction",
        f"{reduction:.1f}"
    )


# =========================================================
# INTERVENTION MAP
# =========================================================

st.subheader("🗺️ Intervention Impact Map")

before_map = folium.Map(
    location=[lat, lon],
    zoom_start=13,
    tiles="OpenStreetMap"
)


# Before plume

before_plume = create_heat_plume(
    lat,
    lon,
    risk
)

HeatMap(
    before_plume,
    radius=28,
    blur=25,
    max_zoom=15,
    min_opacity=0.20
).add_to(before_map)


# Animated risk zone

add_animated_circle(
    before_map,
    lat,
    lon,
    risk,
    new_risk
)


# Road network

for road in roads:

    geometry = road.get(
        "geometry",
        []
    )

    tags = road.get(
        "tags",
        {}
    )

    highway = tags.get(
        "highway",
        "road"
    )

    name = tags.get(
        "name",
        "Unnamed road"
    )

    if len(geometry) < 2:
        continue

    coordinates = [
        [
            point["lat"],
            point["lon"]
        ]
        for point in geometry
    ]

    folium.PolyLine(
        coordinates,
        color=road_color(highway),
        weight=3,
        opacity=0.65,
        tooltip=name
    ).add_to(before_map)


folium.Marker(
    [lat, lon],
    popup=(
        f"{selected}<br>"
        f"Before: {risk:.0f}<br>"
        f"After: {new_risk:.0f}"
    ),
    tooltip="Intervention impact"
).add_to(before_map)


st_folium(
    before_map,
    width=1200,
    height=600
)

st.caption(
    "The animated colour transition is a modeled intervention visualization, "
    "not a measured satellite temperature change."
)


# =========================================================
# COST ESTIMATION
# =========================================================

st.divider()

st.subheader("💰 Lifecycle Cost Estimation")

st.write(
    "HeatScape does not stop at installation cost. "
    "It estimates the cost of keeping the intervention functional."
)

costs = calculate_costs(
    trees,
    roof_area,
    shade_structures
)


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Initial Implementation",
        f"₹{costs['implementation']:,.0f}"
    )

with col2:

    st.metric(
        "Annual Maintenance",
        f"₹{costs['annual_maintenance']:,.0f}"
    )

with col3:

    st.metric(
        "5-Year Total",
        f"₹{costs['five_year_total']:,.0f}"
    )


st.markdown(
    f"""
    <div class="costbox">

    ### 🌳 Trees

    Planting + soil + establishment:
    **₹{costs['tree_planting'] + costs['tree_first_year']:,.0f}**

    Annual watering / fertilizer / pruning / care:
    **₹{costs['tree_maintenance']:,.0f} / year**

    ---

    ### 🏠 Cool Roofs

    Installation:
    **₹{costs['roof_installation']:,.0f}**

    Annual maintenance / upkeep:
    **₹{costs['roof_maintenance']:,.0f} / year**

    ---

    ### 🚶 Shade Structures

    Installation:
    **₹{costs['shade_installation']:,.0f}**

    Annual maintenance:
    **₹{costs['shade_maintenance']:,.0f} / year**

    ---

    ### 💰 Lifecycle View

    Initial implementation:
    **₹{costs['implementation']:,.0f}**

    5-year maintenance:
    **₹{costs['five_year_maintenance']:,.0f}**

    **5-YEAR TOTAL:
    ₹{costs['five_year_total']:,.0f}**

    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Planning estimates only. Rates should be replaced with approved GCC/PWD "
    "schedule rates or local tender rates for implementation."
)


# =========================================================
# METHODOLOGY
# =========================================================

st.divider()

with st.expander("📊 Data & Methodology"):

    st.write("""
    ### Current live layer

    • Open-Meteo → current temperature, humidity, apparent temperature and wind

    • OpenStreetMap → roads and road classification

    ### Heat model

    Heat Risk =
    0.45 × Heat +
    0.25 × Built-up +
    0.20 × Vegetation Deficit +
    0.10 × Population Exposure

    ### Planned satellite layer

    • Landsat 8/9 → Surface Temperature

    • Sentinel-2 → NDVI

    • Copernicus land cover → Built-up / land cover

    • WorldPop → Population exposure

    ### Important

    The thermal plume currently represents a spatialized model of the
    hotspot rather than measured satellite temperature at every pixel.

    The next version can replace the modeled plume with real
    satellite-derived LST.
    """)

st.caption(
    f"HeatScape • Last interface refresh: "
    f"{datetime.now().strftime('%d %b %Y, %H:%M:%S')}"
)
