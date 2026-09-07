import streamlit as st
import streamlit.components.v1 as components
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import requests
import math
import json


# =========================================================
# PAGE
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

.stApp {
    background: #080c11;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: white;
}

p, label {
    color: #c3cad3;
}

.recommendation {
    background: #102218;
    border: 1px solid #2e7145;
    border-radius: 15px;
    padding: 20px;
}

.livebox {
    background: #101a24;
    border: 1px solid #24455e;
    border-radius: 15px;
    padding: 18px;
}

.costbox {
    background: #121820;
    border: 1px solid #303a47;
    border-radius: 15px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# CHENNAI LOCALITIES
# =========================================================

LOCALITIES = {

    "Washermanpet": {
        "lat": 13.1150,
        "lon": 80.2800,
        "lst": 41.1,
        "ndvi": 0.15,
        "built": 87,
        "population": 91
    },

    "Royapuram": {
        "lat": 13.1167,
        "lon": 80.2947,
        "lst": 41.0,
        "ndvi": 0.16,
        "built": 86,
        "population": 89
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
    },

    "Anna Nagar": {
        "lat": 13.0850,
        "lon": 80.2101,
        "lst": 39.7,
        "ndvi": 0.25,
        "built": 82,
        "population": 78
    },

    "Nungambakkam": {
        "lat": 13.0569,
        "lon": 80.2425,
        "lst": 40.0,
        "ndvi": 0.23,
        "built": 84,
        "population": 82
    },

    "T Nagar": {
        "lat": 13.0418,
        "lon": 80.2341,
        "lst": 40.4,
        "ndvi": 0.20,
        "built": 88,
        "population": 86
    },

    "Mylapore": {
        "lat": 13.0339,
        "lon": 80.2676,
        "lst": 39.2,
        "ndvi": 0.29,
        "built": 80,
        "population": 83
    },

    "Guindy": {
        "lat": 13.0067,
        "lon": 80.2206,
        "lst": 39.6,
        "ndvi": 0.31,
        "built": 75,
        "population": 75
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
    }
}


# =========================================================
# RISK
# =========================================================

def normalize(value, minimum, maximum):

    if maximum == minimum:
        return 0

    value = (
        (value - minimum)
        / (maximum - minimum)
    ) * 100

    return max(0, min(100, value))


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

    return max(
        0,
        min(
            100,
            (
                0.45 * heat
                + 0.25 * built
                + 0.20 * vegetation_deficit
                + 0.10 * population
            )
        )
    )


def risk_category(risk):

    if risk >= 75:
        return "Critical"

    if risk >= 50:
        return "High"

    if risk >= 25:
        return "Moderate"

    return "Low"


# =========================================================
# CONTRIBUTIONS
# =========================================================

def get_contributions(data):

    heat = normalize(
        data["lst"],
        30,
        45
    )

    vegetation_deficit = (
        100 - data["ndvi"] * 100
    )

    return {
        "Surface Heat": 0.45 * heat,
        "Built-up Area": 0.25 * data["built"],
        "Vegetation Deficit": 0.20 * vegetation_deficit,
        "Population Exposure": 0.10 * data["population"]
    }


# =========================================================
# RECOMMENDATION
# =========================================================

def get_recommendation(data):

    contributions = get_contributions(data)

    dominant = max(
        contributions,
        key=contributions.get
    )

    if dominant == "Vegetation Deficit":

        return (
            "🌳 Tree Planting / Green Corridor",
            "Vegetation deficit is the dominant heat-risk contributor."
        )

    if dominant == "Built-up Area":

        return (
            "🏠 Cool Roofs + Shade Structures",
            "Dense built-up surfaces are the dominant contributor."
        )

    if dominant == "Population Exposure":

        return (
            "🚶 Shaded Public Corridor",
            "High population exposure makes public cooling infrastructure the priority."
        )

    return (
        "🌳 Green Corridor + Cool Roofs",
        "Surface heat is the dominant contributor."
    )


# =========================================================
# LIVE WEATHER
# =========================================================

@st.cache_data(ttl=600)
def get_weather(lat, lon):

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

        return response.json()["current"]

    except Exception:

        return None


# =========================================================
# OPENSTREETMAP ROADS
# =========================================================

@st.cache_data(ttl=3600)
def get_roads(lat, lon):

    query = f"""
    [out:json][timeout:25];

    way["highway"]
    (around:1800,{lat},{lon});

    out geom;
    """

    try:

        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data=query,
            headers={
                "User-Agent": "HeatScape"
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


def road_color(highway):

    if highway in [
        "motorway",
        "trunk",
        "primary"
    ]:
        return "#ff4b4b"

    if highway in [
        "secondary",
        "tertiary"
    ]:
        return "#ffae42"

    return "#687383"


# =========================================================
# THERMAL PLUME FOR MAIN MAP
# =========================================================

def thermal_points(
    lat,
    lon,
    risk
):

    points = []

    grid = 20

    for i in range(
        -grid,
        grid + 1
    ):

        for j in range(
            -grid,
            grid + 1
        ):

            x = i / grid
            y = j / grid

            distance = math.sqrt(
                x * x + y * y
            )

            intensity = math.exp(
                -(distance ** 2) * 3
            )

            if intensity > 0.03:

                points.append(
                    [
                        lat + x * 0.022,
                        lon + y * 0.022,
                        intensity * risk / 100
                    ]
                )

    return points


# =========================================================
# INTERVENTION SIMULATION
# =========================================================

def simulate_intervention(
    risk,
    trees,
    roof_area,
    shade
):

    tree_effect = (
        trees / 2000
    ) * 18

    roof_effect = (
        roof_area / 50000
    ) * 14

    shade_effect = (
        shade / 100
    ) * 8

    reduction = (
        tree_effect
        + roof_effect
        + shade_effect
    )

    reduction = min(
        reduction,
        40
    )

    new_risk = max(
        0,
        risk - reduction
    )

    return new_risk


# =========================================================
# COST
# =========================================================

def calculate_cost(
    trees,
    roof_area,
    shade
):

    tree_install = (
        trees * 650
    )

    tree_first_year = (
        trees * 300
    )

    tree_maintenance = (
        trees * 250
    )

    roof_install = (
        roof_area * 300
    )

    roof_maintenance = (
        roof_area * 30
    )

    shade_install = (
        shade * 25000
    )

    shade_maintenance = (
        shade * 2500
    )

    initial = (
        tree_install
        + tree_first_year
        + roof_install
        + shade_install
    )

    annual_maintenance = (
        tree_maintenance
        + roof_maintenance
        + shade_maintenance
    )

    five_year_total = (
        initial
        + annual_maintenance * 5
    )

    return {
        "initial": initial,
        "maintenance": annual_maintenance,
        "five_year": five_year_total,
        "tree_install": tree_install,
        "tree_maintenance": tree_maintenance,
        "roof_install": roof_install,
        "roof_maintenance": roof_maintenance,
        "shade_install": shade_install,
        "shade_maintenance": shade_maintenance
    }


# =========================================================
# INTERVENTION MAP
#
# IMPORTANT:
# This is NOT Folium.
# It is a completely independent Leaflet map.
# Therefore the animation is controlled entirely
# by browser JavaScript.
# =========================================================

def intervention_map_html(
    lat,
    lon,
    before,
    after,
    roads
):

    # -----------------------------------------------------
    # Prepare roads
    # -----------------------------------------------------

    road_data = []

    for road in roads:

        geometry = road.get(
            "geometry",
            []
        )

        if len(geometry) < 2:
            continue

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

        coords = []

        for point in geometry:

            coords.append(
                [
                    point["lat"],
                    point["lon"]
                ]
            )

        road_data.append(
            {
                "coords": coords,
                "highway": highway,
                "name": name
            }
        )

    road_json = json.dumps(
        road_data
    )

    # -----------------------------------------------------
    # HTML
    # -----------------------------------------------------

    html = """
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<link
rel="stylesheet"
href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
/>

<style>

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: #080c11;
    overflow: hidden;
}

#map {
    width: 100%;
    height: 100%;
}

#panel {

    position: absolute;

    top: 15px;
    left: 15px;

    z-index: 9999;

    background: rgba(10, 15, 20, 0.92);

    color: white;

    padding: 14px 18px;

    border-radius: 12px;

    font-family:
        Arial,
        sans-serif;

    min-width: 180px;

    box-shadow:
        0 4px 20px
        rgba(0,0,0,0.4);
}

#status {

    font-size: 22px;

    font-weight: bold;

    margin-bottom: 5px;
}

#riskText {

    font-size: 15px;

    color: #cbd5df;
}

.legend {

    position: absolute;

    bottom: 18px;
    right: 18px;

    z-index: 9999;

    background: rgba(10,15,20,0.92);

    color: white;

    padding: 12px;

    border-radius: 10px;

    font-family: Arial;

    font-size: 13px;
}

.legendRow {

    margin: 4px 0;
}

.dot {

    display: inline-block;

    width: 12px;
    height: 12px;

    border-radius: 50%;

    margin-right: 6px;
}

</style>

</head>

<body>

<div id="map"></div>

<div id="panel">

    <div id="status">
        🔴 HEAT FIELD
    </div>

    <div id="riskText">
        Simulating intervention...
    </div>

</div>

<div class="legend">

    <div class="legendRow">
        <span
        class="dot"
        style="background:#ff2020">
        </span>
        Critical
    </div>

    <div class="legendRow">
        <span
        class="dot"
        style="background:#ff8c00">
        </span>
        High
    </div>

    <div class="legendRow">
        <span
        class="dot"
        style="background:#ffd21f">
        </span>
        Moderate
    </div>

    <div class="legendRow">
        <span
        class="dot"
        style="background:#32d74b">
        </span>
        Lower
    </div>

</div>


<script
src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js">
</script>


<script>

const LATITUDE =
    __LATITUDE__;

const LONGITUDE =
    __LONGITUDE__;

const BEFORE =
    __BEFORE__;

const AFTER =
    __AFTER__;

const ROADS =
    __ROADS__;


const map =
    L.map("map", {
        zoomControl: true
    }).setView(
        [
            LATITUDE,
            LONGITUDE
        ],
        13
    );


L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        maxZoom: 19,
        attribution:
            "&copy; OpenStreetMap contributors"
    }
).addTo(map);


// =====================================================
// ROAD NETWORK
// =====================================================

function roadColour(
    highway
) {

    if (
        highway === "motorway" ||
        highway === "trunk" ||
        highway === "primary"
    ) {

        return "#ff4b4b";

    }

    if (
        highway === "secondary" ||
        highway === "tertiary"
    ) {

        return "#ffae42";

    }

    return "#697586";
}


ROADS.forEach(
    function(road) {

        L.polyline(
            road.coords,
            {
                color:
                    roadColour(
                        road.highway
                    ),

                weight:
                    (
                        road.highway === "primary" ||
                        road.highway === "trunk"
                    )
                    ? 4
                    : 2,

                opacity: 0.7
            }
        )
        .bindTooltip(
            road.name
        )
        .addTo(map);

    }
);


// =====================================================
// THERMAL CELLS
// =====================================================

const cells = [];

const GRID = 18;

const LAT_RADIUS = 0.020;

const LON_RADIUS = 0.022;


for (
    let x = -GRID;
    x <= GRID;
    x++
) {

    for (
        let y = -GRID;
        y <= GRID;
        y++
    ) {

        const dx =
            x / GRID;

        const dy =
            y / GRID;

        const distance =
            Math.sqrt(
                dx * dx +
                dy * dy
            );

        const intensity =
            Math.exp(
                -(distance * distance) * 3
            );


        if (
            intensity < 0.035
        ) {

            continue;

        }


        const beforeValue =
            BEFORE * intensity;

        const afterValue =
            AFTER * intensity;


        const cell =
            L.circle(
                [
                    LATITUDE +
                    dx * LAT_RADIUS,

                    LONGITUDE +
                    dy * LON_RADIUS
                ],
                {
                    radius: 130,

                    stroke: false,

                    fill: true,

                    fillColor:
                        getColour(
                            beforeValue
                        ),

                    fillOpacity:
                        getOpacity(
                            beforeValue
                        )
                }
            );


        cell.addTo(map);


        cells.push(
            {
                layer: cell,
                before: beforeValue,
                after: afterValue
            }
        );

    }

}


// =====================================================
// COLOUR
// =====================================================

function getColour(
    risk
) {

    if (
        risk >= 75
    ) {

        return "#ff2020";

    }

    if (
        risk >= 50
    ) {

        return "#ff8c00";

    }

    if (
        risk >= 25
    ) {

        return "#ffd21f";

    }

    return "#32d74b";
}


function getOpacity(
    risk
) {

    return Math.max(
        0.05,
        Math.min(
            0.52,
            0.06 +
            risk / 100 * 0.46
        )
    );

}


// =====================================================
// INTERPOLATION
// =====================================================

function ease(
    value
) {

    return (
        value < 0.5
        ? 2 * value * value
        : 1 -
          Math.pow(
              -2 * value + 2,
              2
          ) / 2
    );

}


// =====================================================
// ANIMATION
// =====================================================

let startTime =
    null;

const duration =
    1800;


function animate(
    timestamp
) {

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


    if (
        progress > 1
    ) {

        progress = 1;

    }


    const smoothProgress =
        ease(progress);


    const currentRisk =
        BEFORE +
        (
            AFTER -
            BEFORE
        ) * smoothProgress;


    cells.forEach(
        function(cell) {

            const value =
                cell.before +
                (
                    cell.after -
                    cell.before
                ) * smoothProgress;


            cell.layer.setStyle(
                {
                    fillColor:
                        getColour(
                            value
                        ),

                    fillOpacity:
                        getOpacity(
                            value
                        )
                }
            );

        }
    );


    document
        .getElementById(
            "riskText"
        )
        .innerHTML =
            "Heat Risk: <b>" +
            currentRisk.toFixed(1) +
            "/100</b>";


    let status = "🟢 LOWER RISK";


    if (
        currentRisk >= 75
    ) {

        status =
            "🔴 CRITICAL";

    }

    else if (
        currentRisk >= 50
    ) {

        status =
            "🟠 HIGH";

    }

    else if (
        currentRisk >= 25
    ) {

        status =
            "🟡 MODERATE";

    }


    document
        .getElementById(
            "status"
        )
        .innerHTML =
            status;


    if (
        progress < 1
    ) {

        requestAnimationFrame(
            animate
        );

    }

    else {

        startTime =
            null;

        setTimeout(
            function() {

                requestAnimationFrame(
                    animate
                );

            },
            1200
        );

    }

}


requestAnimationFrame(
    animate
);


// =====================================================
// CENTRE MARKER
// =====================================================

L.circleMarker(
    [
        LATITUDE,
        LONGITUDE
    ],
    {
        radius: 7,
        color: "#ffffff",
        weight: 2,
        fillColor: "#111111",
        fillOpacity: 1
    }
)
.bindPopup(
    "<b>HeatScape intervention area</b>"
)
.addTo(map);


</script>

</body>

</html>
"""

    html = html.replace(
        "__LATITUDE__",
        str(lat)
    )

    html = html.replace(
        "__LONGITUDE__",
        str(lon)
    )

    html = html.replace(
        "__BEFORE__",
        str(before)
    )

    html = html.replace(
        "__AFTER__",
        str(after)
    )

    html = html.replace(
        "__ROADS__",
        road_json
    )

    return html


# =========================================================
# HEADER
# =========================================================

st.title(
    "🌍 HeatScape"
)

st.subheader(
    "Urban Heat Reduction Planner"
)

st.write(
    "Identify heat hotspots, understand why they occur, "
    "and simulate targeted cooling interventions."
)


# =========================================================
# LOCALITY
# =========================================================

st.sidebar.title(
    "📍 Choose Locality"
)

selected = st.sidebar.selectbox(
    "Chennai locality",
    list(LOCALITIES.keys())
)

data = LOCALITIES[
    selected
]

lat = data["lat"]
lon = data["lon"]


# =========================================================
# LIVE WEATHER
# =========================================================

weather = get_weather(
    lat,
    lon
)


if weather:

    temperature = weather[
        "temperature_2m"
    ]

    humidity = weather[
        "relative_humidity_2m"
    ]

    apparent = weather[
        "apparent_temperature"
    ]

    wind = weather[
        "wind_speed_10m"
    ]

else:

    temperature = data["lst"]
    humidity = 0
    apparent = data["lst"]
    wind = 0


# =========================================================
# RISK
# =========================================================

risk = calculate_risk(
    data["lst"],
    data["ndvi"],
    data["built"],
    data["population"]
)

category = risk_category(
    risk
)


# =========================================================
# TOP METRICS
# =========================================================

st.markdown(
    f"## 📍 {selected}"
)

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Heat Risk",
        f"{risk:.0f}/100"
    )


with c2:

    st.metric(
        "Live Temperature",
        f"{temperature:.1f} °C"
    )


with c3:

    st.metric(
        "Feels Like",
        f"{apparent:.1f} °C"
    )


with c4:

    st.metric(
        "Humidity",
        f"{humidity:.0f}%"
    )


st.markdown(
    f"""
    <div class="livebox">

    🛰️ <b>LIVE ENVIRONMENT</b><br><br>

    Temperature:
    <b>{temperature:.1f} °C</b>

    &nbsp; | &nbsp;

    Feels Like:
    <b>{apparent:.1f} °C</b>

    &nbsp; | &nbsp;

    Humidity:
    <b>{humidity:.0f}%</b>

    &nbsp; | &nbsp;

    Wind:
    <b>{wind:.1f} km/h</b>

    </div>
    """,
    unsafe_allow_html=True
)


st.caption(
    "Live atmospheric conditions: Open-Meteo"
)


# =========================================================
# ROADS
# =========================================================

roads = get_roads(
    lat,
    lon
)


# =========================================================
# MAIN MAP
# =========================================================

st.divider()

st.subheader(
    "🔥 Local Thermal Map"
)

st.write(
    "Thermal plume + road-level planning context."
)


main_map = folium.Map(
    location=[
        lat,
        lon
    ],
    zoom_start=13,
    tiles="OpenStreetMap"
)


HeatMap(
    thermal_points(
        lat,
        lon,
        risk
    ),
    radius=30,
    blur=25,
    min_opacity=0.25,
    max_zoom=15
).add_to(
    main_map
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

    if len(geometry) < 2:
        continue

    highway = tags.get(
        "highway",
        "road"
    )

    name = tags.get(
        "name",
        "Unnamed road"
    )

    coordinates = [
        [
            p["lat"],
            p["lon"]
        ]
        for p in geometry
    ]

    folium.PolyLine(
        coordinates,
        color=road_color(
            highway
        ),
        weight=3,
        opacity=0.7,
        tooltip=name
    ).add_to(
        main_map
    )


folium.Marker(
    [
        lat,
        lon
    ],
    tooltip=selected,
    popup=(
        f"<b>{selected}</b>"
        f"<br>Heat Risk: {risk:.1f}/100"
    ),
    icon=folium.Icon(
        color="red",
        icon="fire"
    )
).add_to(
    main_map
)


st_folium(
    main_map,
    width=1200,
    height=600,
    returned_objects=[],
    key=f"main_{selected}"
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
    "The system explains what is driving the risk."
)


contributions = get_contributions(
    data
)

for name, value in sorted(
    contributions.items(),
    key=lambda x: x[1],
    reverse=True
):

    st.write(
        f"**{name}: {value:.1f} risk points**"
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
        data
    )
)


st.subheader(
    "💡 Recommended Intervention"
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
    "Move the controls. The map below will visibly "
    "transform from the current heat state to the "
    "simulated post-intervention state."
)


# =========================================================
# SIMULATION CONTROLS
# =========================================================

s1, s2, s3 = st.columns(3)


with s1:

    trees = st.slider(
        "🌳 Trees planted",
        0,
        2000,
        0,
        100,
        key="sim_trees"
    )


with s2:

    roof_area = st.slider(
        "🏠 Cool roof area (m²)",
        0,
        50000,
        0,
        5000,
        key="sim_roofs"
    )


with s3:

    shade = st.slider(
        "🚶 Shade structures",
        0,
        100,
        0,
        5,
        key="sim_shade"
    )


# =========================================================
# SIMULATION
# =========================================================

new_risk = simulate_intervention(
    risk,
    trees,
    roof_area,
    shade
)

reduction = (
    risk -
    new_risk
)

percentage = (
    reduction /
    risk *
    100
    if risk > 0
    else 0
)


# =========================================================
# RESULTS
# =========================================================

r1, r2, r3 = st.columns(3)


with r1:

    st.metric(
        "🔴 BEFORE",
        f"{risk:.1f}/100"
    )


with r2:

    st.metric(
        "🟢 AFTER",
        f"{new_risk:.1f}/100",
        delta=f"-{reduction:.1f}"
    )


with r3:

    st.metric(
        "📉 RISK REDUCTION",
        f"{percentage:.1f}%"
    )


# =========================================================
# THE ACTUAL INTERVENTION MAP
# =========================================================

st.subheader(
    "🌡️ Before → After Thermal Transformation"
)

st.caption(
    "The colour field continuously animates at browser "
    "frame rate while transitioning from the current "
    "risk to the simulated risk."
)


map_html = intervention_map_html(
    lat,
    lon,
    risk,
    new_risk,
    roads
)


components.html(
    map_html,
    height=650,
    scrolling=False
)


# =========================================================
# IMPLEMENTATION SUMMARY
# =========================================================

st.subheader(
    "🌱 Implementation"
)

implementation_parts = []

if trees > 0:

    implementation_parts.append(
        f"🌳 {trees:,} trees"
    )

if roof_area > 0:

    implementation_parts.append(
        f"🏠 {roof_area:,} m² cool roofs"
    )

if shade > 0:

    implementation_parts.append(
        f"🚶 {shade:,} shade structures"
    )


if implementation_parts:

    st.success(
        " + ".join(
            implementation_parts
        )
    )

else:

    st.info(
        "Move one of the intervention sliders "
        "to simulate implementation."
    )


# =========================================================
# COST
# =========================================================

st.divider()

st.subheader(
    "💰 Lifecycle Cost"

)

st.write(
    "The planner includes implementation AND "
    "ongoing maintenance."
)


cost = calculate_cost(
    trees,
    roof_area,
    shade
)


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Initial Cost",
        f"₹{cost['initial']:,.0f}"
    )


with c2:

    st.metric(
        "Annual Maintenance",
        f"₹{cost['maintenance']:,.0f}"
    )


with c3:

    st.metric(
        "5-Year Total",
        f"₹{cost['five_year']:,.0f}"
    )


st.markdown(
    f"""
    <div class="costbox">

    ### 🌳 Trees

    Planting + establishment:
    **₹{cost['tree_install']:,.0f}**

    Annual watering, manure,
    pruning and maintenance:
    **₹{cost['tree_maintenance']:,.0f} / year**

    ---

    ### 🏠 Cool Roofs

    Installation:
    **₹{cost['roof_install']:,.0f}**

    Annual maintenance:
    **₹{cost['roof_maintenance']:,.0f} / year**

    ---

    ### 🚶 Shade Structures

    Installation:
    **₹{cost['shade_install']:,.0f}**

    Annual maintenance:
    **₹{cost['shade_maintenance']:,.0f} / year**

    ---

    ### 💰 Lifecycle

    Initial:
    **₹{cost['initial']:,.0f}**

    Five-year maintenance:
    **₹{cost['maintenance'] * 5:,.0f}**

    **5-YEAR TOTAL:
    ₹{cost['five_year']:,.0f}**

    </div>
    """,
    unsafe_allow_html=True
)


st.caption(
    "Costs are configurable planning assumptions, "
    "not tender/contract prices."
)


# =========================================================
# BUDGET
# =========================================================

st.divider()

st.subheader(
    "💸 Budget Planner"
)

budget = st.number_input(
    "Available budget (₹)",
    min_value=100000,
    max_value=100000000,
    value=10000000,
    step=500000
)


possible_trees = int(
    budget / 650
)

possible_roofs = int(
    budget / 300
)

possible_shade = int(
    budget / 25000
)


b1, b2, b3 = st.columns(3)


with b1:

    st.metric(
        "Trees possible",
        f"{possible_trees:,}"
    )


with b2:

    st.metric(
        "Cool roof area",
        f"{possible_roofs:,} m²"
    )


with b3:

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
        ### Heat Risk

        Heat Risk =
        0.45 × Surface Heat +
        0.25 × Built-up +
        0.20 × Vegetation Deficit +
        0.10 × Population Exposure

        ### Live data

        Open-Meteo provides current atmospheric
        conditions.

        OpenStreetMap provides road-level
        geographic context.

        ### Satellite integration

        The architecture is designed to replace
        the prototype locality values with:

        • Landsat 8/9 → Surface Temperature

        • Sentinel-2 → NDVI

        • Copernicus land cover → Built-up / land cover

        • WorldPop → Population exposure

        ### Important

        The intervention thermal field is a
        visualization of the HeatScape risk model.

        It should not be presented as a physical
        prediction of exact air-temperature reduction.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "HeatScape • Urban Heat Reduction Planner"
)
