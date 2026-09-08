import streamlit as st
import folium
from streamlit_folium import st_folium

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="HeatScape | Chennai Climate Intelligence",
    page_icon="🌿",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0d1016;
    color: #f5f7fa;
}

/* Main width */
.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Headings */
h1 {
    font-size: 42px !important;
    font-weight: 700 !important;
    letter-spacing: -1px;
}

h2 {
    font-size: 26px !important;
    font-weight: 700 !important;
}

h3 {
    font-size: 20px !important;
}

/* Select box */
div[data-baseweb="select"] > div {
    background: #252832;
    border: 1px solid #30343f;
    border-radius: 12px;
    min-height: 48px;
}

/* Metric cards */
.metric-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 25px;
    min-height: 175px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.12);
}

.metric-label {
    color: #58708c;
    font-size: 15px;
    font-weight: 500;
    margin-bottom: 16px;
}

.metric-value {
    color: #171a21;
    font-size: 32px;
    font-weight: 700;
    line-height: 1.1;
}

.metric-small {
    color: #64748b;
    font-size: 14px;
    margin-top: 12px;
}

/* Recommendation */
.recommendation-card {
    background: linear-gradient(135deg, #effff5, #e5faed);
    border-radius: 22px;
    padding: 32px;
    margin-top: 10px;
    color: #17251c;
    border: 1px solid #ccebd8;
}

.recommendation-title {
    color: #557261;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.recommendation-main {
    color: #163a25;
    font-size: 32px;
    font-weight: 700;
    margin-top: 8px;
}

.recommendation-location {
    color: #486454;
    font-size: 16px;
    margin-top: 12px;
}

.recommendation-reason {
    color: #405548;
    font-size: 15px;
    margin-top: 18px;
    line-height: 1.6;
}

/* Fingerprint */
.fingerprint-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px;
    color: #171a21;
    box-shadow: 0 3px 12px rgba(0,0,0,0.10);
}

.fingerprint-name {
    color: #526b82;
    font-size: 14px;
    margin-bottom: 8px;
}

.fingerprint-score {
    color: #171a21;
    font-size: 25px;
    font-weight: 700;
}

/* Section label */
.section-note {
    color: #8995a6;
    font-size: 14px;
    margin-top: -8px;
    margin-bottom: 18px;
}

/* Implementation card */
.implementation-card {
    background: #171a21;
    border: 1px solid #292e38;
    border-radius: 18px;
    padding: 24px;
    min-height: 170px;
}

.implementation-title {
    color: #8fa0b4;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.implementation-value {
    color: #ffffff;
    font-size: 22px;
    font-weight: 700;
    margin-top: 8px;
}

.implementation-detail {
    color: #9da8b7;
    font-size: 14px;
    margin-top: 12px;
    line-height: 1.5;
}

/* Technique list */
.technique-card {
    background: #171a21;
    border: 1px solid #292e38;
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 10px;
}

.technique-name {
    color: #ffffff;
    font-weight: 600;
    font-size: 15px;
}

.technique-category {
    color: #8c9aaa;
    font-size: 13px;
    margin-top: 4px;
}

/* Footer */
.footer {
    text-align: center;
    color: #657181;
    font-size: 13px;
    padding-top: 40px;
    padding-bottom: 20px;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    border: 1px solid #313641;
}

/* Slider */
div[data-baseweb="slider"] {
    padding-top: 10px;
}

/* Divider */
hr {
    border-color: #272c35 !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# CHENNAI LOCALITY DATA
# Prototype / representative values
# =========================================================

LOCATIONS = {

    "Washermanpet": {
        "lat": 13.1158,
        "lon": 80.2875,
        "lst": 41.2,
        "ndvi": 0.18,
        "built": 84,
        "population": 82,
        "roads": [
            {
                "name": "Mint Street Corridor",
                "space": 1550,
                "trees": 125,
                "lat": 13.1165,
                "lon": 80.2878
            },
            {
                "name": "Moolakadai Road",
                "space": 1100,
                "trees": 90,
                "lat": 13.1190,
                "lon": 80.2860
            }
        ],
        "open_spaces": [
            {
                "name": "Local Community Open Space",
                "area": 1200,
                "lat": 13.1150,
                "lon": 80.2890
            }
        ]
    },

    "Royapuram": {
        "lat": 13.1155,
        "lon": 80.2940,
        "lst": 40.8,
        "ndvi": 0.21,
        "built": 81,
        "population": 78,
        "roads": [
            {
                "name": "Royapuram High Road",
                "space": 1700,
                "trees": 135,
                "lat": 13.1148,
                "lon": 80.2925
            }
        ],
        "open_spaces": [
            {
                "name": "Royapuram Community Space",
                "area": 2400,
                "lat": 13.1170,
                "lon": 80.2950
            }
        ]
    },

    "Perambur": {
        "lat": 13.1198,
        "lon": 80.2336,
        "lst": 41.0,
        "ndvi": 0.24,
        "built": 78,
        "population": 76,
        "roads": [
            {
                "name": "Perambur High Road",
                "space": 2100,
                "trees": 170,
                "lat": 13.1210,
                "lon": 80.2340
            }
        ],
        "open_spaces": [
            {
                "name": "Perambur Green Space",
                "area": 3000,
                "lat": 13.1180,
                "lon": 80.2320
            }
        ]
    },

    "Ambattur": {
        "lat": 13.1143,
        "lon": 80.1548,
        "lst": 40.2,
        "ndvi": 0.28,
        "built": 73,
        "population": 69,
        "roads": [
            {
                "name": "Ambattur Industrial Road",
                "space": 2600,
                "trees": 210,
                "lat": 13.1150,
                "lon": 80.1555
            }
        ],
        "open_spaces": [
            {
                "name": "Ambattur Open Area",
                "area": 5200,
                "lat": 13.1130,
                "lon": 80.1530
            }
        ]
    },

    "Avadi": {
        "lat": 13.1147,
        "lon": 80.1018,
        "lst": 39.1,
        "ndvi": 0.38,
        "built": 62,
        "population": 63,
        "roads": [
            {
                "name": "Avadi Main Road",
                "space": 3000,
                "trees": 240,
                "lat": 13.1150,
                "lon": 80.1025
            }
        ],
        "open_spaces": [
            {
                "name": "Avadi Green Area",
                "area": 6500,
                "lat": 13.1130,
                "lon": 80.1000
            }
        ]
    },

    "Anna Nagar": {
        "lat": 13.0850,
        "lon": 80.2101,
        "lst": 38.4,
        "ndvi": 0.42,
        "built": 70,
        "population": 64,
        "roads": [
            {
                "name": "2nd Avenue",
                "space": 2200,
                "trees": 175,
                "lat": 13.0845,
                "lon": 80.2110
            }
        ],
        "open_spaces": [
            {
                "name": "Anna Nagar Open Space",
                "area": 3500,
                "lat": 13.0860,
                "lon": 80.2090
            }
        ]
    },

    "Nungambakkam": {
        "lat": 13.0569,
        "lon": 80.2425,
        "lst": 39.2,
        "ndvi": 0.34,
        "built": 76,
        "population": 68,
        "roads": [
            {
                "name": "College Road",
                "space": 1800,
                "trees": 145,
                "lat": 13.0575,
                "lon": 80.2430
            }
        ],
        "open_spaces": [
            {
                "name": "Nungambakkam Green Space",
                "area": 2800,
                "lat": 13.0560,
                "lon": 80.2410
            }
        ]
    },

    "T Nagar": {
        "lat": 13.0418,
        "lon": 80.2341,
        "lst": 40.0,
        "ndvi": 0.22,
        "built": 87,
        "population": 74,
        "roads": [
            {
                "name": "Usman Road Corridor",
                "space": 1900,
                "trees": 150,
                "lat": 13.0420,
                "lon": 80.2350
            }
        ],
        "open_spaces": [
            {
                "name": "T Nagar Community Space",
                "area": 1800,
                "lat": 13.0405,
                "lon": 80.2330
            }
        ]
    },

    "Mylapore": {
        "lat": 13.0339,
        "lon": 80.2676,
        "lst": 38.8,
        "ndvi": 0.35,
        "built": 72,
        "population": 66,
        "roads": [
            {
                "name": "R K Mutt Road",
                "space": 2000,
                "trees": 160,
                "lat": 13.0345,
                "lon": 80.2680
            }
        ],
        "open_spaces": [
            {
                "name": "Mylapore Open Space",
                "area": 4200,
                "lat": 13.0325,
                "lon": 80.2660
            }
        ]
    },

    "Guindy": {
        "lat": 13.0067,
        "lon": 80.2206,
        "lst": 39.5,
        "ndvi": 0.39,
        "built": 68,
        "population": 58,
        "roads": [
            {
                "name": "Guindy Industrial Corridor",
                "space": 3200,
                "trees": 255,
                "lat": 13.0070,
                "lon": 80.2210
            }
        ],
        "open_spaces": [
            {
                "name": "Guindy Green Area",
                "area": 7000,
                "lat": 13.0050,
                "lon": 80.2190
            }
        ]
    },

    "Adyar": {
        "lat": 13.0063,
        "lon": 80.2574,
        "lst": 37.9,
        "ndvi": 0.51,
        "built": 61,
        "population": 55,
        "roads": [
            {
                "name": "LB Road",
                "space": 2400,
                "trees": 190,
                "lat": 13.0070,
                "lon": 80.2580
            }
        ],
        "open_spaces": [
            {
                "name": "Adyar Green Corridor",
                "area": 6500,
                "lat": 13.0050,
                "lon": 80.2560
            }
        ]
    },

    "Velachery": {
        "lat": 12.9815,
        "lon": 80.2180,
        "lst": 40.1,
        "ndvi": 0.25,
        "built": 79,
        "population": 73,
        "roads": [
            {
                "name": "Velachery Main Road",
                "space": 2500,
                "trees": 200,
                "lat": 12.9820,
                "lon": 80.2190
            }
        ],
        "open_spaces": [
            {
                "name": "Velachery Open Space",
                "area": 4000,
                "lat": 12.9800,
                "lon": 80.2170
            }
        ]
    },

    "Perungudi": {
        "lat": 12.9591,
        "lon": 80.2400,
        "lst": 39.8,
        "ndvi": 0.30,
        "built": 75,
        "population": 61,
        "roads": [
            {
                "name": "OMR Service Road",
                "space": 3500,
                "trees": 280,
                "lat": 12.9600,
                "lon": 80.2410
            }
        ],
        "open_spaces": [
            {
                "name": "Perungudi Green Space",
                "area": 5500,
                "lat": 12.9580,
                "lon": 80.2390
            }
        ]
    },

    "Sholinganallur": {
        "lat": 12.9010,
        "lon": 80.2279,
        "lst": 40.4,
        "ndvi": 0.27,
        "built": 77,
        "population": 70,
        "roads": [
            {
                "name": "Sholinganallur OMR Corridor",
                "space": 4200,
                "trees": 335,
                "lat": 12.9020,
                "lon": 80.2290
            }
        ],
        "open_spaces": [
            {
                "name": "Sholinganallur Open Area",
                "area": 6000,
                "lat": 12.9000,
                "lon": 80.2260
            }
        ]
    },

    "Tambaram": {
        "lat": 12.9249,
        "lon": 80.1000,
        "lst": 39.4,
        "ndvi": 0.40,
        "built": 64,
        "population": 65,
        "roads": [
            {
                "name": "Tambaram Main Road",
                "space": 2800,
                "trees": 225,
                "lat": 12.9255,
                "lon": 80.1010
            }
        ],
        "open_spaces": [
            {
                "name": "Tambaram Green Area",
                "area": 5000,
                "lat": 12.9230,
                "lon": 80.0990
            }
        ]
    }
}

# =========================================================
# FUNCTIONS
# =========================================================

def normalize(value, minimum, maximum):
    if maximum == minimum:
        return 0

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


def get_contributions(data):

    heat = normalize(
        data["lst"],
        30,
        45
    )

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


def risk_category(risk):

    if risk >= 75:
        return "Critical", "🔴"

    if risk >= 50:
        return "High", "🟠"

    if risk >= 25:
        return "Moderate", "🟡"

    return "Low", "🟢"


def find_best_tree_road(data):

    roads = data.get("roads", [])

    if not roads:
        return None

    return max(
        roads,
        key=lambda x: x.get("space", 0)
    )


def find_best_open_space(data):

    spaces = data.get("open_spaces", [])

    if not spaces:
        return None

    return max(
        spaces,
        key=lambda x: x.get("area", 0)
    )


def determine_intervention(data):

    contributions = get_contributions(data)

    dominant = max(
        contributions,
        key=contributions.get
    )

    best_road = find_best_tree_road(data)
    best_space = find_best_open_space(data)

    if dominant == "Vegetation Deficit":

        if best_space and best_space["area"] >= 2500:
            return {
                "type": "Urban Forests & Trees",
                "reason": "Vegetation deficit is the strongest contributor to heat risk, and suitable open space is available.",
                "location": best_space["name"],
                "quantity": min(
                    int(best_space["area"] / 20),
                    500
                ),
                "unit": "trees",
                "space": best_space["area"],
                "lat": best_space["lat"],
                "lon": best_space["lon"]
            }

        if best_road:
            return {
                "type": "Urban Forests & Trees",
                "reason": "Low vegetation is a major contributor, so roadside tree planting can increase shade and canopy cover.",
                "location": best_road["name"],
                "quantity": best_road["trees"],
                "unit": "trees",
                "space": best_road["space"],
                "lat": best_road["lat"],
                "lon": best_road["lon"]
            }

    if dominant == "Built-up Intensity":

        suitable_roof_area = data["built"] * 1000

        return {
            "type": "Reflective Cool Roofs",
            "reason": "High built-up intensity is the strongest contributor, so reflective roof treatment is the most targeted first action.",
            "location": f"{data.get('name', 'Selected locality')} buildings",
            "quantity": int(suitable_roof_area * 0.50),
            "unit": "m²",
            "space": suitable_roof_area,
            "lat": data["lat"],
            "lon": data["lon"]
        }

    if dominant == "Surface Heat":

        if best_road:
            return {
                "type": "Green + Shade Corridor",
                "reason": "Surface heat is the dominant contributor and a suitable roadside corridor is available for combined shade and vegetation.",
                "location": best_road["name"],
                "quantity": best_road["space"],
                "unit": "m²",
                "space": best_road["space"],
                "lat": best_road["lat"],
                "lon": best_road["lon"]
            }

    if dominant == "Population Exposure":

        if best_space and best_space["area"] >= 2000:
            return {
                "type": "Pocket Parks",
                "reason": "High population exposure makes accessible cooling space a priority.",
                "location": best_space["name"],
                "quantity": best_space["area"],
                "unit": "m²",
                "space": best_space["area"],
                "lat": best_space["lat"],
                "lon": best_space["lon"]
            }

    if best_space and best_space["area"] >= 3500:
        return {
            "type": "Blue Infrastructure",
            "reason": "Available open space provides an opportunity for blue-green cooling infrastructure.",
            "location": best_space["name"],
            "quantity": best_space["area"],
            "unit": "m²",
            "space": best_space["area"],
            "lat": best_space["lat"],
            "lon": best_space["lon"]
        }

    if best_road and best_road["space"] >= 1500:
        return {
            "type": "Reflective Pavements",
            "reason": "Suitable road space is available for a reflective pavement intervention.",
            "location": best_road["name"],
            "quantity": best_road["space"],
            "unit": "m²",
            "space": best_road["space"],
            "lat": best_road["lat"],
            "lon": best_road["lon"]
        }

    if best_road:
        return {
            "type": "Shaded Pedestrian Corridors",
            "reason": "Roadside space is available for a targeted pedestrian cooling corridor.",
            "location": best_road["name"],
            "quantity": best_road["space"],
            "unit": "m²",
            "space": best_road["space"],
            "lat": best_road["lat"],
            "lon": best_road["lon"]
        }

    return {
        "type": "Targeted Cooling Corridor",
        "reason": "A combined cooling intervention should be assessed using detailed site-level GIS data.",
        "location": "Selected hotspot",
        "quantity": 1000,
        "unit": "m²",
        "space": 1000,
        "lat": data["lat"],
        "lon": data["lon"]
    }


def simulate_intervention(
    original_risk,
    intervention_type,
    quantity,
    suitable_area=0,
    lst=40
):

    reduction = 0

    if intervention_type == "Urban Forests & Trees":
        reduction = (quantity / 2000) * 18

    elif intervention_type == "Pocket Parks":
        reduction = (quantity / 5000) * 22

    elif intervention_type == "Blue Infrastructure":
        reduction = (quantity / 5000) * 18

    elif intervention_type == "Green + Shade Corridor":
        reduction = (quantity / 2000) * 20

    elif intervention_type == "Shaded Pedestrian Corridors":
        reduction = (quantity / 2000) * 12

    elif intervention_type == "Reflective Pavements":
        reduction = (quantity / 10000) * 8

    elif intervention_type == "Reflective Cool Roofs":

        if suitable_area > 0:

            coverage = min(
                quantity / suitable_area,
                1
            )

            heat_component = (
                normalize(lst, 30, 45) * 0.45
            )

            # Modelled reduction in heat-risk contribution
            reduction = (
                heat_component *
                0.20 *
                coverage
            )

    elif intervention_type == "Targeted Cooling Corridor":
        reduction = (quantity / 2000) * 10

    reduction = min(
        reduction,
        original_risk * 0.75
    )

    new_risk = max(
        0,
        original_risk - reduction
    )

    return new_risk, reduction


def calculate_cost(
    intervention_type,
    quantity
):

    prices = {

        "Urban Forests & Trees": {
            "install": 650,
            "establishment": 300,
            "maintenance": 250
        },

        "Pocket Parks": {
            "install": 1600,
            "establishment": 0,
            "maintenance": 100
        },

        "Blue Infrastructure": {
            "install": 1200,
            "establishment": 0,
            "maintenance": 80
        },

        "Reflective Cool Roofs": {
            "install": 300,
            "establishment": 0,
            "maintenance": 30
        },

        "Reflective Pavements": {
            "install": 400,
            "establishment": 0,
            "maintenance": 25
        },

        "Green + Shade Corridor": {
            "install": 650,
            "establishment": 250,
            "maintenance": 150
        },

        "Shaded Pedestrian Corridors": {
            "install": 650,
            "establishment": 250,
            "maintenance": 150
        },

        "Targeted Cooling Corridor": {
            "install": 650,
            "establishment": 250,
            "maintenance": 150
        }
    }

    p = prices.get(
        intervention_type,
        prices["Targeted Cooling Corridor"]
    )

    initial_cost = (
        quantity *
        (p["install"] + p["establishment"])
    )

    annual_maintenance = (
        quantity *
        p["maintenance"]
    )

    five_year_cost = (
        initial_cost +
        annual_maintenance * 5
    )

    return (
        initial_cost,
        annual_maintenance,
        five_year_cost
    )


def format_currency(value):

    return f"₹{value:,.0f}"


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<h1 style="margin-bottom:0;">HeatScape</h1>

<p style="
color:#91a0b2;
font-size:16px;
margin-top:4px;
margin-bottom:28px;
">
Climate Intelligence · Chennai
</p>
""", unsafe_allow_html=True)


# =========================================================
# LOCATION SELECTOR
# =========================================================

selected_location = st.selectbox(
    "Select Location",
    list(LOCATIONS.keys())
)

data = LOCATIONS[selected_location].copy()

# Add name so recommendation logic can use it
data["name"] = selected_location

risk = calculate_risk(
    data["lst"],
    data["ndvi"],
    data["built"],
    data["population"]
)

category, category_icon = risk_category(risk)

contributions = get_contributions(data)

recommendation = determine_intervention(data)


# =========================================================
# CURRENT CONDITIONS
# =========================================================

st.markdown("## Current Conditions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Heat Risk</div>
        <div class="metric-value">{risk:.0f}/100</div>
        <div class="metric-small">{category_icon} {category}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Surface Temperature</div>
        <div class="metric-value">{data["lst"]:.1f}°C</div>
        <div class="metric-small">Surface heat variable</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Vegetation</div>
        <div class="metric-value">{data["ndvi"]:.2f}</div>
        <div class="metric-small">NDVI</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Built-up Area</div>
        <div class="metric-value">{data["built"]}%</div>
        <div class="metric-small">Built-up intensity</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# AVAILABLE SPACE
# =========================================================

best_road = find_best_tree_road(data)
best_space = find_best_open_space(data)

road_space = best_road["space"] if best_road else 0
tree_capacity = best_road["trees"] if best_road else 0
open_space = best_space["area"] if best_space else 0

st.markdown("## Available Implementation Space")

st.markdown("""
<p class="section-note">
Estimated spaces where cooling interventions could potentially be implemented.
</p>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Roadside Space</div>
        <div class="metric-value">{road_space:,} m²</div>
        <div class="metric-small">Candidate corridors</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Tree Capacity</div>
        <div class="metric-value">{tree_capacity}</div>
        <div class="metric-small">Estimated roadside capacity</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Open Space</div>
        <div class="metric-value">{open_space:,} m²</div>
        <div class="metric-small">Candidate green-space sites</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# MAIN HEAT MAP
# =========================================================

st.markdown("## Chennai Heat Map")

st.markdown("""
<p class="section-note">
Interactive spatial view of estimated heat-risk intensity across selected Chennai localities.
</p>
""", unsafe_allow_html=True)

heat_map = folium.Map(
    location=[13.05, 80.22],
    zoom_start=11,
    tiles="OpenStreetMap",
    control_scale=True
)

# Add locality markers
for name, location_data in LOCATIONS.items():

    location_risk = calculate_risk(
        location_data["lst"],
        location_data["ndvi"],
        location_data["built"],
        location_data["population"]
    )

    if location_risk >= 75:
        marker_color = "red"
    elif location_risk >= 50:
        marker_color = "orange"
    elif location_risk >= 25:
        marker_color = "beige"
    else:
        marker_color = "green"

    folium.CircleMarker(
        location=[
            location_data["lat"],
            location_data["lon"]
        ],
        radius=12,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.65,
        popup=folium.Popup(
            f"""
            <b>{name}</b><br>
            Heat Risk: {location_risk:.0f}/100<br>
            Surface Temperature: {location_data["lst"]:.1f}°C<br>
            NDVI: {location_data["ndvi"]:.2f}<br>
            Built-up: {location_data["built"]}%
            """,
            max_width=300
        )
    ).add_to(heat_map)

# Selected locality
folium.Marker(
    [data["lat"], data["lon"]],
    popup=f"<b>{selected_location}</b><br>Risk: {risk:.0f}/100",
    tooltip=f"{selected_location} · Risk {risk:.0f}/100"
).add_to(heat_map)

st_folium(
    heat_map,
    width=None,
    height=500,
    returned_objects=[],
    key=f"heatmap_{selected_location}"
)


# =========================================================
# HEAT FINGERPRINT
# =========================================================

st.markdown("## Heat Fingerprint")

st.markdown("""
<p class="section-note">
What is driving the heat risk at this location?
</p>
""", unsafe_allow_html=True)

sorted_contributions = sorted(
    contributions.items(),
    key=lambda x: x[1],
    reverse=True
)

cols = st.columns(4)

for i, (name, value) in enumerate(sorted_contributions):

    with cols[i]:

        st.markdown(f"""
        <div class="fingerprint-card">
            <div class="fingerprint-name">{name}</div>
            <div class="fingerprint-score">{value:.1f}</div>
            <div style="
                color:#7b8796;
                font-size:12px;
                margin-top:4px;
            ">
                Risk contribution
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(
            min(value / 100, 1.0)
        )


# =========================================================
# RECOMMENDED ACTION
# =========================================================

st.markdown("## Recommended First Action")

st.markdown(f"""
<div class="recommendation-card">

    <div class="recommendation-title">
        Recommended Technique
    </div>

    <div class="recommendation-main">
        {recommendation["type"]}
    </div>

    <div class="recommendation-location">
        📍 {recommendation["location"]}
    </div>

    <div class="recommendation-reason">
        {recommendation["reason"]}
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# CANDIDATE IMPLEMENTATION LOCATIONS
# =========================================================

st.markdown("## Candidate Implementation Locations")

location_cols = st.columns(2)

with location_cols[0]:

    if best_road:

        st.markdown(f"""
        <div class="implementation-card">

            <div class="implementation-title">
                Roadside Opportunity
            </div>

            <div class="implementation-value">
                {best_road["name"]}
            </div>

            <div class="implementation-detail">
                Estimated available space:
                <b>{best_road["space"]:,} m²</b><br><br>

                Estimated tree capacity:
                <b>{best_road["trees"]}</b> trees
            </div>

        </div>
        """, unsafe_allow_html=True)

with location_cols[1]:

    if best_space:

        st.markdown(f"""
        <div class="implementation-card">

            <div class="implementation-title">
                Open-Space Opportunity
            </div>

            <div class="implementation-value">
                {best_space["name"]}
            </div>

            <div class="implementation-detail">
                Estimated available area:
                <b>{best_space["area"]:,} m²</b><br><br>

                Potential for parks,
                trees or blue-green infrastructure.
            </div>

        </div>
        """, unsafe_allow_html=True)


# =========================================================
# TEST INTERVENTION
# =========================================================

st.markdown("## Test the Intervention")

st.markdown("""
<p class="section-note">
Adjust the implementation scale and see the projected effect on the Heat Risk Index.
</p>
""", unsafe_allow_html=True)

technique = recommendation["type"]

# Different sliders based on technique

if technique == "Urban Forests & Trees":

    max_value = max(
        50,
        min(
            500,
            tree_capacity
        )
    )

    quantity = st.slider(
        "Number of trees",
        min_value=10,
        max_value=max_value,
        value=min(100, max_value),
        step=10
    )

    quantity_unit = "trees"
    suitable_area = 0

elif technique == "Reflective Cool Roofs":

    suitable_area = int(
        data["built"] * 1000
    )

    max_value = max(
        1000,
        suitable_area
    )

    default_value = min(
        int(suitable_area * 0.50),
        max_value
    )

    quantity = st.slider(
        "Reflective roof area",
        min_value=500,
        max_value=max_value,
        value=max(500, default_value),
        step=500
    )

    quantity_unit = "m²"

elif technique in [
    "Pocket Parks",
    "Blue Infrastructure"
]:

    suitable_area = open_space

    max_value = max(
        1000,
        open_space
    )

    quantity = st.slider(
        "Implementation area",
        min_value=500,
        max_value=max_value,
        value=min(
            max(1000, int(open_space * 0.5)),
            max_value
        ),
        step=500
    )

    quantity_unit = "m²"

else:

    suitable_area = road_space

    max_value = max(
        1000,
        road_space
    )

    quantity = st.slider(
        "Implementation area",
        min_value=500,
        max_value=max_value,
        value=min(
            max(1000, int(road_space * 0.5)),
            max_value
        ),
        step=500
    )

    quantity_unit = "m²"


# =========================================================
# SIMULATION
# =========================================================

new_risk, reduction = simulate_intervention(
    original_risk=risk,
    intervention_type=technique,
    quantity=quantity,
    suitable_area=suitable_area,
    lst=data["lst"]
)

risk_difference = risk - new_risk

st.markdown("### Projected Impact")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
            Current Heat Risk
        </div>

        <div class="metric-value">
            {risk:.0f}/100
        </div>

        <div class="metric-small">
            Before intervention
        </div>

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
            Projected Heat Risk
        </div>

        <div class="metric-value">
            {new_risk:.1f}/100
        </div>

        <div class="metric-small">
            After intervention
        </div>

    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
            Modelled Reduction
        </div>

        <div class="metric-value">
            {risk_difference:.1f}
        </div>

        <div class="metric-small">
            Heat Risk Index points
        </div>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# BEFORE / AFTER BAR
# =========================================================

st.markdown("### Before → After")

st.progress(
    min(risk / 100, 1.0),
    text=f"Before · {risk:.0f}/100"
)

st.progress(
    min(new_risk / 100, 1.0),
    text=f"After · {new_risk:.1f}/100"
)


# =========================================================
# IMPLEMENTATION PLAN
# =========================================================

st.markdown("## Implementation Plan")

st.markdown(f"""
<div class="recommendation-card">

    <div class="recommendation-title">
        Selected Technique
    </div>

    <div class="recommendation-main">
        {technique}
    </div>

    <div class="recommendation-location">
        📍 {recommendation["location"]}
    </div>

    <div class="recommendation-reason">

        <b>Implementation scale:</b>
        {quantity:,.0f} {quantity_unit}

        <br><br>

        <b>Projected Heat Risk:</b>
        {risk:.0f} → {new_risk:.1f}

        <br><br>

        <b>Modelled reduction:</b>
        {risk_difference:.1f} Heat Risk Index points

    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# INTERVENTION MAP
# =========================================================

st.markdown("## Intervention Impact Map")

st.markdown("""
<p class="section-note">
Selected hotspot and candidate implementation location.
</p>
""", unsafe_allow_html=True)

intervention_map = folium.Map(
    location=[
        data["lat"],
        data["lon"]
    ],
    zoom_start=14,
    tiles="OpenStreetMap"
)

# Hotspot
folium.CircleMarker(
    [
        data["lat"],
        data["lon"]
    ],
    radius=18,
    color="red",
    fill=True,
    fill_color="red",
    fill_opacity=0.25,
    popup=f"Current Heat Risk: {risk:.0f}/100"
).add_to(intervention_map)

# Recommendation
folium.Marker(
    [
        recommendation["lat"],
        recommendation["lon"]
    ],
    popup=f"""
    <b>{recommendation["type"]}</b><br>
    {recommendation["location"]}<br>
    Scale: {quantity:,.0f} {quantity_unit}<br>
    Projected Risk: {new_risk:.1f}/100
    """,
    tooltip=recommendation["type"],
    icon=folium.Icon(
        color="green",
        icon="leaf"
    )
).add_to(intervention_map)

# Candidate roads
for road in data.get("roads", []):

    folium.CircleMarker(
        [
            road["lat"],
            road["lon"]
        ],
        radius=7,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.7,
        popup=f"""
        <b>{road["name"]}</b><br>
        Roadside space: {road["space"]:,} m²<br>
        Tree capacity: {road["trees"]}
        """
    ).add_to(intervention_map)

# Candidate open spaces
for space in data.get("open_spaces", []):

    folium.CircleMarker(
        [
            space["lat"],
            space["lon"]
        ],
        radius=8,
        color="green",
        fill=True,
        fill_color="green",
        fill_opacity=0.65,
        popup=f"""
        <b>{space["name"]}</b><br>
        Estimated area: {space["area"]:,} m²
        """
    ).add_to(intervention_map)

st_folium(
    intervention_map,
    width=None,
    height=500,
    returned_objects=[],
    key=f"intervention_{selected_location}"
)


# =========================================================
# COST
# =========================================================

st.markdown("## Cost of Implementation")

initial_cost, annual_maintenance, five_year_cost = calculate_cost(
    technique,
    quantity
)

cost_col1, cost_col2, cost_col3 = st.columns(3)

with cost_col1:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
            Initial Implementation
        </div>

        <div class="metric-value">
            {format_currency(initial_cost)}
        </div>

        <div class="metric-small">
            Installation + establishment
        </div>

    </div>
    """, unsafe_allow_html=True)

with cost_col2:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
            Annual Maintenance
        </div>

        <div class="metric-value">
            {format_currency(annual_maintenance)}
        </div>

        <div class="metric-small">
            Estimated yearly cost
        </div>

    </div>
    """, unsafe_allow_html=True)

with cost_col3:

    st.markdown(f"""
    <div class="metric-card">

        <div class="metric-label">
            5-Year Lifecycle Cost
        </div>

        <div class="metric-value">
            {format_currency(five_year_cost)}
        </div>

        <div class="metric-small">
            Implementation + 5 years maintenance
        </div>

    </div>
    """, unsafe_allow_html=True)


st.caption(
    "Planning estimate only. Actual implementation costs vary by site, "
    "procurement rates, materials and maintenance requirements."
)


# =========================================================
# COOLING TECHNIQUES
# =========================================================

st.markdown("## Cooling Techniques")

techniques = [
    (
        "Urban Forests & Trees",
        "Nature-based"
    ),
    (
        "Green Corridors",
        "Nature-based"
    ),
    (
        "Pocket Parks",
        "Nature-based"
    ),
    (
        "Blue Infrastructure",
        "Nature-based"
    ),
    (
        "Reflective Cool Roofs",
        "Reflective materials"
    ),
    (
        "Reflective Pavements",
        "Reflective materials"
    ),
    (
        "Shaded Pedestrian Corridors",
        "Smart planning"
    ),
    (
        "Green + Shade Corridors",
        "Smart planning"
    )
]

for technique_name, category_name in techniques:

    st.markdown(f"""
    <div class="technique-card">

        <div class="technique-name">
            {technique_name}
        </div>

        <div class="technique-category">
            {category_name}
        </div>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# METHODOLOGY
# =========================================================

st.markdown("## Methodology & Data Sources")

with st.expander("How HeatScape works"):

    st.markdown("""
### 1. Environmental and demographic inputs

HeatScape combines:

- **Landsat 8/9** → Surface Land Temperature
- **Sentinel-2** → NDVI / vegetation
- **ESA WorldCover** → Land-cover / built-up information
- **WorldPop** → Population exposure
- **OpenStreetMap / municipal GIS** → Roads and geographic context

### 2. Heat Risk Index

The prototype calculates:

**Heat Risk =**

`0.45 × Heat + 0.25 × Built-up + 0.20 × Vegetation Deficit + 0.10 × Population Exposure`

Each factor is normalized to a 0–100 scale.

### 3. Heat Fingerprint

The system calculates the contribution of each factor to the final risk score.

This makes the recommendation explainable.

### 4. Intervention selection

The recommendation engine identifies the dominant contributor and checks available implementation space.

For example:

**High vegetation deficit**
→ Urban Forests & Trees

**High built-up intensity**
→ Reflective Cool Roofs

**High surface heat + roadside space**
→ Green + Shade Corridor

### 5. Intervention simulation

The simulator estimates how the selected intervention could reduce the **Heat Risk Index**.

This is a modelled scenario, not a claim of exact physical temperature reduction.

### 6. Cost

Estimated lifecycle cost is calculated using:

`Quantity × Unit Cost`

The prototype includes installation and maintenance assumptions.

### Important data note

The current hackathon interface uses representative locality values to demonstrate the complete workflow.

The production version would replace these values with processed satellite-derived and municipal GIS data at the appropriate spatial resolution.

Available space values are also prototype estimates and should be verified using detailed GIS, cadastral and municipal datasets before real-world implementation.
""")


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

HeatScape · Urban Heat Reduction Planner<br>
Decision support for cooler, greener and more resilient Chennai

</div>
""", unsafe_allow_html=True)
