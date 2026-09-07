import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import requests
import math
from datetime import datetime

# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="HeatScape",
    page_icon="🌍",
    layout="wide"
)

# =========================================================
# BEAUTIFUL HEATSCAPE THEME
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(255,91,54,0.08), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(255,184,77,0.06), transparent 25%),
        #0b1117;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1 {
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    letter-spacing: -2px;
}

h2 {
    font-weight: 750 !important;
}

h3 {
    font-weight: 700 !important;
}

p, label {
    color: #b8c5d1 !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #151e27,
        #10171e
    );
    border: 1px solid #273542;
    padding: 18px;
    border-radius: 16px;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

[data-testid="stMetricLabel"] {
    color: #91a1b1 !important;
}

.recommendation {
    background:
        linear-gradient(
            135deg,
            rgba(42, 130, 75, 0.20),
            rgba(20, 35, 27, 0.95)
        );
    border: 1px solid #2f8150;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.20);
}

.livebox {
    background:
        linear-gradient(
            135deg,
            rgba(25, 91, 116, 0.22),
            rgba(13, 25, 35, 0.95)
        );
    border: 1px solid #27617a;
    padding: 20px;
    border-radius: 18px;
}

.costbox {
    background:
        linear-gradient(
            135deg,
            rgba(255, 165, 70, 0.08),
            rgba(19, 24, 30, 0.98)
        );
    border: 1px solid #554330;
    padding: 25px;
    border-radius: 18px;
}

.section {
    background: #101820;
    border: 1px solid #22303c;
    border-radius: 18px;
    padding: 20px;
}

.stSlider > div > div > div {
    background: #f07b4f !important;
}

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0d151c,
            #0b1117
        );
    border-right: 1px solid #22303c;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
}

hr {
    border-color: #24323e !important;
}

.small {
    color: #718191;
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


def get_category(risk):

    if risk < 25:
        return "Low"

    if risk < 50:
        return "Moderate"

    if risk < 75:
        return "High"

    return "Critical"


def calculate_risk(lst, ndvi, built, population):

    heat = normalize(lst, 30, 45)

    vegetation_deficit = 100 - ndvi * 100

    return max(
        0,
        min(
            100,
            0.45 * heat +
            0.25 * built +
            0.20 * vegetation_deficit +
            0.10 * population
        )
    )


def get_contributions(lst, ndvi, built, population):

    heat = normalize(lst, 30, 45)

    vegetation_deficit = 100 - ndvi * 100

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

        return response.json()["current"]

    except:

        return None


# =========================================================
# OSM ROADS
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

    try:

        response = requests.post(
            "https://overpass-api.de/api/interpreter",
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


def road_color(highway):

    if highway in [
        "motorway",
        "trunk",
        "primary"
    ]:
        return "#ff654d"

    if highway in [
        "secondary",
        "tertiary"
    ]:
        return "#f4ad52"

    return "#71808f"


# =========================================================
# THERMAL PLUME
# =========================================================

def create_heat_plume(lat, lon, risk):

    points = []

    radius = 0.018

    grid = 18

    for i in range(-grid, grid + 1):

        for j in range(-grid, grid + 1):

            dx = i / grid
            dy = j / grid

            distance = math.sqrt(
                dx * dx + dy * dy
            )

            intensity = math.exp(
                -(distance ** 2) * 3
            )

            intensity *= risk / 100

            if intensity > 0.025:

                points.append([
                    lat + dx * radius,
                    lon + dy * radius,
                    intensity
                ])

    return points


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
# ANIMATED INTERVENTION MAP
# =========================================================

def build_intervention_map(
    lat,
    lon,
    before,
    after,
    roads,
    locality
):

    m = folium.Map(
        location=[lat, lon],
        zoom_start=13,
        tiles="OpenStreetMap"
    )

    # -----------------------------------------------------
    # CREATE MANY THERMAL ZONES
    # -----------------------------------------------------

    zones = []

    for ring in range(1, 7):

        radius = ring * 150

        for angle in range(0, 360, 45):

            radians = math.radians(angle)

            zone_lat = (
                lat +
                math.cos(radians) *
                radius /
                111000
            )

            zone_lon = (
                lon +
                math.sin(radians) *
                radius /
                (111000 * math.cos(math.radians(lat)))
            )

            circle = folium.Circle(
                location=[
                    zone_lat,
                    zone_lon
                ],
                radius=radius * 0.75,
                color="#ff2020",
                fill=True,
                fill_color="#ff2020",
                fill_opacity=0.12,
                weight=0
            )

            circle.add_to(m)

            zones.append(
                circle.get_name()
            )

    # -----------------------------------------------------
    # CENTRE
    # -----------------------------------------------------

    centre = folium.Circle(
        location=[lat, lon],
        radius=650,
        color="#ff2020",
        fill=True,
        fill_color="#ff2020",
        fill_opacity=0.20,
        weight=2
    )

    centre.add_to(m)

    zones.append(
        centre.get_name()
    )

    # -----------------------------------------------------
    # ROADS
    # -----------------------------------------------------

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
                p["lat"],
                p["lon"]
            ]
            for p in geometry
        ]

        folium.PolyLine(
            coordinates,
            color=road_color(highway),
            weight=3,
            opacity=0.60,
            tooltip=name
        ).add_to(m)

    # -----------------------------------------------------
    # MARKER
    # -----------------------------------------------------

    folium.Marker(
        [lat, lon],
        tooltip=locality,
        popup=(
            f"{locality}<br>"
            f"Before: {before:.0f}/100<br>"
            f"After: {after:.0f}/100"
        )
    ).add_to(m)

    # -----------------------------------------------------
    # JAVASCRIPT ANIMATION
    # -----------------------------------------------------

    zone_names = ",".join(
        f"window['{z}']"
        for z in zones
    )

    script = f"""

    <script>

    const heatZones = [
        {zone_names}
    ];

    const beforeRisk = {before};
    const afterRisk = {after};

    let animationStart = null;
    const duration = 1800;

    function interpolate(a, b, t) {{
        return a + (b - a) * t;
    }}

    function colorForRisk(risk) {{

        if (risk >= 75) {{

            return "#ff1f1f";

        }} else if (risk >= 50) {{

            return "#ff9f1c";

        }} else if (risk >= 25) {{

            return "#ffe14a";

        }} else {{

            return "#37d66b";

        }}
    }}

    function opacityForRisk(risk) {{

        return 0.10 + (risk / 100) * 0.22;

    }}

    function animate(timestamp) {{

        if (!animationStart) {{
            animationStart = timestamp;
        }}

        let progress =
            (timestamp - animationStart) / duration;

        if (progress > 1) {{
            progress = 1;
        }}

        const smooth =
            progress < 0.5
            ? 2 * progress * progress
            : 1 - Math.pow(-2 * progress + 2, 2) / 2;

        const currentRisk =
            interpolate(
                beforeRisk,
                afterRisk,
                smooth
            );

        const color =
            colorForRisk(currentRisk);

        const opacity =
            opacityForRisk(currentRisk);

        heatZones.forEach(function(zone) {{

            zone.setStyle({{
                color: color,
                fillColor: color,
                fillOpacity: opacity
            }});

        }});

        if (progress < 1) {{

            requestAnimationFrame(animate);

        }} else {{

            setTimeout(function() {{

                animationStart = null;
                requestAnimationFrame(animate);

            }}, 700);

        }}
    }}

    requestAnimationFrame(animate);

    </script>
    """

    m.get_root().html.add_child(
        folium.Element(script)
    )

    return m


# =========================================================
# COST MODEL
# =========================================================

def calculate_costs(
    trees,
    roof_area,
    shade_structures
):

    tree_planting = trees * 650
    tree_first_year = trees * 300
    tree_maintenance = trees * 250

    roof_installation = roof_area * 300
    roof_maintenance = roof_area * 30

    shade_installation = shade_structures * 25000
    shade_maintenance = shade_structures * 2500

    implementation = (
        tree_planting +
        tree_first_year +
        roof_installation +
        shade_installation
    )

    annual_maintenance = (
        tree_maintenance +
        roof_maintenance +
        shade_maintenance
    )

    five_year_maintenance = (
        annual_maintenance * 5
    )

    return {
        "implementation": implementation,
        "annual_maintenance": annual_maintenance,
        "five_year_maintenance": five_year_maintenance,
        "five_year_total":
            implementation +
            five_year_maintenance,
        "tree_planting": tree_planting,
        "tree_first_year": tree_first_year,
        "tree_maintenance": tree_maintenance,
        "roof_installation": roof_installation,
        "roof_maintenance": roof_maintenance,
        "shade_installation": shade_installation,
        "shade_maintenance": shade_maintenance
    }


# =========================================================
# HEADER
# =========================================================

st.title("🌍 HeatScape")

st.write(
    "### Urban Heat Reduction Planner"
)

st.write(
    "Locality → Live conditions → Thermal plume → "
    "Road-level planning → Intervention → Lifecycle cost"
)

st.divider()


# =========================================================
# LOCALITY
# =========================================================

st.sidebar.title("📍 Choose Locality")

selected = st.sidebar.selectbox(
    "Chennai locality",
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
# CURRENT RISK
# =========================================================

base_heat = normalize(
    data["lst"],
    30,
    45
)

live_heat = normalize(
    live_temperature,
    25,
    45
)

combined_heat = (
    0.65 * base_heat +
    0.35 * live_heat
)

vegetation_deficit = (
    100 -
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


# =========================================================
# METRICS
# =========================================================

st.subheader(
    f"📍 {selected}"
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "🔥 Heat Risk",
        f"{risk:.0f}/100"
    )

with c2:
    st.metric(
        "🌡️ Live Temperature",
        f"{live_temperature:.1f} °C"
    )

with c3:
    st.metric(
        "🥵 Feels Like",
        f"{live_apparent:.1f} °C"
    )

with c4:
    st.metric(
        "💧 Humidity",
        f"{live_humidity:.0f}%"
    )


st.markdown(
    f"""
    <div class="livebox">

    🟢 <b>LIVE ENVIRONMENTAL CONDITIONS</b><br><br>

    Temperature: {live_temperature:.1f} °C<br>
    Apparent temperature: {live_apparent:.1f} °C<br>
    Humidity: {live_humidity:.0f}%<br>
    Wind: {live_wind:.1f} km/h

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MAIN MAP
# =========================================================

st.divider()

st.subheader(
    "🔥 Local Thermal Plume + Road Network"
)

st.write(
    "HeatScape spatializes the selected locality's risk and overlays "
    "the surrounding OpenStreetMap road network."
)

roads = get_osm_roads(
    lat,
    lon
)

m = folium.Map(
    location=[lat, lon],
    zoom_start=13,
    tiles="OpenStreetMap"
)

plume = create_heat_plume(
    lat,
    lon,
    risk
)

HeatMap(
    plume,
    radius=30,
    blur=28,
    max_zoom=15,
    min_opacity=0.25
).add_to(m)


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
            p["lat"],
            p["lon"]
        ]
        for p in geometry
    ]

    folium.PolyLine(
        coordinates,
        color=road_color(highway),
        weight=3,
        opacity=0.65,
        tooltip=name
    ).add_to(m)


folium.Marker(
    [lat, lon],
    tooltip=selected
).add_to(m)


st_folium(
    m,
    width=1200,
    height=600
)


# =========================================================
# HEAT FINGERPRINT
# =========================================================

st.divider()

st.subheader(
    "🧬 Heat Fingerprint"
)

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
        f"**{name} — {value:.1f} risk points**"
    )

    st.progress(
        min(100, int(value))
    )


# =========================================================
# RECOMMENDATION
# =========================================================

recommendation, reason = get_recommendation(
    data["lst"],
    data["ndvi"],
    data["built"],
    data["population"]
)

st.divider()

st.subheader(
    "💡 Recommended First Intervention"
)

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
# SIMULATOR
# =========================================================

st.divider()

st.subheader(
    "🔬 Intervention Simulator"
)

st.write(
    "Change the intervention scale and watch the modeled "
    "risk transform from 🔴 red → 🟠 orange → 🟡 yellow → 🟢 green."
)

c1, c2, c3 = st.columns(3)

with c1:

    trees = st.slider(
        "🌳 Trees planted",
        0,
        2000,
        500,
        100
    )

with c2:

    roof_area = st.slider(
        "🏠 Cool roof area",
        0,
        50000,
        10000,
        5000
    )

with c3:

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

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "🔴 BEFORE",
        f"{risk:.0f}/100"
    )

with c2:

    st.metric(
        "🟢 AFTER",
        f"{new_risk:.0f}/100"
    )

with c3:

    st.metric(
        "📉 REDUCTION",
        f"{reduction:.1f} points"
    )


# =========================================================
# ANIMATED MAP
# =========================================================

st.subheader(
    "🗺️ Live Intervention Simulation"
)

st.write(
    "The thermal field continuously transitions toward the "
    "simulated post-intervention state."
)

impact_map = build_intervention_map(
    lat,
    lon,
    risk,
    new_risk,
    roads,
    selected
)

# IMPORTANT:
# Use direct HTML rendering here instead of st_folium.
# This allows the browser animation to actually run.

components.html(
    impact_map.get_root().render(),
    height=620,
    scrolling=False
)

st.caption(
    "Animation represents a modeled change in Heat Risk. "
    "It is not a measured satellite temperature change."
)


# =========================================================
# COST
# =========================================================

st.divider()

st.subheader(
    "💰 Lifecycle Cost Estimation"
)

st.write(
    "HeatScape estimates not only installation, but also "
    "the recurring cost required to keep the intervention working."
)

costs = calculate_costs(
    trees,
    roof_area,
    shade_structures
)

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Initial Implementation",
        f"₹{costs['implementation']:,.0f}"
    )

with c2:

    st.metric(
        "Annual Maintenance",
        f"₹{costs['annual_maintenance']:,.0f}"
    )

with c3:

    st.metric(
        "5-Year Lifecycle Cost",
        f"₹{costs['five_year_total']:,.0f}"
    )


st.markdown(
    f"""
    <div class="costbox">

    ### 🌳 Trees

    Planting + establishment:
    **₹{costs['tree_planting'] + costs['tree_first_year']:,.0f}**

    Annual watering, fertilizer, pruning and care:
    **₹{costs['tree_maintenance']:,.0f} / year**

    ### 🏠 Cool Roofs

    Installation:
    **₹{costs['roof_installation']:,.0f}**

    Annual upkeep:
    **₹{costs['roof_maintenance']:,.0f} / year**

    ### 🚶 Shade Structures

    Installation:
    **₹{costs['shade_installation']:,.0f}**

    Annual maintenance:
    **₹{costs['shade_maintenance']:,.0f} / year**

    ---

    ### 5-YEAR VIEW

    Initial implementation:
    **₹{costs['implementation']:,.0f}**

    5-year maintenance:
    **₹{costs['five_year_maintenance']:,.0f}**

    ## Total:
    **₹{costs['five_year_total']:,.0f}**

    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Planning estimates only. Replace unit rates with approved "
    "GCC/PWD schedule or tender rates before real-world deployment."
)


# =========================================================
# METHODOLOGY
# =========================================================

st.divider()

with st.expander(
    "📊 Data & Methodology"
):

    st.write("""
    ### Live Data

    • Open-Meteo → current atmospheric conditions

    • OpenStreetMap → road network and road classification

    ### Heat Model

    Heat Risk =
    0.45 × Heat +
    0.25 × Built-up +
    0.20 × Vegetation Deficit +
    0.10 × Population Exposure

    ### Planned Satellite Layer

    • Landsat 8/9 → Surface Temperature

    • Sentinel-2 → NDVI

    • Copernicus land cover → Built-up / land cover

    • WorldPop → Population exposure

    ### Simulation

    The intervention simulator estimates a change in the
    Heat Risk Index based on the scale of the intervention.

    The animated thermal field visualizes this modeled change.
    """)

st.caption(
    f"HeatScape • {datetime.now().strftime('%d %b %Y, %H:%M')}"
)
