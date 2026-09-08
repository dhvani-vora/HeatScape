import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import math


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HeatScape | Urban Heat Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f6f7f5;
    color: #18231e;
}

/* Remove excessive Streamlit spacing */
.block-container {
    max-width: 1440px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

/* Main titles */
h1 {
    font-size: 42px !important;
    font-weight: 700 !important;
    letter-spacing: -1.5px;
    color: #152019 !important;
}

h2 {
    font-size: 27px !important;
    font-weight: 700 !important;
    letter-spacing: -0.7px;
    color: #152019 !important;
}

h3 {
    font-size: 19px !important;
    font-weight: 700 !important;
    color: #18231e !important;
}

/* Paragraphs */
p {
    color: #53615a;
}

/* Captions */
.stCaption {
    color: #738078 !important;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #dfe4e0;
    margin: 2rem 0;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: white !important;
    border: 1px solid #d8ded9 !important;
    border-radius: 10px !important;
    min-height: 45px;
}

/* Slider */
div[data-testid="stSlider"] {
    padding-top: 0.3rem;
}

/* Metric cards */
.metric-card {
    background: #ffffff;
    border: 1px solid #e1e6e2;
    border-radius: 14px;
    padding: 20px 22px;
    min-height: 112px;
    box-shadow: 0 2px 8px rgba(20, 35, 28, 0.035);
}

.metric-label {
    color: #758179;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.metric-value {
    color: #17231d;
    font-size: 30px;
    line-height: 1.1;
    font-weight: 700;
}

.metric-sub {
    color: #7b8780;
    font-size: 12px;
    margin-top: 6px;
}

/* Risk hero */
.risk-card {
    background: #17241d;
    color: white;
    border-radius: 16px;
    padding: 26px 28px;
    min-height: 145px;
    box-shadow: 0 8px 24px rgba(22, 38, 29, 0.12);
}

.risk-label {
    color: #aebbb3;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.1px;
    text-transform: uppercase;
}

.risk-number {
    color: white;
    font-size: 45px;
    font-weight: 700;
    letter-spacing: -2px;
    margin-top: 6px;
}

.risk-status {
    color: #d6e2da;
    font-size: 13px;
    margin-top: 4px;
}

/* Recommendation */
.recommendation-card {
    background: #ffffff;
    border: 1px solid #dfe7e1;
    border-radius: 16px;
    padding: 24px 26px;
    box-shadow: 0 3px 12px rgba(20, 35, 28, 0.035);
}

.recommendation-tag {
    color: #25825a;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.recommendation-title {
    color: #17231d;
    font-size: 23px;
    font-weight: 700;
    margin-top: 6px;
}

.recommendation-text {
    color: #5e6963;
    font-size: 14px;
    line-height: 1.6;
    margin-top: 8px;
}

/* Fingerprint */
.fingerprint-card {
    background: white;
    border: 1px solid #e1e6e2;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 10px;
}

.fingerprint-name {
    font-size: 14px;
    font-weight: 600;
    color: #26322c;
}

.fingerprint-value {
    float: right;
    font-size: 13px;
    font-weight: 600;
    color: #69756e;
}

/* Simulator */
.simulator-card {
    background: #ffffff;
    border: 1px solid #dfe5e1;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 3px 12px rgba(20, 35, 28, 0.035);
}

.simulator-label {
    color: #758179;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.before-number {
    color: #d94c45;
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -1.5px;
}

.after-number {
    color: #26845a;
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -1.5px;
}

.arrow {
    color: #a4aea8;
    font-size: 26px;
    text-align: center;
    padding-top: 14px;
}

.reduction-card {
    background: #edf7f0;
    border: 1px solid #d2ead9;
    border-radius: 12px;
    padding: 15px 18px;
    margin-top: 15px;
}

.reduction-number {
    color: #23794f;
    font-size: 20px;
    font-weight: 700;
}

.reduction-label {
    color: #5b7164;
    font-size: 12px;
    margin-top: 2px;
}

/* Section eyebrow */
.eyebrow {
    color: #31815c;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 5px;
}

/* Cost */
.cost-card {
    background: white;
    border: 1px solid #e1e6e2;
    border-radius: 14px;
    padding: 20px;
    min-height: 118px;
}

.cost-label {
    color: #78847d;
    font-size: 12px;
    margin-bottom: 8px;
}

.cost-value {
    color: #1a2820;
    font-size: 24px;
    font-weight: 700;
}

/* Info box */
.info-box {
    background: #f0f4f1;
    border: 1px solid #dce5df;
    border-radius: 12px;
    padding: 16px 18px;
    color: #5c6961;
    font-size: 13px;
}

/* Buttons */
.stButton > button {
    border-radius: 9px;
    border: 1px solid #ccd6cf;
    background: white;
    color: #233029;
    font-weight: 600;
    min-height: 42px;
}

.stButton > button:hover {
    border-color: #3b8d65;
    color: #26744f;
}

/* Expander */
.streamlit-expanderHeader {
    font-weight: 600 !important;
    color: #27342d !important;
}

/* Map spacing */
.map-wrap {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #dce2de;
}

/* Footer */
.footer {
    text-align: center;
    color: #87928c;
    font-size: 12px;
    padding-top: 30px;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOCALITY DATA
# ============================================================

LOCALITIES = {

    "Washermanpet": {
        "lat": 13.116,
        "lon": 80.279,
        "lst": 41.6,
        "ndvi": 0.14,
        "built": 84,
        "population": 91
    },

    "Royapuram": {
        "lat": 13.115,
        "lon": 80.294,
        "lst": 41.4,
        "ndvi": 0.15,
        "built": 82,
        "population": 89
    },

    "Perambur": {
        "lat": 13.116,
        "lon": 80.233,
        "lst": 40.8,
        "ndvi": 0.19,
        "built": 78,
        "population": 86
    },

    "Ambattur": {
        "lat": 13.114,
        "lon": 80.154,
        "lst": 40.7,
        "ndvi": 0.20,
        "built": 79,
        "population": 78
    },

    "Avadi": {
        "lat": 13.106,
        "lon": 80.096,
        "lst": 39.5,
        "ndvi": 0.28,
        "built": 68,
        "population": 72
    },

    "Anna Nagar": {
        "lat": 13.085,
        "lon": 80.210,
        "lst": 40.0,
        "ndvi": 0.25,
        "built": 76,
        "population": 80
    },

    "Nungambakkam": {
        "lat": 13.056,
        "lon": 80.242,
        "lst": 40.1,
        "ndvi": 0.24,
        "built": 77,
        "population": 79
    },

    "T Nagar": {
        "lat": 13.041,
        "lon": 80.234,
        "lst": 40.3,
        "ndvi": 0.21,
        "built": 83,
        "population": 87
    },

    "Mylapore": {
        "lat": 13.033,
        "lon": 80.269,
        "lst": 39.4,
        "ndvi": 0.29,
        "built": 73,
        "population": 76
    },

    "Guindy": {
        "lat": 13.006,
        "lon": 80.220,
        "lst": 39.0,
        "ndvi": 0.34,
        "built": 66,
        "population": 70
    },

    "Adyar": {
        "lat": 13.006,
        "lon": 80.257,
        "lst": 38.6,
        "ndvi": 0.39,
        "built": 61,
        "population": 68
    },

    "Velachery": {
        "lat": 12.981,
        "lon": 80.218,
        "lst": 39.1,
        "ndvi": 0.31,
        "built": 69,
        "population": 77
    },

    "Perungudi": {
        "lat": 12.960,
        "lon": 80.245,
        "lst": 38.9,
        "ndvi": 0.33,
        "built": 67,
        "population": 71
    },

    "Sholinganallur": {
        "lat": 12.901,
        "lon": 80.227,
        "lst": 38.0,
        "ndvi": 0.40,
        "built": 62,
        "population": 69
    },

    "Tambaram": {
        "lat": 12.925,
        "lon": 80.127,
        "lst": 37.4,
        "ndvi": 0.46,
        "built": 58,
        "population": 62
    }
}


# ============================================================
# HEAT RISK ENGINE
# ============================================================

def normalize(value, minimum, maximum):

    result = ((value - minimum) / (maximum - minimum)) * 100

    return max(0, min(100, result))


def calculate_risk(lst, ndvi, built, population):

    heat = normalize(lst, 30, 45)

    vegetation_deficit = max(
        0,
        min(100, 100 - ndvi * 100)
    )

    risk = (
        0.45 * heat +
        0.25 * built +
        0.20 * vegetation_deficit +
        0.10 * population
    )

    return max(0, min(100, risk))


# ============================================================
# CONTRIBUTIONS
# ============================================================

def get_contributions(data):

    heat = normalize(data["lst"], 30, 45)

    vegetation_deficit = max(
        0,
        min(100, 100 - data["ndvi"] * 100)
    )

    return {
        "Surface Heat": 0.45 * heat,
        "Built-up Intensity": 0.25 * data["built"],
        "Vegetation Deficit": 0.20 * vegetation_deficit,
        "Population Exposure": 0.10 * data["population"]
    }


# ============================================================
# RECOMMENDATION
# ============================================================

def recommendation(data):

    contributions = get_contributions(data)

    dominant = max(
        contributions,
        key=contributions.get
    )

    if dominant == "Vegetation Deficit":

        return (
            "Tree planting / Green Corridor",
            "Vegetation deficit is the dominant contributor. "
            "Increasing tree cover and connected green space "
            "is the strongest first intervention."
        )

    if dominant == "Built-up Intensity":

        return (
            "Cool Roofs",
            "Built-up intensity is the dominant contributor. "
            "Reflective or cool roofs can reduce heat absorption "
            "across large built surfaces."
        )

    if dominant == "Surface Heat":

        return (
            "Combined Green + Shade Intervention",
            "Surface heat is the dominant contributor. "
            "A combination of vegetation and pedestrian shade "
            "is recommended."
        )

    return (
        "Targeted Cooling Corridor",
        "Population exposure is significant. "
        "Prioritize cooling interventions around highly "
        "used public areas."
    )


# ============================================================
# INTERVENTION SIMULATION
# ============================================================

def simulate_intervention(
    original_risk,
    trees,
    roof_area,
    shade_structures
):

    tree_effect = (trees / 2000.0) * 18.0

    roof_effect = (roof_area / 50000.0) * 14.0

    shade_effect = (shade_structures / 100.0) * 8.0

    total_reduction = (
        tree_effect +
        roof_effect +
        shade_effect
    )

    total_reduction = min(
        total_reduction,
        original_risk * 0.75
    )

    new_risk = max(
        0,
        original_risk - total_reduction
    )

    return new_risk, total_reduction


# ============================================================
# RISK COLOR
# ============================================================

def risk_color(risk):

    if risk >= 75:
        return "#e54848"

    if risk >= 50:
        return "#f39a35"

    if risk >= 25:
        return "#e7ca4d"

    return "#38b879"


# ============================================================
# THERMAL PLUME
# ============================================================

def generate_thermal_points(lat, lon, risk):

    points = []

    radius = 0.025

    for y in range(-10, 11):

        for x in range(-10, 11):

            distance = math.sqrt(
                x * x + y * y
            )

            intensity = math.exp(
                -(distance ** 2) / 35
            )

            intensity *= risk / 100

            if intensity > 0.04:

                p_lat = lat + (y / 10) * radius

                p_lon = lon + (x / 10) * radius

                points.append([
                    p_lat,
                    p_lon,
                    intensity
                ])

    return points


# ============================================================
# MAIN MAP
# ============================================================

def create_main_map(selected):

    data = LOCALITIES[selected]

    m = folium.Map(
        location=[13.05, 80.22],
        zoom_start=11,
        tiles="OpenStreetMap",
        control_scale=True
    )

    heat_points = []

    for name, location in LOCALITIES.items():

        risk = calculate_risk(
            location["lst"],
            location["ndvi"],
            location["built"],
            location["population"]
        )

        heat_points.extend(
            generate_thermal_points(
                location["lat"],
                location["lon"],
                risk
            )
        )

    HeatMap(
        heat_points,
        radius=25,
        blur=30,
        min_opacity=0.25,
        max_zoom=13
    ).add_to(m)

    for name, location in LOCALITIES.items():

        risk = calculate_risk(
            location["lst"],
            location["ndvi"],
            location["built"],
            location["population"]
        )

        selected_radius = 11 if name == selected else 6

        folium.CircleMarker(
            location=[
                location["lat"],
                location["lon"]
            ],
            radius=selected_radius,
            color=risk_color(risk),
            fill=True,
            fill_color=risk_color(risk),
            fill_opacity=0.9,
            weight=2,
            popup=folium.Popup(
                f"""
                <div style="
                    font-family:Arial;
                    min-width:180px;
                    line-height:1.6;
                ">
                    <b style="font-size:16px;">{name}</b><br>
                    <span style="color:#666;">
                    Heat Risk
                    </span>
                    <b>{risk:.1f}/100</b><br>
                    Surface Temperature: {location["lst"]:.1f}°C<br>
                    Built-up: {location["built"]}%<br>
                    NDVI: {location["ndvi"]:.2f}
                </div>
                """,
                max_width=280
            )
        ).add_to(m)

    return m


# ============================================================
# INTERVENTION MAP
# ============================================================

def create_intervention_map(
    lat,
    lon,
    before,
    after
):

    html = """
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<link
rel="stylesheet"
href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
/>

<script
src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js">
</script>

<style>

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: #f6f7f5;
}

#map {
    width: 100%;
    height: 620px;
}

.legend {
    position: absolute;
    bottom: 18px;
    left: 18px;
    z-index: 9999;

    background: rgba(255,255,255,0.96);

    border: 1px solid #d9dfdb;

    color: #26332c;

    padding: 13px 15px;

    border-radius: 10px;

    font-family: Arial, sans-serif;

    font-size: 12px;

    box-shadow: 0 2px 10px rgba(0,0,0,0.10);
}

.legend-title {
    font-weight: bold;
    margin-bottom: 8px;
}

.legend-row {
    margin: 5px 0;
}

.legend-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 6px;
}

</style>

</head>

<body>

<div id="map"></div>

<div class="legend">

<div class="legend-title">
Heat Risk
</div>

<div class="legend-row">
<span class="legend-dot"
style="background:#e54848"></span>
Critical
</div>

<div class="legend-row">
<span class="legend-dot"
style="background:#f39a35"></span>
High
</div>

<div class="legend-row">
<span class="legend-dot"
style="background:#e7ca4d"></span>
Moderate
</div>

<div class="legend-row">
<span class="legend-dot"
style="background:#38b879"></span>
Low
</div>

</div>

<script>

var lat = __LAT__;
var lon = __LON__;

var beforeRisk = __BEFORE__;
var afterRisk = __AFTER__;

var map = L.map('map', {
    zoomControl: true
}).setView(
    [lat, lon],
    14
);

L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
        maxZoom: 19,
        attribution:
        '&copy; OpenStreetMap contributors'
    }
).addTo(map);


// ---------------------------------------------------------
// SELECTED LOCATION
// ---------------------------------------------------------

L.circleMarker(
    [lat, lon],
    {
        radius: 7,
        color: '#ffffff',
        weight: 3,
        fillColor: '#e54848',
        fillOpacity: 1
    }
).addTo(map);


// ---------------------------------------------------------
// THERMAL FIELD
// ---------------------------------------------------------

var cells = [];

for (var y = -12; y <= 12; y++) {

    for (var x = -12; x <= 12; x++) {

        var distance = Math.sqrt(
            x*x + y*y
        );

        var strength = Math.exp(
            -(distance*distance) / 55
        );

        if (strength > 0.08) {

            var pLat =
                lat + (y / 10) * 0.022;

            var pLon =
                lon + (x / 10) * 0.022;

            var circle = L.circle(
                [pLat, pLon],
                {
                    radius: 95,
                    stroke: false,
                    fillOpacity: 0.40
                }
            ).addTo(map);

            cells.push({
                circle: circle,
                strength: strength
            });

        }

    }

}


// ---------------------------------------------------------
// COLOR FUNCTION
// ---------------------------------------------------------

function getColor(risk) {

    if (risk >= 75)
        return '#e54848';

    if (risk >= 50)
        return '#f39a35';

    if (risk >= 25)
        return '#e7ca4d';

    return '#38b879';

}


// ---------------------------------------------------------
// ANIMATION
// ---------------------------------------------------------

function animateMap() {

    var start = null;

    var duration = 1800;

    function frame(timestamp) {

        if (!start)
            start = timestamp;

        var progress =
            (timestamp - start) / duration;

        if (progress > 1)
            progress = 1;

        var eased =
            progress * progress *
            (3 - 2 * progress);

        var currentRisk =
            beforeRisk +
            (afterRisk - beforeRisk) *
            eased;

        cells.forEach(function(item) {

            var localRisk =
                currentRisk *
                (
                    0.55 +
                    item.strength * 0.45
                );

            item.circle.setStyle({

                fillColor:
                    getColor(localRisk),

                fillOpacity:
                    0.18 +
                    item.strength * 0.35

            });

        });

        if (progress < 1) {

            requestAnimationFrame(frame);

        }

    }

    requestAnimationFrame(frame);

}

animateMap();

</script>

</body>

</html>
"""

    html = html.replace(
        "__LAT__",
        str(lat)
    )

    html = html.replace(
        "__LON__",
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

    return html


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [4, 1]
)

with header_left:

    st.markdown(
        "<div class='eyebrow'>CLIMATE INTELLIGENCE · CHENNAI</div>",
        unsafe_allow_html=True
    )

    st.title("HeatScape")

    st.markdown(
        "Urban heat reduction planning, made simple."
    )

with header_right:

    st.markdown(
        "<div style='text-align:right; padding-top:12px;'>"
        "<span style='font-size:12px; color:#758179;'>"
        "GREATER CHENNAI"
        "</span><br>"
        "<span style='font-size:13px; font-weight:600;'>"
        "Planning View"
        "</span>"
        "</div>",
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# LOCATION
# ============================================================

st.markdown(
    "<div class='eyebrow'>01 · SELECT LOCATION</div>",
    unsafe_allow_html=True
)

location_col, status_col = st.columns(
    [2.5, 1]
)

with location_col:

    selected = st.selectbox(
        "Locality",
        list(LOCALITIES.keys()),
        label_visibility="collapsed"
    )

with status_col:

    st.markdown(
        """
        <div style="
            padding-top:10px;
            text-align:right;
            color:#66736b;
            font-size:13px;
        ">
        ● Planning dataset active
        </div>
        """,
        unsafe_allow_html=True
    )


data = LOCALITIES[selected]


# ============================================================
# BASE RISK
# ============================================================

risk = calculate_risk(
    data["lst"],
    data["ndvi"],
    data["built"],
    data["population"]
)

contributions = get_contributions(data)

best_intervention, reason = recommendation(data)


# ============================================================
# LOCATION OVERVIEW
# ============================================================

st.markdown(
    f"""
    <div style="
        display:flex;
        justify-content:space-between;
        align-items:end;
        margin-top:22px;
        margin-bottom:12px;
    ">
        <div>
            <div class="eyebrow">CURRENT CONDITIONS</div>
            <div style="
                font-size:25px;
                font-weight:700;
                color:#17231d;
            ">
                {selected}
            </div>
        </div>
        <div style="
            color:#7a857e;
            font-size:13px;
        ">
            Locality-level assessment
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


m1, m2, m3, m4 = st.columns(4)

with m1:

    st.markdown(
        f"""
        <div class="risk-card">
            <div class="risk-label">
                Heat Risk Index
            </div>
            <div class="risk-number">
                {risk:.1f}
            </div>
            <div class="risk-status">
                out of 100
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                Surface Temperature
            </div>
            <div class="metric-value">
                {data["lst"]:.1f}°C
            </div>
            <div class="metric-sub">
                Observed surface heat
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                Built-up Intensity
            </div>
            <div class="metric-value">
                {data["built"]}%
            </div>
            <div class="metric-sub">
                Developed surface
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                Vegetation
            </div>
            <div class="metric-value">
                {data["ndvi"]:.2f}
            </div>
            <div class="metric-sub">
                NDVI indicator
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN MAP
# ============================================================

st.markdown(
    "<div style='height:18px'></div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='eyebrow'>02 · EXPLORE THE HOTSPOT</div>",
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:12px;
    ">

        <div>
            <div style="
                font-size:23px;
                font-weight:700;
                color:#17231d;
            ">
                Chennai heat map
            </div>

            <div style="
                font-size:13px;
                color:#718078;
                margin-top:3px;
            ">
                Thermal intensity across selected localities
            </div>
        </div>

        <div style="
            font-size:12px;
            color:#718078;
        ">
            OpenStreetMap · Leaflet
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


main_map = create_main_map(selected)

st_folium(
    main_map,
    width=None,
    height=570,
    returned_objects=[],
    key="main_heat_map"
)


# ============================================================
# DIAGNOSIS
# ============================================================

st.divider()

st.markdown(
    "<div class='eyebrow'>03 · UNDERSTAND THE HOTSPOT</div>",
    unsafe_allow_html=True
)

diag_left, diag_right = st.columns(
    [1.05, 0.95],
    gap="large"
)


with diag_left:

    st.markdown(
        f"""
        <div style="
            font-size:23px;
            font-weight:700;
            color:#17231d;
            margin-bottom:5px;
        ">
            What's driving the heat?
        </div>

        <div style="
            color:#718078;
            font-size:13px;
            margin-bottom:18px;
        ">
            Contribution to the current Heat Risk Index
        </div>
        """,
        unsafe_allow_html=True
    )

    sorted_contributions = sorted(
        contributions.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for name, value in sorted_contributions:

        percentage = (
            value / risk * 100
            if risk > 0
            else 0
        )

        st.markdown(
            f"""
            <div class="fingerprint-card">

                <div>
                    <span class="fingerprint-name">
                        {name}
                    </span>

                    <span class="fingerprint-value">
                        {percentage:.0f}%
                    </span>
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            min(1.0, value / 45)
        )


with diag_right:

    st.markdown(
        f"""
        <div class="recommendation-card">

            <div class="recommendation-tag">
                Recommended first action
            </div>

            <div class="recommendation-title">
                {best_intervention}
            </div>

            <div class="recommendation-text">
                {reason}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='height:12px'></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="info-box">

        <b>Decision logic</b><br><br>

        HeatScape identifies the largest contributor to
        the locality's Heat Risk Index and uses it to select
        the first intervention to test.

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SIMULATOR
# ============================================================

st.divider()

st.markdown(
    "<div class='eyebrow'>04 · TEST AN INTERVENTION</div>",
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div style="
        font-size:26px;
        font-weight:700;
        color:#17231d;
    ">
        What happens if we cool {selected}?
    </div>

    <div style="
        color:#718078;
        font-size:14px;
        margin-top:4px;
        margin-bottom:22px;
    ">
        Adjust the implementation and watch the modelled
        Heat Risk change.
    </div>
    """,
    unsafe_allow_html=True
)


sim_left, sim_right = st.columns(
    [1, 1.25],
    gap="large"
)


# ------------------------------------------------------------
# CONTROLS
# ------------------------------------------------------------

with sim_left:

    st.markdown(
        "<div class='simulator-card'>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='font-size:17px;font-weight:700;margin-bottom:4px;'>"
        "Implementation"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='color:#718078;font-size:12px;margin-bottom:16px;'>"
        "Set the scale of each cooling measure."
        "</div>",
        unsafe_allow_html=True
    )

    trees = st.slider(
        "🌳 Trees planted",
        min_value=0,
        max_value=2000,
        value=0,
        step=50,
        key="trees_slider"
    )

    roof_area = st.slider(
        "🏠 Cool roof area (m²)",
        min_value=0,
        max_value=50000,
        value=0,
        step=1000,
        key="roof_slider"
    )

    shade = st.slider(
        "🚶 Shade structures",
        min_value=0,
        max_value=100,
        value=0,
        step=5,
        key="shade_slider"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# CALCULATION
# ------------------------------------------------------------

predicted_risk, reduction = simulate_intervention(
    risk,
    trees,
    roof_area,
    shade
)

reduction_percent = (
    reduction / risk * 100
    if risk > 0
    else 0
)


# ------------------------------------------------------------
# RESULT
# ------------------------------------------------------------

with sim_right:

    st.markdown(
        "<div class='simulator-card'>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='font-size:17px;font-weight:700;margin-bottom:16px;'>"
        "Projected impact"
        "</div>",
        unsafe_allow_html=True
    )

    before_col, arrow_col, after_col = st.columns(
        [1, 0.25, 1]
    )

    with before_col:

        st.markdown(
            f"""
            <div class="simulator-label">
                Current risk
            </div>

            <div class="before-number">
                {risk:.1f}
            </div>
            """,
            unsafe_allow_html=True
        )

    with arrow_col:

        st.markdown(
            "<div class='arrow'>→</div>",
            unsafe_allow_html=True
        )

    with after_col:

        st.markdown(
            f"""
            <div class="simulator-label">
                Projected risk
            </div>

            <div class="after-number">
                {predicted_risk:.1f}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="reduction-card">

            <div class="reduction-number">
                ↓ {reduction:.1f} risk points
            </div>

            <div class="reduction-label">
                {reduction_percent:.1f}% projected reduction
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# IMPLEMENTATION SUMMARY
# ============================================================

st.markdown(
    "<div style='height:22px'></div>",
    unsafe_allow_html=True
)

s1, s2, s3 = st.columns(3)

with s1:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Trees
            </div>

            <div class="metric-value">
                {trees:,}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with s2:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Cool Roof
            </div>

            <div class="metric-value">
                {roof_area:,} m²
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with s3:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Shade Structures
            </div>

            <div class="metric-value">
                {shade:,}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# INTERVENTION MAP
# ============================================================

st.markdown(
    "<div style='height:28px'></div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='eyebrow'>05 · WATCH THE CHANGE</div>",
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div style="
        font-size:25px;
        font-weight:700;
        color:#17231d;
    ">
        Intervention impact simulation
    </div>

    <div style="
        color:#718078;
        font-size:13px;
        margin-top:4px;
        margin-bottom:14px;
    ">
        Modelled heat-risk field for {selected}
    </div>
    """,
    unsafe_allow_html=True
)


simulation_html = create_intervention_map(
    data["lat"],
    data["lon"],
    risk,
    predicted_risk
)

components.html(
    simulation_html,
    height=640,
    scrolling=False
)


st.markdown(
    """
    <div style="
        color:#7c8781;
        font-size:11px;
        margin-top:6px;
    ">
        The thermal field represents the modelled Heat Risk Index,
        not physical heat dispersion or exact temperature reduction.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# COST MODEL
# ============================================================

st.divider()

st.markdown(
    "<div class='eyebrow'>06 · COST OF IMPLEMENTATION</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        font-size:25px;
        font-weight:700;
        color:#17231d;
    ">
        What would this cost?
    </div>

    <div style="
        color:#718078;
        font-size:13px;
        margin-top:4px;
        margin-bottom:18px;
    ">
        Lifecycle estimate for the selected intervention mix
    </div>
    """,
    unsafe_allow_html=True
)


tree_install = trees * 650
tree_establishment = trees * 300
tree_maintenance = trees * 250

roof_install = roof_area * 300
roof_maintenance = roof_area * 30

shade_install = shade * 25000
shade_maintenance = shade * 2500

initial_cost = (
    tree_install +
    tree_establishment +
    roof_install +
    shade_install
)

annual_maintenance = (
    tree_maintenance +
    roof_maintenance +
    shade_maintenance
)

five_year_cost = (
    initial_cost +
    annual_maintenance * 5
)


c1, c2, c3 = st.columns(3)

with c1:

    st.markdown(
        f"""
        <div class="cost-card">

            <div class="cost-label">
                Initial implementation
            </div>

            <div class="cost-value">
                ₹{initial_cost:,.0f}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        f"""
        <div class="cost-card">

            <div class="cost-label">
                Annual maintenance
            </div>

            <div class="cost-value">
                ₹{annual_maintenance:,.0f}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        f"""
        <div class="cost-card">

            <div class="cost-label">
                5-year lifecycle
            </div>

            <div class="cost-value">
                ₹{five_year_cost:,.0f}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    "<div style='height:10px'></div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-box">

    <b>Included in the estimate</b><br><br>

    Trees: planting, establishment, watering and recurring maintenance
    &nbsp; · &nbsp;
    Cool roofs: installation and maintenance
    &nbsp; · &nbsp;
    Shade structures: installation and maintenance

    <br><br>

    Planning assumptions only. Actual costs vary by site,
    material, labour and procurement.

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# METHODOLOGY
# ============================================================

st.divider()

with st.expander("Methodology & data sources"):

    st.markdown(
        """
### Heat Risk Index

HeatScape combines four transparent indicators:

| Factor | Weight |
|---|---:|
| Surface Heat | 45% |
| Built-up Intensity | 25% |
| Vegetation Deficit | 20% |
| Population Exposure | 10% |

The resulting **Heat Risk Index ranges from 0–100**.

### Data inputs

**Landsat**  
Surface temperature

**Sentinel-2**  
Vegetation / NDVI

**Land cover**  
Built-up intensity

**WorldPop**  
Population exposure

**OpenStreetMap**  
Road network and geographic context

### Interpretation

The intervention simulator is a modelled scenario tool.
It estimates how changing intervention quantities affects
the HeatScape risk index.

It is not a validated physical climate model and does not
claim an exact future air-temperature reduction.
"""
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        HeatScape · Urban Heat Reduction Planner
        <br>
        Decision support for targeted, explainable cooling interventions
    </div>
    """,
    unsafe_allow_html=True
)
