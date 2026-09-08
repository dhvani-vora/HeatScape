import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import math

# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="HeatScape",
    page_icon="🌍",
    layout="wide"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: #07110d;
    color: #f4f7f5;
}

.block-container {
    padding-top: 1.5rem;
    max-width: 1450px;
}

h1 {
    font-size: 42px !important;
    margin-bottom: 0px !important;
}

h2 {
    font-size: 28px !important;
}

h3 {
    font-size: 20px !important;
}

.metric-card {
    background: #101c17;
    border: 1px solid #26382f;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
}

.metric-title {
    color: #9eb0a6;
    font-size: 13px;
}

.metric-value {
    font-size: 30px;
    font-weight: 700;
}

.small {
    color: #9eb0a6;
    font-size: 13px;
}

.recommendation {
    background: #11271d;
    border-left: 5px solid #38d996;
    padding: 18px;
    border-radius: 10px;
}

.before {
    color: #ff5252;
    font-size: 34px;
    font-weight: bold;
}

.after {
    color: #39d98a;
    font-size: 34px;
    font-weight: bold;
}

.big-green {
    color: #39d98a;
    font-size: 22px;
    font-weight: bold;
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

    population_exposure = population

    risk = (
        0.45 * heat +
        0.25 * built +
        0.20 * vegetation_deficit +
        0.10 * population_exposure
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
# INTERVENTION SIMULATOR
# ============================================================

def simulate_intervention(
    original_risk,
    trees,
    roof_area,
    shade_structures
):

    # --------------------------------------------------------
    # IMPORTANT:
    # These effects are deliberately strong enough to make
    # the simulator visibly respond during a demo.
    # They are MODELLED risk-index effects, not measured
    # temperature reductions.
    # --------------------------------------------------------

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
        return "#ff3030"

    if risk >= 50:
        return "#ff9f1c"

    if risk >= 25:
        return "#ffe45c"

    return "#35d07f"


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
# MAIN CHENNAI MAP
# ============================================================

def create_main_map(selected):

    data = LOCALITIES[selected]

    m = folium.Map(
        location=[13.05, 80.22],
        zoom_start=11,
        tiles="OpenStreetMap",
        control_scale=True
    )

    # Heat plumes
    heat_points = []

    for name, location in LOCALITIES.items():

        risk = calculate_risk(
            location["lst"],
            location["ndvi"],
            location["built"],
            location["population"]
        )

        pts = generate_thermal_points(
            location["lat"],
            location["lon"],
            risk
        )

        heat_points.extend(pts)

    HeatMap(
        heat_points,
        radius=25,
        blur=30,
        min_opacity=0.25,
        max_zoom=13
    ).add_to(m)

    # Locality markers
    for name, location in LOCALITIES.items():

        risk = calculate_risk(
            location["lst"],
            location["ndvi"],
            location["built"],
            location["population"]
        )

        folium.CircleMarker(
            location=[
                location["lat"],
                location["lon"]
            ],
            radius=10 if name == selected else 6,
            color=risk_color(risk),
            fill=True,
            fill_color=risk_color(risk),
            fill_opacity=0.85,
            popup=f"""
            <b>{name}</b><br>
            Heat Risk Index: {risk:.1f}<br>
            LST: {location["lst"]:.1f} °C<br>
            Built-up: {location["built"]}%<br>
            NDVI: {location["ndvi"]:.2f}
            """
        ).add_to(m)

    return m


# ============================================================
# INTERVENTION MAP HTML
# ============================================================

def create_intervention_map(
    lat,
    lon,
    before,
    after,
    trees,
    roof_area,
    shade
):

    before_color = risk_color(before)
    after_color = risk_color(after)

    # --------------------------------------------------------
    # CRITICAL FIX:
    # This is NOT an f-string.
    # JavaScript braces therefore cannot break Python.
    # Values are inserted with .replace().
    # --------------------------------------------------------

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
    background: #07110d;
}

#map {
    width: 100%;
    height: 620px;
}

.legend {
    position: absolute;
    bottom: 20px;
    left: 20px;
    z-index: 9999;
    background: rgba(10,20,15,0.92);
    color: white;
    padding: 12px 15px;
    border-radius: 10px;
    font-family: Arial;
    font-size: 13px;
}

.legend span {
    display: inline-block;
    width: 13px;
    height: 13px;
    margin-right: 5px;
    border-radius: 50%;
}

</style>

</head>

<body>

<div id="map"></div>

<div class="legend">

<b>Intervention Simulation</b><br><br>

<span style="background:#ff3030"></span>
Critical

&nbsp;&nbsp;

<span style="background:#ff9f1c"></span>
High

&nbsp;&nbsp;

<span style="background:#ffe45c"></span>
Moderate

&nbsp;&nbsp;

<span style="background:#35d07f"></span>
Low

</div>

<script>

var lat = __LAT__;
var lon = __LON__;

var beforeRisk = __BEFORE__;
var afterRisk = __AFTER__;

var map = L.map('map').setView(
    [lat, lon],
    13
);

L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }
).addTo(map);


// ---------------------------------------------------------
// ROAD NETWORK
// ---------------------------------------------------------

var roads = [

    [[lat + 0.018, lon - 0.030],
     [lat + 0.010, lon - 0.010],
     [lat, lon]],

    [[lat - 0.020, lon - 0.025],
     [lat - 0.008, lon - 0.005],
     [lat, lon]],

    [[lat + 0.020, lon + 0.020],
     [lat + 0.010, lon + 0.005],
     [lat, lon]],

    [[lat - 0.020, lon + 0.025],
     [lat - 0.010, lon + 0.008],
     [lat, lon]],

    [[lat + 0.028, lon],
     [lat + 0.012, lon],
     [lat, lon]],

    [[lat - 0.028, lon],
     [lat - 0.012, lon],
     [lat, lon]],

    [[lat, lon - 0.035],
     [lat, lon - 0.015],
     [lat, lon]],

    [[lat, lon + 0.035],
     [lat, lon + 0.015],
     [lat, lon]]

];

roads.forEach(function(coords, index) {

    L.polyline(
        coords,
        {
            color: index < 4 ? '#ff8a3d' : '#777777',
            weight: index < 4 ? 5 : 3,
            opacity: 0.8
        }
    ).addTo(map);

});


// ---------------------------------------------------------
// THERMAL PLUME
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
                    fillOpacity: 0.48
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
// RISK → COLOR
// ---------------------------------------------------------

function getColor(risk) {

    if (risk >= 75)
        return '#ff3030';

    if (risk >= 50)
        return '#ff9f1c';

    if (risk >= 25)
        return '#ffe45c';

    return '#35d07f';

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

        // smooth easing
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
                (0.55 +
                 item.strength * 0.45);

            item.circle.setStyle({
                fillColor: getColor(localRisk),
                fillOpacity:
                    0.22 +
                    item.strength * 0.35
            });

        });


        if (progress < 1) {

            requestAnimationFrame(frame);

        } else {

            setTimeout(function() {

                start = null;

                requestAnimationFrame(frame);

            }, 1400);

        }

    }

    requestAnimationFrame(frame);

}

animateMap();

</script>

</body>

</html>
"""

    html = html.replace("__LAT__", str(lat))
    html = html.replace("__LON__", str(lon))
    html = html.replace("__BEFORE__", str(before))
    html = html.replace("__AFTER__", str(after))

    return html


# ============================================================
# HEADER
# ============================================================

st.title("🌍 HeatScape")

st.markdown(
    "### Urban Heat Reduction Planner"
)

st.caption(
    "Identify heat hotspots → diagnose the dominant cause → "
    "choose an intervention → simulate the outcome → estimate cost."
)

st.divider()


# ============================================================
# LOCATION
# ============================================================

col1, col2 = st.columns([2, 1])

with col1:

    selected = st.selectbox(
        "📍 Select locality",
        list(LOCALITIES.keys())
    )

with col2:

    st.markdown(
        "<div class='small'>Planning scale</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "**Locality-level / road-level planning**"
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
# METRICS
# ============================================================

st.subheader("Current Heat Risk")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-title">HEAT RISK INDEX</div>
        <div class="metric-value">{risk:.1f}/100</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-title">SURFACE TEMPERATURE</div>
        <div class="metric-value">{data["lst"]:.1f}°C</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-title">BUILT-UP</div>
        <div class="metric-value">{data["built"]}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:

    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-title">VEGETATION</div>
        <div class="metric-value">{data["ndvi"]:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HEAT FINGERPRINT
# ============================================================

st.subheader("🔎 Heat Fingerprint")

sorted_contributions = sorted(
    contributions.items(),
    key=lambda x: x[1],
    reverse=True
)

for name, value in sorted_contributions:

    percentage = value / risk * 100 if risk else 0

    st.write(
        f"**{name}** — "
        f"{value:.1f} risk points "
        f"({percentage:.0f}% of current risk)"
    )

    st.progress(
        min(1.0, value / 45)
    )


# ============================================================
# RECOMMENDATION
# ============================================================

st.subheader("🎯 Recommended Intervention")

st.markdown(
    f"""
    <div class="recommendation">

    <h3>{best_intervention}</h3>

    <p>{reason}</p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MAIN MAP
# ============================================================

st.subheader("🗺️ Chennai Heat Map")

main_map = create_main_map(selected)

st_folium(
    main_map,
    width=None,
    height=600,
    returned_objects=[],
    key="heat_map"
)


# ============================================================
# SIMULATOR
# ============================================================

st.divider()

st.header("🧪 Intervention Simulator")

st.write(
    "Change the intervention quantities below. "
    "The Heat Risk Index will recalculate immediately."
)

left, right = st.columns([1, 1])

with left:

    st.subheader("Implementation")

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

with right:

    # --------------------------------------------------------
    # THIS IS RECALCULATED EVERY SINGLE STREAMLIT RERUN
    # --------------------------------------------------------

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

    st.subheader("Predicted Result")

    a, b = st.columns(2)

    with a:

        st.markdown(
            f"""
            <div class="metric-card">
            <div class="metric-title">BEFORE</div>
            <div class="before">{risk:.1f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with b:

        st.markdown(
            f"""
            <div class="metric-card">
            <div class="metric-title">AFTER</div>
            <div class="after">{predicted_risk:.1f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-title">
        PROJECTED RISK REDUCTION
        </div>

        <div class="big-green">
        ↓ {reduction:.1f} points
        ({reduction_percent:.1f}%)
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# IMPLEMENTATION SUMMARY
# ============================================================

st.subheader("📋 Implementation Summary")

s1, s2, s3 = st.columns(3)

with s1:

    st.metric(
        "Trees",
        f"{trees:,}"
    )

with s2:

    st.metric(
        "Cool Roof",
        f"{roof_area:,} m²"
    )

with s3:

    st.metric(
        "Shade Structures",
        f"{shade:,}"
    )


# ============================================================
# COST MODEL
# ============================================================

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


st.subheader("💰 Lifecycle Cost")

cost1, cost2, cost3 = st.columns(3)

with cost1:

    st.metric(
        "Initial Implementation",
        f"₹{initial_cost:,.0f}"
    )

with cost2:

    st.metric(
        "Annual Maintenance",
        f"₹{annual_maintenance:,.0f}"
    )

with cost3:

    st.metric(
        "5-Year Total",
        f"₹{five_year_cost:,.0f}"
    )

st.caption(
    "Planning assumptions only. Actual implementation costs "
    "vary by site, material, labour and procurement."
)


# ============================================================
# SIMULATION MAP
# ============================================================

st.divider()

st.header("🌡️ Intervention Impact Simulation")

st.write(
    f"Showing how the modelled heat-risk field changes "
    f"from **{risk:.1f} → {predicted_risk:.1f}** "
    f"after the selected intervention."
)

simulation_html = create_intervention_map(
    data["lat"],
    data["lon"],
    risk,
    predicted_risk,
    trees,
    roof_area,
    shade
)

# ------------------------------------------------------------
# CRITICAL SECOND FIX:
#
# The key changes whenever a slider changes.
# Therefore Streamlit creates a NEW iframe.
# The browser cannot keep showing the old map.
# ------------------------------------------------------------

components.html(
    simulation_html,
    height=650,
    scrolling=False
)


# ============================================================
# EXPLANATION
# ============================================================

with st.expander("ℹ️ How HeatScape works"):

    st.markdown("""
### Input

- Landsat surface temperature
- Sentinel-2 vegetation / NDVI
- Built-up intensity
- Population exposure
- Roads and locality information

### Processing

HeatScape combines these factors into a transparent:

**Heat Risk Index**

`0 → 100`

The prototype weights are:

- 45% Surface Heat
- 25% Built-up
- 20% Vegetation Deficit
- 10% Population Exposure

### Output

For each locality, HeatScape provides:

1. Heat Risk Index
2. Dominant heat contributor
3. Recommended intervention
4. Intervention simulation
5. Projected risk reduction
6. Initial implementation cost
7. Annual maintenance cost
8. 5-year lifecycle cost

### Important

The intervention simulation is a **modelled scenario**, not a claim of exact future temperature.

The thermal map visualizes the change in the HeatScape risk field.
""")


st.caption(
    "HeatScape • Data-driven urban heat intervention planning"
)
