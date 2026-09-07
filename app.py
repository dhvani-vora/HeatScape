import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import requests
import math
import json
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
# CSS
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

.info {
    background: #151b23;
    border: 1px solid #29313c;
    padding: 18px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# CHENNAI LOCALITIES
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
# RISK FUNCTIONS
# =========================================================

def normalize(value, minimum, maximum):

    if maximum == minimum:
        return 0

    result = (
        (value - minimum)
        / (maximum - minimum)
    ) * 100

    return max(
        0,
        min(100, result)
    )


def calculate_risk(
    lst,
    ndvi,
    built,
    population
):

    heat = normalize(
        lst,
        30,
        45
    )

    vegetation_deficit = (
        100 - ndvi * 100
    )

    risk = (
        0.45 * heat +
        0.25 * built +
        0.20 * vegetation_deficit +
        0.10 * population
    )

    return max(
        0,
        min(100, risk)
    )


def get_category(risk):

    if risk < 25:
        return "Low"

    if risk < 50:
        return "Moderate"

    if risk < 75:
        return "High"

    return "Critical"


def get_contributions(
    lst,
    ndvi,
    built,
    population
):

    heat = normalize(
        lst,
        30,
        45
    )

    vegetation_deficit = (
        100 - ndvi * 100
    )

    return {

        "Surface Heat":
        0.45 * heat,

        "Built-up Area":
        0.25 * built,

        "Vegetation Deficit":
        0.20 * vegetation_deficit,

        "Population Exposure":
        0.10 * population
    }


# =========================================================
# RECOMMENDATION
# =========================================================

def get_recommendation(
    lst,
    ndvi,
    built,
    population
):

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

            "Vegetation deficit is the dominant "
            "contributor. Increase tree cover "
            "along roads and connect existing "
            "green spaces."
        )

    if dominant == "Built-up Area":

        return (
            "🏠 Cool Roofs + Shade",

            "Dense built-up surfaces are absorbing "
            "significant heat. Prioritize reflective "
            "roofs and shaded public areas."
        )

    if dominant == "Population Exposure":

        return (
            "🚶 Shaded Public Corridor",

            "High population exposure makes "
            "pedestrian cooling infrastructure "
            "the priority."
        )

    return (
        "🌳 Green Corridor + Cool Roofs",

        "Surface heat is the dominant contributor. "
        "Combine vegetation with reflective "
        "built surfaces."
    )


# =========================================================
# LIVE WEATHER
# =========================================================

@st.cache_data(ttl=600)
def get_live_weather(
    lat,
    lon
):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&current="
        "temperature_2m,"
        "relative_humidity_2m,"
        "apparent_temperature,"
        "wind_speed_10m"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return data["current"]

    except Exception:

        return None


# =========================================================
# OPENSTREETMAP
# =========================================================

@st.cache_data(ttl=3600)
def get_osm_roads(
    lat,
    lon
):

    query = f"""
    [out:json][timeout:25];

    (
      way["highway"]
      (around:1800,{lat},{lon});
    );

    out geom;
    """

    url = (
        "https://overpass-api.de/api/interpreter"
    )

    try:

        response = requests.post(
            url,
            data=query,
            headers={
                "User-Agent":
                "HeatScape/1.0"
            },
            timeout=30
        )

        response.raise_for_status()

        return response.json().get(
            "elements",
            []
        )

    except Exception:

        return []


# =========================================================
# ROAD COLORS
# =========================================================

def road_color(
    highway
):

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
        return "#ff4d4d"

    if highway in medium:
        return "#ffad42"

    return "#66717f"


# =========================================================
# THERMAL PLUME DATA
# =========================================================

def create_heat_plume(
    lat,
    lon,
    risk
):

    points = []

    grid = 18

    radius = 0.020

    for i in range(
        -grid,
        grid + 1
    ):

        for j in range(
            -grid,
            grid + 1
        ):

            dx = i / grid
            dy = j / grid

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            intensity = math.exp(
                -(distance ** 2) * 3
            )

            intensity *= (
                risk / 100
            )

            if intensity > 0.025:

                points.append(
                    [
                        lat + dx * radius,
                        lon + dy * radius,
                        intensity
                    ]
                )

    return points


# =========================================================
# ANIMATED INTERVENTION PLUME
# =========================================================

def add_animated_plume(
    map_object,
    lat,
    lon,
    before,
    after
):

    map_name = map_object.get_name()

    # Create spatial cells in Python
    cells = []

    grid = 13

    radius = 0.018

    for i in range(
        -grid,
        grid + 1
    ):

        for j in range(
            -grid,
            grid + 1
        ):

            dx = i / grid
            dy = j / grid

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            intensity = math.exp(
                -(distance ** 2) * 2.8
            )

            if intensity < 0.08:
                continue

            local_before = (
                before * intensity
            )

            local_after = (
                after * intensity
            )

            cells.append(
                {
                    "lat":
                    lat + dx * radius,

                    "lon":
                    lon + dy * radius,

                    "before":
                    local_before,

                    "after":
                    local_after,

                    "intensity":
                    intensity
                }
            )

    cells_json = json.dumps(
        cells
    )

    # IMPORTANT:
    # We use a normal string instead of a Python f-string.
    # Therefore JavaScript { } cannot break Python.

    script = """
    <script>

    (function() {

        const mapObject = MAP_NAME;

        const cells = CELLS_DATA;

        const duration = 1800;

        let startTime = null;

        let heatLayers = [];

        function getColor(risk) {

            if (risk >= 75) {

                return "#ff2020";

            }

            if (risk >= 50) {

                return "#ff8c00";

            }

            if (risk >= 25) {

                return "#ffd21f";

            }

            return "#32d74b";
        }


        function getOpacity(risk) {

            let value =
                0.06 + (risk / 100) * 0.42;

            return Math.max(
                0.06,
                Math.min(
                    0.48,
                    value
                )
            );
        }


        function makeLayers() {

            cells.forEach(
                function(cell) {

                    const circle =
                        L.circle(
                            [
                                cell.lat,
                                cell.lon
                            ],
                            {
                                radius: 115,
                                stroke: false,
                                fill: true,
                                fillColor:
                                    getColor(
                                        cell.before
                                    ),
                                fillOpacity:
                                    getOpacity(
                                        cell.before
                                    )
                            }
                        );

                    circle.addTo(
                        mapObject
                    );

                    heatLayers.push(
                        {
                            circle:
                                circle,

                            before:
                                cell.before,

                            after:
                                cell.after
                        }
                    );

                }
            );

        }


        function animate(timestamp) {

            if (
                startTime === null
            ) {

                startTime =
                    timestamp;

            }


            let progress =
                (
                    timestamp -
                    startTime
                ) / duration;


            if (progress > 1) {

                progress = 1;

            }


            heatLayers.forEach(
                function(layer) {

                    const current =
                        layer.before +
                        (
                            layer.after -
                            layer.before
                        ) * progress;


                    layer.circle.setStyle(
                        {
                            fillColor:
                                getColor(
                                    current
                                ),

                            fillOpacity:
                                getOpacity(
                                    current
                                )
                        }
                    );

                }
            );


            if (
                progress < 1
            ) {

                requestAnimationFrame(
                    animate
                );

            }

            else {

                startTime = null;

                setTimeout(
                    function() {

                        requestAnimationFrame(
                            animate
                        );

                    },
                    700
                );

            }

        }


        makeLayers();

        requestAnimationFrame(
            animate
        );

    })();

    </script>
    """

    script = script.replace(
        "MAP_NAME",
        map_name
    )

    script = script.replace(
        "CELLS_DATA",
        cells_json
    )

    map_object.get_root().html.add_child(
        folium.Element(
            script
        )
    )


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
        (trees / 2000) * 15,
        15
    )

    roof_effect = min(
        (roof_area / 50000) * 12,
        12
    )

    shade_effect = min(
        (shade_structures / 100) * 7,
        7
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
# COST MODEL
# =========================================================

def calculate_costs(
    trees,
    roof_area,
    shade_structures
):

    # -----------------------------------------
    # TREES
    # -----------------------------------------

    tree_planting = (
        trees * 650
    )

    tree_first_year = (
        trees * 300
    )

    tree_maintenance = (
        trees * 250
    )


    # -----------------------------------------
    # COOL ROOF
    # -----------------------------------------

    roof_installation = (
        roof_area * 300
    )

    roof_maintenance = (
        roof_area * 30
    )


    # -----------------------------------------
    # SHADE STRUCTURES
    # -----------------------------------------

    shade_installation = (
        shade_structures * 25000
    )

    shade_maintenance = (
        shade_structures * 2500
    )


    # -----------------------------------------
    # TOTALS
    # -----------------------------------------

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

    five_year_total = (
        implementation +
        five_year_maintenance
    )


    return {

        "tree_planting":
        tree_planting,

        "tree_first_year":
        tree_first_year,

        "tree_maintenance":
        tree_maintenance,

        "roof_installation":
        roof_installation,

        "roof_maintenance":
        roof_maintenance,

        "shade_installation":
        shade_installation,

        "shade_maintenance":
        shade_maintenance,

        "implementation":
        implementation,

        "annual_maintenance":
        annual_maintenance,

        "five_year_maintenance":
        five_year_maintenance,

        "five_year_total":
        five_year_total
    }


# =========================================================
# HEADER
# =========================================================

st.title(
    "🌍 HeatScape"
)

st.write(
    "### Urban Heat Reduction Planner"
)

st.write(
    "Locality → Live conditions → "
    "Thermal plume → Road-level planning → "
    "Intervention → Lifecycle cost"
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title(
    "📍 Locality"
)

selected = st.sidebar.selectbox(
    "Choose a Chennai locality",
    list(localities.keys())
)

data = localities[
    selected
]

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

    live_temperature = (
        weather["temperature_2m"]
    )

    live_humidity = (
        weather["relative_humidity_2m"]
    )

    live_apparent = (
        weather["apparent_temperature"]
    )

    live_wind = (
        weather["wind_speed_10m"]
    )

else:

    live_temperature = (
        data["lst"]
    )

    live_humidity = 0

    live_apparent = (
        data["lst"]
    )

    live_wind = 0


# =========================================================
# LIVE HEAT COMPONENT
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


# =========================================================
# CURRENT RISK
# =========================================================

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

category = get_category(
    risk
)


# =========================================================
# LIVE PANEL
# =========================================================

st.subheader(
    f"📍 {selected}"
)

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

    🟢 <b>LIVE ENVIRONMENTAL DATA</b>

    <br><br>

    Temperature:
    <b>{live_temperature:.1f} °C</b>

    &nbsp;&nbsp; | &nbsp;&nbsp;

    Apparent:
    <b>{live_apparent:.1f} °C</b>

    &nbsp;&nbsp; | &nbsp;&nbsp;

    Humidity:
    <b>{live_humidity:.0f}%</b>

    &nbsp;&nbsp; | &nbsp;&nbsp;

    Wind:
    <b>{live_wind:.1f} km/h</b>

    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Live atmospheric conditions are retrieved "
    "from Open-Meteo."
)

st.write(
    f"**Current Heat Risk Level: {category}**"
)

st.divider()


# =========================================================
# MAIN THERMAL MAP
# =========================================================

st.subheader(
    "🔥 Local Thermal Plume"
)

st.write(
    "HeatScape expands the hotspot into a spatial "
    "thermal field and overlays the local road network."
)


main_map = folium.Map(
    location=[
        lat,
        lon
    ],
    zoom_start=13,
    tiles="OpenStreetMap"
)


# -----------------------------------------
# Thermal plume
# -----------------------------------------

plume = create_heat_plume(
    lat,
    lon,
    risk
)

HeatMap(
    plume,
    radius=30,
    blur=25,
    max_zoom=15,
    min_opacity=0.25
).add_to(
    main_map
)


# -----------------------------------------
# Roads
# -----------------------------------------

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
        color=road_color(
            highway
        ),
        weight=(
            4
            if highway in [
                "motorway",
                "trunk",
                "primary"
            ]
            else 2
        ),
        opacity=0.75,
        tooltip=(
            f"{name} — {highway}"
        )
    ).add_to(
        road_layer
    )


road_layer.add_to(
    main_map
)


# -----------------------------------------
# Locality marker
# -----------------------------------------

folium.Marker(
    [
        lat,
        lon
    ],
    popup=(
        f"<b>{selected}</b>"
        f"<br>Risk: {risk:.0f}/100"
    ),
    tooltip=selected,
    icon=folium.Icon(
        color="red",
        icon="fire"
    )
).add_to(
    main_map
)


folium.LayerControl().add_to(
    main_map
)


# -----------------------------------------
# DISPLAY
# -----------------------------------------

st_folium(
    main_map,
    width=1200,
    height=600,
    returned_objects=[],
    key=f"main_map_{selected}"
)


st.caption(
    "© OpenStreetMap contributors"
)


# =========================================================
# HEAT FINGERPRINT
# =========================================================

st.divider()

st.subheader(
    "🧬 Heat Fingerprint"
)

st.write(
    "What is actually driving the heat risk here?"
)

contributions = get_contributions(
    data["lst"],
    data["ndvi"],
    data["built"],
    data["population"]
)


sorted_contributions = sorted(
    contributions.items(),
    key=lambda x: x[1],
    reverse=True
)


for name, value in sorted_contributions:

    st.write(
        f"**{name} — {value:.1f} risk points**"
    )

    st.progress(
        min(
            100,
            int(value)
        )
    )


# =========================================================
# RECOMMENDATION
# =========================================================

st.divider()

recommendation, reason = (
    get_recommendation(
        data["lst"],
        data["ndvi"],
        data["built"],
        data["population"]
    )
)


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

st.markdown(
    """
    **Change the intervention → watch the locality respond.**

    The model recalculates the Heat Risk Index and
    continuously transitions the thermal field:

    🔴 Critical → 🟠 High → 🟡 Moderate → 🟢 Lower Risk
    """
)


# =========================================================
# SLIDERS
# =========================================================

col1, col2, col3 = st.columns(3)


with col1:

    trees = st.slider(
        "🌳 Trees planted",
        min_value=0,
        max_value=2000,
        value=500,
        step=100,
        key="trees_slider"
    )


with col2:

    roof_area = st.slider(
        "🏠 Cool roof area (m²)",
        min_value=0,
        max_value=50000,
        value=10000,
        step=5000,
        key="roof_slider"
    )


with col3:

    shade_structures = st.slider(
        "🚶 Shade structures",
        min_value=0,
        max_value=100,
        value=10,
        step=5,
        key="shade_slider"
    )


# =========================================================
# SIMULATED RISK
# =========================================================

new_risk = simulate_risk(
    risk,
    trees,
    roof_area,
    shade_structures
)

reduction = (
    risk -
    new_risk
)


percentage_reduction = (
    reduction / risk * 100
    if risk > 0
    else 0
)


# =========================================================
# BEFORE / AFTER
# =========================================================

st.markdown(
    "### 📉 Intervention Result"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🔴 BEFORE",
        f"{risk:.0f}/100"
    )


with col2:

    st.metric(
        "🟢 AFTER",
        f"{new_risk:.0f}/100",
        delta=f"-{reduction:.1f}"
    )


with col3:

    st.metric(
        "📉 IMPROVEMENT",
        f"{percentage_reduction:.1f}%"
    )


# =========================================================
# INTERVENTION MAP
# =========================================================

st.subheader(
    "🗺️ Intervention Impact Map"
)

st.write(
    "The thermal field below continuously changes "
    "from the current risk toward the simulated risk."
)


impact_map = folium.Map(
    location=[
        lat,
        lon
    ],
    zoom_start=13,
    tiles="OpenStreetMap"
)


# -----------------------------------------
# Animated plume
# -----------------------------------------

add_animated_plume(
    impact_map,
    lat,
    lon,
    risk,
    new_risk
)


# -----------------------------------------
# Roads
# -----------------------------------------

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
        color=road_color(
            highway
        ),
        weight=3,
        opacity=0.65,
        tooltip=name
    ).add_to(
        impact_map
    )


# -----------------------------------------
# Centre marker
# -----------------------------------------

folium.Marker(
    [
        lat,
        lon
    ],
    popup=(
        f"<b>{selected}</b>"
        f"<br>Before: {risk:.0f}/100"
        f"<br>After: {new_risk:.0f}/100"
        f"<br>Reduction: {reduction:.1f}"
    ),
    tooltip="Intervention impact"
).add_to(
    impact_map
)


# -----------------------------------------
# Display
# -----------------------------------------

st_folium(
    impact_map,
    width=1200,
    height=600,
    returned_objects=[],
    key=f"impact_map_{selected}"
)


st.caption(
    "🔴 Critical → 🟠 High → 🟡 Moderate → 🟢 Lower Risk"
)


# =========================================================
# COST
# =========================================================

st.divider()

st.subheader(
    "💰 Lifecycle Cost Estimation"
)

st.write(
    "HeatScape considers both implementation and "
    "the cost of keeping each intervention functional."
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


# =========================================================
# COST BREAKDOWN
# =========================================================

st.markdown(
    f"""
    <div class="costbox">

    ### 🌳 Trees

    Planting + establishment:

    **₹{(
        costs['tree_planting']
        +
        costs['tree_first_year']
    ):,.0f}**

    Annual watering, fertilizer,
    pruning and maintenance:

    **₹{costs['tree_maintenance']:,.0f} / year**

    ---

    ### 🏠 Cool Roofs

    Installation:

    **₹{costs['roof_installation']:,.0f}**

    Annual upkeep:

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

    ### 5-YEAR TOTAL

    **₹{costs['five_year_total']:,.0f}**

    </div>
    """,
    unsafe_allow_html=True
)


st.caption(
    "Planning estimates only. Replace these "
    "assumptions with approved GCC/PWD or "
    "local tender rates before real deployment."
)


# =========================================================
# BUDGET OPTIMIZER
# =========================================================

st.divider()

st.subheader(
    "💸 Budget Planner"
)

st.write(
    "Test how much intervention can be funded "
    "under a fixed public budget."
)


budget = st.number_input(
    "Available budget (₹)",
    min_value=100000,
    max_value=100000000,
    value=10000000,
    step=500000
)


if budget > 0:

    possible_trees = int(
        budget / 650
    )

    possible_roofs = int(
        budget / 300
    )

    possible_shade = int(
        budget / 25000
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Possible trees",
            f"{possible_trees:,}"
        )


    with col2:

        st.metric(
            "Cool roof area",
            f"{possible_roofs:,} m²"
        )


    with col3:

        st.metric(
            "Shade structures",
            f"{possible_shade:,}"
        )


# =========================================================
# METHODOLOGY
# =========================================================

st.divider()

with st.expander(
    "📊 Data & Methodology"
):

    st.write(
        """
        ### Heat Risk Formula

        Heat Risk =

        0.45 × Surface Heat +

        0.25 × Built-up +

        0.20 × Vegetation Deficit +

        0.10 × Population Exposure

        ---

        ### Current live data

        • Open-Meteo → current atmospheric conditions

        • OpenStreetMap → roads and road classification

        ---

        ### Planned satellite layer

        • Landsat 8/9 → Surface Temperature

        • Sentinel-2 → NDVI

        • Copernicus land cover → Built-up / land cover

        • WorldPop → Population exposure

        ---

        ### Important

        The thermal plume currently visualizes
        the HeatScape risk model spatially.

        It is not claiming that every pixel is
        a directly measured satellite temperature.

        The next version can replace the modeled
        plume with satellite-derived LST.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "HeatScape • Data-driven urban heat reduction planning"
)

st.caption(
    "Interface refresh: "
    +
    datetime.now().strftime(
        "%d %b %Y • %H:%M:%S"
    )
)
