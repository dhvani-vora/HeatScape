
# ============================================================
# PAGE
# PAGE CONFIG
# ============================================================

st.set_page_config(
@@ -19,7 +19,7 @@


# ============================================================
# PROFESSIONAL UI
# GLOBAL STYLE
# ============================================================

st.markdown("""
@@ -42,7 +42,6 @@
    padding-bottom: 60px;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}
@@ -55,32 +54,27 @@
    visibility: hidden;
}

/* Typography */

h1 {
    font-size: 44px !important;
    font-weight: 700 !important;
    letter-spacing: -2px;
    color: #17231d !important;
}

h2 {
h2, h3 {
    color: #17231d !important;
}

h3 {
    color: #17231d !important;
}

/* Divider */

hr {
    border: none !important;
    border-top: 1px solid #dfe5e1 !important;
    margin: 32px 0 !important;
}

/* Eyebrow */

/* ============================================================
   LABELS
   ============================================================ */

.eyebrow {
    color: #2f8059;
@@ -91,15 +85,18 @@
    margin-bottom: 7px;
}

/* Cards */

/* ============================================================
   METRIC CARDS
   ============================================================ */

.metric-card {
    background: #ffffff;
    border: 1px solid #e1e6e2;
    border-radius: 15px;
    padding: 21px 22px;
    min-height: 112px;
    box-shadow: 0 2px 8px rgba(20, 35, 28, 0.035);
    box-shadow: 0 2px 8px rgba(20,35,28,0.035);
}

.metric-label {
@@ -124,14 +121,17 @@
    margin-top: 6px;
}

/* Risk */

/* ============================================================
   RISK CARD
   ============================================================ */

.risk-card {
    background: #17241d;
    border-radius: 15px;
    padding: 22px 24px;
    min-height: 112px;
    box-shadow: 0 6px 20px rgba(20, 35, 28, 0.10);
    box-shadow: 0 6px 20px rgba(20,35,28,0.10);
}

.risk-label {
@@ -155,69 +155,78 @@
    font-size: 12px;
}

/* Recommendation */

/* ============================================================
   RECOMMENDATION
   ============================================================ */

.recommendation-card {
    background: #ffffff;
    border: 1px solid #dfe7e1;
    border-radius: 15px;
    padding: 23px 25px;
    box-shadow: 0 2px 10px rgba(20, 35, 28, 0.035);
    border: 1px solid #d6e4da;
    border-radius: 18px;
    padding: 32px 34px;
    min-height: 250px;
    box-shadow: 0 8px 28px rgba(30,70,48,0.08);
}

.recommendation-tag {
    color: #2e8158;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}

.recommendation-title {
    color: #17231d;
    font-size: 22px;
    font-size: 30px;
    line-height: 1.15;
    font-weight: 700;
    margin-top: 7px;
    margin-top: 12px;
    margin-bottom: 14px;
}

.recommendation-text {
    color: #5f6c64;
    font-size: 13px;
    line-height: 1.6;
    margin-top: 9px;
    font-size: 14px;
    line-height: 1.7;
}

/* Fingerprint */

.fingerprint-card {
    background: white;
    border: 1px solid #e1e6e2;
    border-radius: 11px;
    padding: 14px 17px;
    margin-bottom: 7px;
.recommendation-highlight {
    background: #edf7f0;
    border-radius: 10px;
    padding: 11px 13px;
    margin-top: 18px;
    color: #397052;
    font-size: 12px;
}

.fingerprint-name {
    font-size: 13px;
    font-weight: 600;
    color: #28342d;
}

.fingerprint-value {
    float: right;
/* ============================================================
   DECISION BOX
   ============================================================ */

.decision-box {
    background: #f0f4f1;
    border: 1px solid #dce5df;
    border-radius: 13px;
    padding: 18px 20px;
    color: #5c6961;
    font-size: 12px;
    font-weight: 600;
    color: #718078;
    line-height: 1.6;
}

/* Simulator */

/* ============================================================
   SIMULATOR
   ============================================================ */

.simulator-card {
    background: white;
    border: 1px solid #dfe5e1;
    border-radius: 15px;
    padding: 23px;
    box-shadow: 0 2px 10px rgba(20, 35, 28, 0.035);
    box-shadow: 0 2px 10px rgba(20,35,28,0.035);
}

.before-number {
@@ -269,7 +278,10 @@
    margin-top: 2px;
}

/* Cost */

/* ============================================================
   COST
   ============================================================ */

.cost-card {
    background: white;
@@ -291,7 +303,10 @@
    font-weight: 700;
}

/* Info */

/* ============================================================
   INFO
   ============================================================ */

.info-box {
    background: #f0f4f1;
@@ -303,44 +318,21 @@
    line-height: 1.6;
}

/* Selectbox */

/* ============================================================
   SELECT
   ============================================================ */

div[data-baseweb="select"] > div {
    background: white !important;
    border: 1px solid #d7ded9 !important;
    border-radius: 9px !important;
}

/* Slider */

div[data-testid="stSlider"] {
    padding-top: 3px;
}

/* Buttons */

.stButton > button {
    border-radius: 9px;
    border: 1px solid #cdd7d0;
    background: white;
    color: #233029;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: #398a62;
    color: #28764f;
}

/* Expander */

[data-testid="stExpander"] {
    background: white;
    border: 1px solid #dfe5e1;
    border-radius: 12px;
}

/* Footer */
/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;
@@ -354,7 +346,7 @@


# ============================================================
# DATA
# LOCALITY DATA
# ============================================================

LOCALITIES = {
@@ -502,18 +494,36 @@

def normalize(value, minimum, maximum):

    result = ((value - minimum) / (maximum - minimum)) * 100
    result = (
        (value - minimum)
        / (maximum - minimum)
    ) * 100

    return max(0, min(100, result))
    return max(
        0,
        min(100, result)
    )


def calculate_risk(lst, ndvi, built, population):
def calculate_risk(
    lst,
    ndvi,
    built,
    population
):

    heat = normalize(lst, 30, 45)
    heat = normalize(
        lst,
        30,
        45
    )

    vegetation_deficit = max(
        0,
        min(100, 100 - ndvi * 100)
        min(
            100,
            100 - ndvi * 100
        )
    )

    risk = (
@@ -523,7 +533,10 @@ def calculate_risk(lst, ndvi, built, population):
        0.10 * population
    )

    return max(0, min(100, risk))
    return max(
        0,
        min(100, risk)
    )


# ============================================================
@@ -532,18 +545,33 @@ def calculate_risk(lst, ndvi, built, population):

def get_contributions(data):

    heat = normalize(data["lst"], 30, 45)
    heat = normalize(
        data["lst"],
        30,
        45
    )

    vegetation_deficit = max(
        0,
        min(100, 100 - data["ndvi"] * 100)
        min(
            100,
            100 - data["ndvi"] * 100
        )
    )

    return {
        "Surface Heat": 0.45 * heat,
        "Built-up Intensity": 0.25 * data["built"],
        "Vegetation Deficit": 0.20 * vegetation_deficit,
        "Population Exposure": 0.10 * data["population"]

        "Surface Heat":
            0.45 * heat,

        "Built-up Intensity":
            0.25 * data["built"],

        "Vegetation Deficit":
            0.20 * vegetation_deficit,

        "Population Exposure":
            0.10 * data["population"]
    }


@@ -596,7 +624,7 @@ def recommendation(data):


# ============================================================
# SIMULATION
# INTERVENTION SIMULATOR
# ============================================================

def simulate_intervention(
@@ -606,11 +634,17 @@ def simulate_intervention(
    shade_structures
):

    tree_effect = (trees / 2000.0) * 18.0
    tree_effect = (
        trees / 2000.0
    ) * 18.0

    roof_effect = (roof_area / 50000.0) * 14.0
    roof_effect = (
        roof_area / 50000.0
    ) * 14.0

    shade_effect = (shade_structures / 100.0) * 8.0
    shade_effect = (
        shade_structures / 100.0
    ) * 8.0

    reduction = (
        tree_effect +
@@ -632,7 +666,7 @@ def simulate_intervention(


# ============================================================
# RISK COLORS
# RISK COLOR
# ============================================================

def risk_color(risk):
@@ -653,7 +687,11 @@ def risk_color(risk):
# THERMAL FIELD
# ============================================================

def generate_thermal_points(lat, lon, risk):
def generate_thermal_points(
    lat,
    lon,
    risk
):

    points = []

@@ -664,20 +702,29 @@ def generate_thermal_points(lat, lon, risk):
        for x in range(-10, 11):

            distance = math.sqrt(
                x * x + y * y
                x * x +
                y * y
            )

            intensity = math.exp(
                -(distance ** 2) / 35
            )

            intensity *= risk / 100
            intensity *= (
                risk / 100
            )

            if intensity > 0.04:

                p_lat = lat + (y / 10) * radius
                p_lat = (
                    lat +
                    (y / 10) * radius
                )

                p_lon = lon + (x / 10) * radius
                p_lon = (
                    lon +
                    (x / 10) * radius
                )

                points.append([
                    p_lat,
@@ -689,13 +736,16 @@ def generate_thermal_points(lat, lon, risk):


# ============================================================
# MAIN LEAFLET MAP
# MAIN CHENNAI MAP
# ============================================================

def create_main_map(selected):

    m = folium.Map(
        location=[13.05, 80.22],
        location=[
            13.05,
            80.22
        ],
        zoom_start=11,
        tiles="OpenStreetMap",
        control_scale=True
@@ -728,6 +778,7 @@ def create_main_map(selected):
        max_zoom=13
    ).add_to(m)


    for name, location in LOCALITIES.items():

        location_risk = calculate_risk(
@@ -737,33 +788,51 @@ def create_main_map(selected):
            location["population"]
        )

        is_selected = name == selected
        is_selected = (
            name == selected
        )

        folium.CircleMarker(
            location=[
                location["lat"],
                location["lon"]
            ],
            radius=11 if is_selected else 6,
            radius=(
                11
                if is_selected
                else 6
            ),
            color="#ffffff",
            weight=2,
            fill=True,
            fill_color=risk_color(location_risk),
            fill_color=risk_color(
                location_risk
            ),
            fill_opacity=0.95,
            popup=folium.Popup(
                f"""
                <div style="font-family:Arial;min-width:180px;">
                    <b style="font-size:16px;">{name}</b>
                    <b style="font-size:16px;">
                    {name}
                    </b>

                    <br><br>

                    Heat Risk:
                    <b>{location_risk:.1f}/100</b>

                    <br>

                    Surface Temperature:
                    {location["lst"]:.1f}°C

                    <br>

                    Built-up:
                    {location["built"]}%

                    <br>

                    NDVI:
                    {location["ndvi"]:.2f}
                </div>
@@ -896,25 +965,29 @@ def create_intervention_map(

<div class="legend-row">
<span class="dot"
style="background:#e54848"></span>
style="background:#e54848">
</span>
Critical
</div>

<div class="legend-row">
<span class="dot"
style="background:#f39a35"></span>
style="background:#f39a35">
</span>
High
</div>

<div class="legend-row">
<span class="dot"
style="background:#e7ca4d"></span>
style="background:#e7ca4d">
</span>
Moderate
</div>

<div class="legend-row">
<span class="dot"
style="background:#38b879"></span>
style="background:#38b879">
</span>
Low
</div>

@@ -931,10 +1004,7 @@ def create_intervention_map(


var map = L.map(
    "map",
    {
        zoomControl: true
    }
    "map"
).setView(
    [lat, lon],
    14
@@ -954,9 +1024,7 @@ def create_intervention_map(
).addTo(map);


// ---------------------------------------------------------
// LOCATION MARKER
// ---------------------------------------------------------
// LOCATION

L.circleMarker(
    [lat, lon],
@@ -976,9 +1044,7 @@ def create_intervention_map(
).addTo(map);


// ---------------------------------------------------------
// THERMAL FIELD
// ---------------------------------------------------------
// THERMAL CELLS

var cells = [];

@@ -995,36 +1061,46 @@ def create_intervention_map(
        x++
    ) {

        var distance = Math.sqrt(
            x * x + y * y
        );
        var distance =
            Math.sqrt(
                x * x +
                y * y
            );

        var strength = Math.exp(
            -(distance * distance) / 55
        );
        var strength =
            Math.exp(
                -(distance * distance)
                / 55
            );


        if (strength > 0.08) {

            var pointLat =
                lat + (y / 10) * 0.022;
                lat +
                (y / 10) * 0.022;

            var pointLon =
                lon + (x / 10) * 0.022;
                lon +
                (x / 10) * 0.022;


            var circle = L.circle(
                [pointLat, pointLon],
                {
            var circle =
                L.circle(
                    [
                        pointLat,
                        pointLon
                    ],
                    {

                    radius: 95,
                        radius: 95,

                    stroke: false,
                        stroke: false,

                    fillOpacity: 0.35
                        fillOpacity: 0.35

                }
            ).addTo(map);
                    }
                ).addTo(map);


            cells.push({
@@ -1042,9 +1118,7 @@ def create_intervention_map(
}


// ---------------------------------------------------------
// COLOR
// ---------------------------------------------------------
// COLORS

function getColor(risk) {

@@ -1071,9 +1145,7 @@ def create_intervention_map(
}


// ---------------------------------------------------------
// ANIMATION
// ---------------------------------------------------------

function animateMap() {

@@ -1092,7 +1164,8 @@ def create_intervention_map(


        var progress =
            (timestamp - start) / duration;
            (timestamp - start)
            / duration;


        if (progress > 1) {
@@ -1110,7 +1183,10 @@ def create_intervention_map(

        var currentRisk =
            beforeRisk +
            (afterRisk - beforeRisk) *
            (
                afterRisk -
                beforeRisk
            ) *
            eased;


@@ -1121,18 +1197,22 @@ def create_intervention_map(
                    currentRisk *
                    (
                        0.55 +
                        item.strength * 0.45
                        item.strength *
                        0.45
                    );


                item.circle.setStyle({

                    fillColor:
                        getColor(localRisk),
                        getColor(
                            localRisk
                        ),

                    fillOpacity:
                        0.18 +
                        item.strength * 0.35
                        item.strength *
                        0.35

                });

@@ -1142,14 +1222,18 @@ def create_intervention_map(

        if (progress < 1) {

            requestAnimationFrame(frame);
            requestAnimationFrame(
                frame
            );

        }

    }


    requestAnimationFrame(frame);
    requestAnimationFrame(
        frame
    );

}

@@ -1190,9 +1274,11 @@ def create_intervention_map(
# HEADER
# ============================================================

left, right = st.columns([4, 1])
header_left, header_right = st.columns(
    [4, 1]
)

with left:
with header_left:

    st.markdown(
        '<div class="eyebrow">'
@@ -1211,7 +1297,7 @@ def create_intervention_map(
    )


with right:
with header_right:

    st.markdown(
        """
@@ -1248,7 +1334,7 @@ def create_intervention_map(


# ============================================================
# LOCATION
# SELECT LOCATION
# ============================================================

st.markdown(
@@ -1258,7 +1344,11 @@ def create_intervention_map(
    unsafe_allow_html=True
)

location_col, status_col = st.columns([2.5, 1])

location_col, status_col = st.columns(
    [2.5, 1]
)


with location_col:

@@ -1268,6 +1358,7 @@ def create_intervention_map(
        label_visibility="collapsed"
    )


with status_col:

    st.markdown(
@@ -1289,7 +1380,7 @@ def create_intervention_map(


# ============================================================
# RISK
# CALCULATE
# ============================================================

risk = calculate_risk(
@@ -1299,9 +1390,13 @@ def create_intervention_map(
    data["population"]
)

contributions = get_contributions(data)
contributions = get_contributions(
    data
)

best_intervention, reason = recommendation(data)
best_intervention, reason = recommendation(
    data
)


# ============================================================
@@ -1448,7 +1543,11 @@ def create_intervention_map(
    unsafe_allow_html=True
)

map_title_col, map_info_col = st.columns([3, 1])

map_title_col, map_info_col = st.columns(
    [3, 1]
)


with map_title_col:

@@ -1473,6 +1572,7 @@ def create_intervention_map(
        unsafe_allow_html=True
    )


with map_info_col:

    st.markdown(
@@ -1490,7 +1590,9 @@ def create_intervention_map(
    )


main_map = create_main_map(selected)
main_map = create_main_map(
    selected
)


st_folium(
@@ -1508,19 +1610,25 @@ def create_intervention_map(

st.divider()


st.markdown(
    '<div class="eyebrow">'
    '03 · UNDERSTAND THE HOTSPOT'
    '</div>',
    unsafe_allow_html=True
)


diag_left, diag_right = st.columns(
    [1.05, 0.95],
    [1, 1.15],
    gap="large"
)


# ============================================================
# LEFT — HEAT FINGERPRINT
# ============================================================

with diag_left:

    st.markdown(
@@ -1537,7 +1645,7 @@ def create_intervention_map(
            color:#718078;
            font-size:13px;
            margin-top:3px;
            margin-bottom:17px;
            margin-bottom:18px;
        ">
        Contribution to the current Heat Risk Index
        </div>
@@ -1561,27 +1669,65 @@ def create_intervention_map(
            else 0
        )

        st.markdown(
            f"""
            <div class="fingerprint-card">
        # Native Streamlit layout.
        # No raw HTML here, so it cannot render as code.

        contribution_col1, contribution_col2 = st.columns(
            [4, 1]
        )

                <span class="fingerprint-name">

        with contribution_col1:

            st.markdown(
                f"""
                <div style="
                    font-size:13px;
                    font-weight:600;
                    color:#28342d;
                    padding-top:4px;
                ">
                {name}
                </span>
                </div>
                """,
                unsafe_allow_html=True
            )


                <span class="fingerprint-value">
        with contribution_col2:

            st.markdown(
                f"""
                <div style="
                    text-align:right;
                    font-size:12px;
                    font-weight:700;
                    color:#718078;
                    padding-top:4px;
                ">
                {percentage:.0f}%
                </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            min(1.0, value / 45)
            min(
                1.0,
                value / 45
            )
        )

        st.markdown(
            "<div style='height:5px'></div>",
            unsafe_allow_html=True
        )


# ============================================================
# RIGHT — BIG RECOMMENDATION
# ============================================================

with diag_right:

@@ -1590,7 +1736,7 @@ def create_intervention_map(
        <div class="recommendation-card">

        <div class="recommendation-tag">
        Recommended first action
        RECOMMENDED FIRST ACTION
        </div>

        <div class="recommendation-title">
@@ -1601,23 +1747,28 @@ def create_intervention_map(
        {reason}
        </div>

        <div class="recommendation-highlight">
        Selected because it addresses the largest
        contributor to this locality's current heat risk.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        "<div style='height:12px'></div>",
        "<div style='height:14px'></div>",
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="info-box">
        <div class="decision-box">

        <b>Decision logic</b><br>
        <b>Decision logic</b><br><br>

        HeatScape identifies the largest contributor
        to the locality's Heat Risk Index and uses it
@@ -1630,18 +1781,20 @@ def create_intervention_map(


# ============================================================
# SIMULATOR
# INTERVENTION SIMULATOR
# ============================================================

st.divider()


st.markdown(
    '<div class="eyebrow">'
    '04 · TEST AN INTERVENTION'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <div style="
@@ -1673,7 +1826,7 @@ def create_intervention_map(


# ============================================================
# CONTROLS
# SIMULATION CONTROLS
# ============================================================

with sim_left:
@@ -1699,6 +1852,7 @@ def create_intervention_map(
        Set the scale of each cooling measure.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )
@@ -1734,14 +1888,8 @@ def create_intervention_map(
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# SIMULATION RESULT
# SIMULATION CALCULATION
# ============================================================

predicted_risk, reduction = simulate_intervention(
@@ -1759,6 +1907,10 @@ def create_intervention_map(
)


# ============================================================
# SIMULATION RESULT
# ============================================================

with sim_right:

    st.markdown(
@@ -1772,6 +1924,8 @@ def create_intervention_map(
            margin-bottom:15px;
        ">
        Projected impact
        </div>

        </div>
        """,
        unsafe_allow_html=True
@@ -1835,8 +1989,6 @@ def create_intervention_map(
        {reduction_percent:.1f}% projected reduction
        </div>

        </div>

        </div>
        """,
        unsafe_allow_html=True
@@ -1925,13 +2077,15 @@ def create_intervention_map(
    unsafe_allow_html=True
)


st.markdown(
    '<div class="eyebrow">'
    '05 · WATCH THE CHANGE'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <div style="
@@ -1992,13 +2146,15 @@ def create_intervention_map(

st.divider()


st.markdown(
    '<div class="eyebrow">'
    '06 · COST OF IMPLEMENTATION'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <div style="
@@ -2022,6 +2178,8 @@ def create_intervention_map(
)


# COST ASSUMPTIONS

tree_install = trees * 650
tree_establishment = trees * 300
tree_maintenance = trees * 250
@@ -2151,7 +2309,9 @@ def create_intervention_map(
st.divider()


with st.expander("Methodology & data sources"):
with st.expander(
    "Methodology & data sources"
):

    st.markdown("""
### Heat Risk Index
