import streamlit as st
import folium
from streamlit_folium import st_folium

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HeatScape",
    page_icon="🌿",
    layout="wide"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

h1 {
    font-size: 38px !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 28px !important;
    font-weight: 700 !important;
    margin-top: 30px;
}

h3 {
    font-size: 20px !important;
    font-weight: 600 !important;
}

.metric-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 20px;
    min-height: 125px;
}

.metric-label {
    color: #6b7280;
    font-size: 14px;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 30px;
    font-weight: 700;
    color: #111827;
}

.metric-small {
    color: #6b7280;
    font-size: 13px;
    margin-top: 5px;
}

.recommendation {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 18px;
    padding: 28px;
    margin-top: 15px;
}

.recommendation-title {
    font-size: 14px;
    font-weight: 600;
    color: #166534;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.recommendation-main {
    font-size: 28px;
    font-weight: 700;
    color: #14532d;
    margin-top: 8px;
}

.site-card {
    background: #ffffff;
    border: 1px solid #dbe4df;
    border-radius: 16px;
    padding: 20px;
    margin-top: 12px;
}

.site-card-best {
    background: #f0fdf4;
    border: 2px solid #86efac;
    border-radius: 16px;
    padding: 20px;
    margin-top: 12px;
}

.site-title {
    font-size: 20px;
    font-weight: 700;
    color: #14532d;
}

.site-description {
    color: #475569;
    font-size: 14px;
    margin-top: 5px;
}

.action-text {
    font-size: 18px;
    font-weight: 600;
    color: #0f172a;
    line-height: 1.5;
}

.technical-note {
    background: #f8fafc;
    border-left: 4px solid #94a3b8;
    padding: 14px 18px;
    border-radius: 8px;
    color: #475569;
    font-size: 13px;
}

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    padding-top: 40px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA
# ============================================================

locations = {

    "Washermanpet": {
        "lat": 13.1085,
        "lon": 80.2806,
        "lst": 41.2,
        "ndvi": 0.18,
        "built": 84,
        "population": 88,
        "roads": [
            {
                "name": "Tondiarpet High Road",
                "space": 900,
                "trees": 75,
                "lat": 13.1089,
                "lon": 80.2820
            },
            {
                "name": "Moolakadai Main Road",
                "space": 650,
                "trees": 50,
                "lat": 13.1040,
                "lon": 80.2790
            }
        ],
        "open_spaces": [
            {
                "name": "Pocket Space near Moolakadai",
                "area": 1200,
                "lat": 13.1050,
                "lon": 80.2780
            }
        ]
    },

    "Royapuram": {
        "lat": 13.1150,
        "lon": 80.2940,
        "lst": 40.8,
        "ndvi": 0.20,
        "built": 81,
        "population": 86,
        "roads": [
            {
                "name": "Royapuram High Road",
                "space": 1100,
                "trees": 90,
                "lat": 13.1140,
                "lon": 80.2945
            },
            {
                "name": "Kalmandapam Road",
                "space": 700,
                "trees": 55,
                "lat": 13.1170,
                "lon": 80.2900
            }
        ],
        "open_spaces": [
            {
                "name": "Royapuram Pocket Open Space",
                "area": 1500,
                "lat": 13.1160,
                "lon": 80.2910
            }
        ]
    },

    "Perambur": {
        "lat": 13.1152,
        "lon": 80.2332,
        "lst": 40.5,
        "ndvi": 0.22,
        "built": 79,
        "population": 83,
        "roads": [
            {
                "name": "Perambur High Road",
                "space": 1200,
                "trees": 100,
                "lat": 13.1160,
                "lon": 80.2340
            },
            {
                "name": "Paper Mills Road",
                "space": 800,
                "trees": 65,
                "lat": 13.1120,
                "lon": 80.2310
            }
        ],
        "open_spaces": [
            {
                "name": "Perambur Community Open Space",
                "area": 1800,
                "lat": 13.1140,
                "lon": 80.2290
            }
        ]
    },

    "Ambattur": {
        "lat": 13.1143,
        "lon": 80.1548,
        "lst": 39.8,
        "ndvi": 0.28,
        "built": 72,
        "population": 77,
        "roads": [
            {
                "name": "Ambattur Red Hills Road",
                "space": 1600,
                "trees": 130,
                "lat": 13.1150,
                "lon": 80.1560
            },
            {
                "name": "MTH Road",
                "space": 1300,
                "trees": 105,
                "lat": 13.1120,
                "lon": 80.1530
            }
        ],
        "open_spaces": [
            {
                "name": "Ambattur Industrial Pocket Space",
                "area": 2400,
                "lat": 13.1180,
                "lon": 80.1500
            }
        ]
    },

    "Avadi": {
        "lat": 13.1147,
        "lon": 80.1017,
        "lst": 39.5,
        "ndvi": 0.31,
        "built": 68,
        "population": 73,
        "roads": [
            {
                "name": "Avadi Main Road",
                "space": 1800,
                "trees": 145,
                "lat": 13.1155,
                "lon": 80.1030
            },
            {
                "name": "Poonamallee High Road",
                "space": 1500,
                "trees": 120,
                "lat": 13.1110,
                "lon": 80.1010
            }
        ],
        "open_spaces": [
            {
                "name": "Avadi Community Open Space",
                "area": 3200,
                "lat": 13.1180,
                "lon": 80.0990
            }
        ]
    },

    "Anna Nagar": {
        "lat": 13.0850,
        "lon": 80.2101,
        "lst": 38.6,
        "ndvi": 0.34,
        "built": 75,
        "population": 70,
        "roads": [
            {
                "name": "2nd Avenue",
                "space": 1400,
                "trees": 115,
                "lat": 13.0860,
                "lon": 80.2110
            },
            {
                "name": "3rd Avenue",
                "space": 1000,
                "trees": 80,
                "lat": 13.0830,
                "lon": 80.2130
            }
        ],
        "open_spaces": [
            {
                "name": "Anna Nagar Pocket Park Site",
                "area": 2100,
                "lat": 13.0840,
                "lon": 80.2070
            }
        ]
    },

    "Nungambakkam": {
        "lat": 13.0569,
        "lon": 80.2425,
        "lst": 38.9,
        "ndvi": 0.29,
        "built": 78,
        "population": 73,
        "roads": [
            {
                "name": "College Road",
                "space": 900,
                "trees": 75,
                "lat": 13.0580,
                "lon": 80.2430
            },
            {
                "name": "Nelson Manickam Road",
                "space": 750,
                "trees": 60,
                "lat": 13.0600,
                "lon": 80.2400
            }
        ],
        "open_spaces": [
            {
                "name": "Nungambakkam Pocket Open Space",
                "area": 1100,
                "lat": 13.0550,
                "lon": 80.2400
            }
        ]
    },

    "T Nagar": {
        "lat": 13.0418,
        "lon": 80.2341,
        "lst": 39.8,
        "ndvi": 0.25,
        "built": 82,
        "population": 78,
        "roads": [
            {
                "name": "South Usman Road",
                "space": 850,
                "trees": 70,
                "lat": 13.0405,
                "lon": 80.2350
            },
            {
                "name": "G N Chetty Road",
                "space": 1000,
                "trees": 80,
                "lat": 13.0440,
                "lon": 80.2370
            }
        ],
        "open_spaces": [
            {
                "name": "T Nagar Pocket Space",
                "area": 900,
                "lat": 13.0430,
                "lon": 80.2310
            }
        ]
    },

    "Mylapore": {
        "lat": 13.0339,
        "lon": 80.2674,
        "lst": 38.3,
        "ndvi": 0.38,
        "built": 69,
        "population": 69,
        "roads": [
            {
                "name": "R K Mutt Road",
                "space": 1300,
                "trees": 105,
                "lat": 13.0345,
                "lon": 80.2680
            },
            {
                "name": "Santhome High Road",
                "space": 1000,
                "trees": 80,
                "lat": 13.0310,
                "lon": 80.2660
            }
        ],
        "open_spaces": [
            {
                "name": "Mylapore Community Park Site",
                "area": 2600,
                "lat": 13.0360,
                "lon": 80.2640
            }
        ]
    },

    "Guindy": {
        "lat": 13.0067,
        "lon": 80.2206,
        "lst": 39.1,
        "ndvi": 0.36,
        "built": 67,
        "population": 65,
        "roads": [
            {
                "name": "Guindy Industrial Road",
                "space": 1500,
                "trees": 120,
                "lat": 13.0070,
                "lon": 80.2220
            },
            {
                "name": "Mount Poonamallee Road",
                "space": 1800,
                "trees": 145,
                "lat": 13.0090,
                "lon": 80.2180
            }
        ],
        "open_spaces": [
            {
                "name": "Guindy Industrial Green Site",
                "area": 3500,
                "lat": 13.0040,
                "lon": 80.2190
            }
        ]
    },

    "Adyar": {
        "lat": 13.0012,
        "lon": 80.2565,
        "lst": 37.8,
        "ndvi": 0.44,
        "built": 60,
        "population": 62,
        "roads": [
            {
                "name": "L B Road",
                "space": 1400,
                "trees": 115,
                "lat": 13.0015,
                "lon": 80.2580
            },
            {
                "name": "Sardar Patel Road",
                "space": 1200,
                "trees": 95,
                "lat": 13.0030,
                "lon": 80.2540
            }
        ],
        "open_spaces": [
            {
                "name": "Adyar Pocket Park Site",
                "area": 3000,
                "lat": 12.9990,
                "lon": 80.2550
            }
        ]
    },

    "Velachery": {
        "lat": 12.9815,
        "lon": 80.2180,
        "lst": 39.2,
        "ndvi": 0.27,
        "built": 76,
        "population": 82,
        "roads": [
            {
                "name": "Velachery Main Road",
                "space": 1300,
                "trees": 105,
                "lat": 12.9820,
                "lon": 80.2200
            },
            {
                "name": "Taramani Link Road",
                "space": 1100,
                "trees": 90,
                "lat": 12.9790,
                "lon": 80.2160
            }
        ],
        "open_spaces": [
            {
                "name": "Velachery Open Space",
                "area": 2200,
                "lat": 12.9840,
                "lon": 80.2140
            }
        ]
    },

    "Perungudi": {
        "lat": 12.9600,
        "lon": 80.2420,
        "lst": 40.0,
        "ndvi": 0.23,
        "built": 79,
        "population": 80,
        "roads": [
            {
                "name": "OMR Service Road",
                "space": 1700,
                "trees": 135,
                "lat": 12.9610,
                "lon": 80.2440
            },
            {
                "name": "Perungudi Industrial Road",
                "space": 1400,
                "trees": 110,
                "lat": 12.9580,
                "lon": 80.2400
            }
        ],
        "open_spaces": [
            {
                "name": "Perungudi Green Buffer Site",
                "area": 4000,
                "lat": 12.9630,
                "lon": 80.2390
            }
        ]
    },

    "Sholinganallur": {
        "lat": 12.9010,
        "lon": 80.2279,
        "lst": 40.4,
        "ndvi": 0.21,
        "built": 75,
        "population": 85,
        "roads": [
            {
                "name": "Sholinganallur Main Road",
                "space": 1600,
                "trees": 130,
                "lat": 12.9020,
                "lon": 80.2290
            },
            {
                "name": "OMR Service Road",
                "space": 1800,
                "trees": 145,
                "lat": 12.8990,
                "lon": 80.2260
            }
        ],
        "open_spaces": [
            {
                "name": "Sholinganallur Open Development Space",
                "area": 4500,
                "lat": 12.9040,
                "lon": 80.2240
            }
        ]
    },

    "Tambaram": {
        "lat": 12.9249,
        "lon": 80.1000,
        "lst": 39.0,
        "ndvi": 0.32,
        "built": 70,
        "population": 78,
        "roads": [
            {
                "name": "GST Road",
                "space": 1700,
                "trees": 135,
                "lat": 12.9260,
                "lon": 80.1020
            },
            {
                "name": "Tambaram Velachery Road",
                "space": 1500,
                "trees": 120,
                "lat": 12.9220,
                "lon": 80.0980
            }
        ],
        "open_spaces": [
            {
                "name": "Tambaram Community Open Space",
                "area": 3300,
                "lat": 12.9280,
                "lon": 80.0960
            }
        ]
    }
}


# ============================================================
# HEAT ENGINE
# ============================================================

def normalize(value, minimum, maximum):

    result = (
        (value - minimum) /
        (maximum - minimum)
    ) * 100

    return max(0, min(100, result))


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

    vegetation_deficit = max(
        0,
        min(
            100,
            100 - ndvi * 100
        )
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
        min(
            100,
            100 - data["ndvi"] * 100
        )
    )

    return {
        "Surface Heat":
            0.45 * heat,

        "Built-up Intensity":
            0.25 * data["built"],

        "Vegetation Deficit":
            0.20 * vegetation_deficit,

        "Population Exposure":
            0.10 * data["population"]
    }


# ============================================================
# SPACE ANALYSIS
# ============================================================

def find_best_tree_road(data):

    if not data["roads"]:
        return None

    return max(
        data["roads"],
        key=lambda x: x["trees"]
    )


def find_best_open_space(data):

    if not data["open_spaces"]:
        return None

    return max(
        data["open_spaces"],
        key=lambda x: x["area"]
    )


def calculate_space(data):

    roadside_space = sum(
        road["space"]
        for road in data["roads"]
    )

    tree_capacity = sum(
        road["trees"]
        for road in data["roads"]
    )

    open_space = sum(
        space["area"]
        for space in data["open_spaces"]
    )

    return (
        roadside_space,
        tree_capacity,
        open_space
    )


# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

def determine_intervention(
    data,
    risk
):

    contributions = get_contributions(data)

    dominant = max(
        contributions,
        key=contributions.get
    )

    best_road = find_best_tree_road(data)
    best_space = find_best_open_space(data)

    roadside_space, tree_capacity, open_space = calculate_space(data)

    # --------------------------------------------------------
    # LOW VEGETATION
    # --------------------------------------------------------

    if dominant == "Vegetation Deficit":

        if best_space and best_space["area"] >= 2500:

            return {
                "type": "urban_forest",
                "name": "Urban Forests & Trees",
                "action":
                    f"Develop an urban forest at "
                    f"{best_space['name']}.",
                "location":
                    best_space["name"],
                "details":
                    f"{best_space['area']:,} m² of open space "
                    "is available for dense tree planting.",
                "lat":
                    best_space["lat"],
                "lon":
                    best_space["lon"],
                "quantity":
                    best_space["area"]
            }

        elif best_road:

            return {
                "type": "trees",
                "name": "Urban Forests & Trees",
                "action":
                    f"Plant {best_road['trees']} trees along "
                    f"{best_road['name']}.",
                "location":
                    best_road["name"],
                "details":
                    f"Approximately {best_road['space']:,} m² "
                    "of roadside space is available.",
                "lat":
                    best_road["lat"],
                "lon":
                    best_road["lon"],
                "quantity":
                    best_road["trees"]
            }

    # --------------------------------------------------------
    # HIGH BUILT-UP
    # --------------------------------------------------------

    if dominant == "Built-up Intensity":

        suitable_roof_area = int(
            data["built"] * 1000
        )

        return {
            "type": "cool_roof",
            "name": "Reflective Cool Roofs",
            "action":
                f"Apply reflective cool-roof material to "
                f"approximately {suitable_roof_area:,} m² "
                "of suitable roof area.",
            "location":
                f"{data['built']}% built-up zone",
            "details":
                "High built-up intensity means roof treatment "
                "is more practical than using limited ground space.",
            "lat":
                data["lat"],
            "lon":
                data["lon"],
            "quantity":
                suitable_roof_area,
            "suitable_area":
                suitable_roof_area
        }

    # --------------------------------------------------------
    # HIGH SURFACE HEAT
    # --------------------------------------------------------

    if dominant == "Surface Heat":

        if best_road:

            return {
                "type": "green_shade",
                "name": "Green + Shade Corridor",
                "action":
                    f"Create a green and shaded corridor along "
                    f"{best_road['name']}.",
                "location":
                    best_road["name"],
                "details":
                    f"{best_road['space']:,} m² of roadside space "
                    "can support trees and pedestrian shade.",
                "lat":
                    best_road["lat"],
                "lon":
                    best_road["lon"],
                "quantity":
                    best_road["trees"]
            }

    # --------------------------------------------------------
    # HIGH POPULATION
    # --------------------------------------------------------

    if dominant == "Population Exposure":

        if best_space and best_space["area"] >= 2000:

            return {
                "type": "pocket_park",
                "name": "Pocket Parks",
                "action":
                    f"Develop a cooling pocket park at "
                    f"{best_space['name']}.",
                "location":
                    best_space["name"],
                "details":
                    f"The site provides approximately "
                    f"{best_space['area']:,} m² of open space "
                    "for public cooling.",
                "lat":
                    best_space["lat"],
                "lon":
                    best_space["lon"],
                "quantity":
                    best_space["area"]
            }

    # --------------------------------------------------------
    # WATER-BASED OPTION
    # --------------------------------------------------------

    if best_space and best_space["area"] >= 3500:

        return {
            "type": "blue_green",
            "name": "Blue Infrastructure",
            "action":
                f"Develop a blue-green cooling space at "
                f"{best_space['name']}.",
            "location":
                best_space["name"],
            "details":
                f"The large {best_space['area']:,} m² space "
                "can support water-sensitive cooling design.",
            "lat":
                best_space["lat"],
            "lon":
                best_space["lon"],
            "quantity":
                best_space["area"]
        }

    # --------------------------------------------------------
    # REFLECTIVE PAVEMENT FALLBACK
    # --------------------------------------------------------

    if best_road and best_road["space"] >= 1500:

        return {
            "type": "reflective_pavement",
            "name": "Reflective Pavements",
            "action":
                f"Use reflective pavement treatment along "
                f"{best_road['name']}.",
            "location":
                best_road["name"],
            "details":
                f"Approximately {best_road['space']:,} m² "
                "of roadside/paved area is available.",
            "lat":
                best_road["lat"],
            "lon":
                best_road["lon"],
            "quantity":
                best_road["space"]
        }

    # --------------------------------------------------------
    # FINAL FALLBACK
    # --------------------------------------------------------

    if best_road:

        return {
            "type": "shaded_corridor",
            "name": "Shaded Pedestrian Corridors",
            "action":
                f"Create a shaded pedestrian corridor along "
                f"{best_road['name']}.",
            "location":
                best_road["name"],
            "details":
                f"{best_road['space']:,} m² of roadside space "
                "is available.",
            "lat":
                best_road["lat"],
            "lon":
                best_road["lon"],
            "quantity":
                best_road["space"]
        }

    return None


# ============================================================
# INTERVENTION SIMULATION
# ============================================================

def simulate_intervention(
    original_risk,
    intervention_type,
    quantity,
    suitable_area=0
):

    # --------------------------------------------------------
    # URBAN FORESTS / TREES
    # --------------------------------------------------------

    if intervention_type == "trees":

        reduction = (
            quantity / 2000.0
        ) * 18.0

    # --------------------------------------------------------
    # URBAN FOREST
    # --------------------------------------------------------

    elif intervention_type == "urban_forest":

        reduction = (
            quantity / 5000.0
        ) * 22.0

    # --------------------------------------------------------
    # POCKET PARK
    # --------------------------------------------------------

    elif intervention_type == "pocket_park":

        reduction = (
            quantity / 5000.0
        ) * 22.0

    # --------------------------------------------------------
    # BLUE INFRASTRUCTURE
    # --------------------------------------------------------

    elif intervention_type == "blue_green":

        reduction = (
            quantity / 5000.0
        ) * 18.0

    # --------------------------------------------------------
    # GREEN + SHADE
    # --------------------------------------------------------

    elif intervention_type == "green_shade":

        reduction = (
            quantity / 2000.0
        ) * 20.0

    # --------------------------------------------------------
    # SHADED CORRIDOR
    # --------------------------------------------------------

    elif intervention_type == "shaded_corridor":

        reduction = (
            quantity / 2000.0
        ) * 12.0

    # --------------------------------------------------------
    # REFLECTIVE PAVEMENT
    # --------------------------------------------------------

    elif intervention_type == "reflective_pavement":

        reduction = (
            quantity / 10000.0
        ) * 8.0

    # --------------------------------------------------------
    # REFLECTIVE COOL ROOF
    # --------------------------------------------------------

    elif intervention_type == "cool_roof":

        if suitable_area <= 0:

            suitable_area = quantity

        coverage = min(
            1.0,
            quantity / suitable_area
        )

        # Maximum modelled reduction of the HEAT COMPONENT.
        # This is an adjustable planning assumption.
        max_heat_component_reduction = 0.20

        heat_component = (
            normalize(
                data["lst"],
                30,
                45
            ) * 0.45
        )

        reduction = (
            heat_component
            * max_heat_component_reduction
            * coverage
        )

    else:

        reduction = 5

    # Never allow the intervention to reduce
    # more than 75% of the existing risk.

    reduction = min(
        reduction,
        original_risk * 0.75
    )

    new_risk = max(
        0,
        original_risk - reduction
    )

    return new_risk, reduction


# ============================================================
# COST MODEL
# ============================================================

def calculate_cost(
    intervention_type,
    quantity
):

    if intervention_type in [
        "trees",
        "urban_forest"
    ]:

        install = quantity * 650
        establishment = quantity * 300
        maintenance = quantity * 250

    elif intervention_type == "cool_roof":

        install = quantity * 300
        establishment = 0
        maintenance = quantity * 30

    elif intervention_type == "pocket_park":

        install = quantity * 1600
        establishment = 0
        maintenance = quantity * 100

    elif intervention_type == "blue_green":

        install = quantity * 1200
        establishment = 0
        maintenance = quantity * 80

    elif intervention_type in [
        "green_shade",
        "shaded_corridor"
    ]:

        install = quantity * 650
        establishment = quantity * 250
        maintenance = quantity * 150

    elif intervention_type == "reflective_pavement":

        install = quantity * 400
        establishment = 0
        maintenance = quantity * 25

    else:

        install = 0
        establishment = 0
        maintenance = 0

    initial = (
        install +
        establishment
    )

    five_year = (
        initial +
        maintenance * 5
    )

    return initial, five_year


# ============================================================
# RISK LABEL
# ============================================================

def risk_label(risk):

    if risk < 25:
        return "Low"

    elif risk < 50:
        return "Moderate"

    elif risk < 75:
        return "High"

    return "Critical"


# ============================================================
# HEADER
# ============================================================

st.title("🌿 HeatScape")

st.markdown(
    "### Climate Intelligence · Chennai"
)

st.write(
    "Identify urban heat hotspots, understand what is causing them, "
    "and determine where practical cooling interventions can be implemented."
)

st.divider()


# ============================================================
# LOCATION
# ============================================================

st.subheader("Select Location")

selected_location = st.selectbox(
    "Choose a locality",
    list(locations.keys())
)

data = locations[selected_location]

risk = calculate_risk(
    data["lst"],
    data["ndvi"],
    data["built"],
    data["population"]
)

label = risk_label(risk)


# ============================================================
# CURRENT CONDITIONS
# ============================================================

st.subheader("Current Conditions")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                Heat Risk
            </div>

            <div class="metric-value">
                {risk:.0f}/100
            </div>

            <div class="metric-small">
                {label}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                Surface Temperature
            </div>

            <div class="metric-value">
                {data["lst"]:.1f}°C
            </div>

            <div class="metric-small">
                Surface heat variable
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                Vegetation
            </div>

            <div class="metric-value">
                {data["ndvi"]:.2f}
            </div>

            <div class="metric-small">
                NDVI
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                Built-up Area
            </div>

            <div class="metric-value">
                {data["built"]}%
            </div>

            <div class="metric-small">
                Built-up intensity
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAP
# ============================================================

st.subheader("Chennai Heat Map")

heat_map = folium.Map(
    location=[
        data["lat"],
        data["lon"]
    ],
    zoom_start=13,
    tiles="OpenStreetMap"
)

folium.CircleMarker(
    location=[
        data["lat"],
        data["lon"]
    ],
    radius=16,
    color="red",
    fill=True,
    fill_opacity=0.5,
    popup=(
        f"{selected_location} — "
        f"Heat Risk {risk:.0f}/100"
    )
).add_to(heat_map)

for road in data["roads"]:

    folium.CircleMarker(
        location=[
            road["lat"],
            road["lon"]
        ],
        radius=6,
        color="orange",
        fill=True,
        fill_opacity=0.8,
        popup=(
            f"<b>{road['name']}</b><br>"
            f"Roadside space: "
            f"{road['space']:,} m²<br>"
            f"Tree capacity: "
            f"{road['trees']}"
        )
    ).add_to(heat_map)

for space in data["open_spaces"]:

    folium.CircleMarker(
        location=[
            space["lat"],
            space["lon"]
        ],
        radius=7,
        color="green",
        fill=True,
        fill_opacity=0.8,
        popup=(
            f"<b>{space['name']}</b><br>"
            f"Open space: "
            f"{space['area']:,} m²"
        )
    ).add_to(heat_map)

st_folium(
    heat_map,
    width=None,
    height=520,
    returned_objects=[],
    key="main_heat_map"
)


# ============================================================
# HEAT FINGERPRINT
# ============================================================

st.subheader("What's Driving the Heat?")

contributions = get_contributions(data)

sorted_contributions = sorted(
    contributions.items(),
    key=lambda x: x[1],
    reverse=True
)

for name, value in sorted_contributions:

    st.markdown(
        f"**{name} — {value:.1f}**"
    )

    st.progress(
        min(
            1.0,
            value / 50
        )
    )

dominant = sorted_contributions[0][0]

st.markdown(
    f"""
    <div class="technical-note">

    <b>Dominant contributor:</b>
    {dominant}

    <br><br>

    HeatScape uses this contributor together with
    available physical space to determine the most
    suitable cooling technique.

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SPACE ANALYSIS
# ============================================================

st.subheader("Available Space Analysis")

st.write(
    "HeatScape checks the physical space available before "
    "selecting a cooling technique."
)

roadside_space, tree_capacity, open_space = calculate_space(data)

s1, s2, s3 = st.columns(3)

with s1:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Roadside Space
            </div>

            <div class="metric-value">
                {roadside_space:,} m²
            </div>

            <div class="metric-small">
                Candidate corridors
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
                Tree Capacity
            </div>

            <div class="metric-value">
                {tree_capacity}
            </div>

            <div class="metric-small">
                Estimated roadside capacity
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
                Open Space
            </div>

            <div class="metric-value">
                {open_space:,} m²
            </div>

            <div class="metric-small">
                Candidate green-space sites
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RECOMMENDATION
# ============================================================

recommendation = determine_intervention(
    data,
    risk
)

st.subheader("Recommended First Action")

if recommendation:

    st.markdown(
        f"""
        <div class="recommendation">

            <div class="recommendation-title">
                RECOMMENDED TECHNIQUE
            </div>

            <div class="recommendation-main">
                {recommendation["name"]}
            </div>

            <br>

            <div class="action-text">
                📍 {recommendation["action"]}
            </div>

            <br>

            <div class="site-description">
                {recommendation["details"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CANDIDATE LOCATIONS
# ============================================================

st.subheader("Candidate Implementation Locations")

for road in data["roads"]:

    if recommendation["location"] == road["name"]:

        card_class = "site-card-best"
        badge = "⭐ RECOMMENDED"

    else:

        card_class = "site-card"
        badge = "Candidate"

    st.markdown(
        f"""
        <div class="{card_class}">

            <div class="small-label">
                {badge}
            </div>

            <div class="site-title">
                {road["name"]}
            </div>

            <br>

            <div class="site-description">

                Available roadside space:
                <b>{road["space"]:,} m²</b>

                &nbsp;&nbsp;|&nbsp;&nbsp;

                Estimated tree capacity:
                <b>{road["trees"]}</b>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# INTERVENTION SIMULATOR
# ============================================================

st.subheader("Test the Intervention")

st.write(
    "Adjust the intervention scale and see the projected "
    "change in the Heat Risk Index."
)

if recommendation["type"] in [
    "trees",
    "urban_forest"
]:

    max_quantity = int(
        recommendation["quantity"]
    )

    if max_quantity < 10:
        max_quantity = 10

    quantity = st.slider(
        "Number / scale of trees",
        min_value=10,
        max_value=max_quantity,
        value=max(
            10,
            int(max_quantity * 0.75)
        ),
        step=10
    )

elif recommendation["type"] in [
    "pocket_park",
    "blue_green"
]:

    max_quantity = int(
        recommendation["quantity"]
    )

    quantity = st.slider(
        "Area treated (m²)",
        min_value=500,
        max_value=max_quantity,
        value=max(
            500,
            int(max_quantity * 0.75)
        ),
        step=100
    )

elif recommendation["type"] == "cool_roof":

    max_quantity = int(
        recommendation["suitable_area"]
    )

    quantity = st.slider(
        "Reflective roof area (m²)",
        min_value=500,
        max_value=max_quantity,
        value=max(
            500,
            int(max_quantity * 0.50)
        ),
        step=500
    )

elif recommendation["type"] == "reflective_pavement":

    max_quantity = int(
        recommendation["quantity"]
    )

    quantity = st.slider(
        "Reflective pavement area (m²)",
        min_value=500,
        max_value=max_quantity,
        value=max(
            500,
            int(max_quantity * 0.50)
        ),
        step=100
    )

else:

    max_quantity = int(
        recommendation["quantity"]
    )

    quantity = st.slider(
        "Intervention area (m²)",
        min_value=500,
        max_value=max_quantity,
        value=max(
            500,
            int(max_quantity * 0.75)
        ),
        step=100
    )


# ============================================================
# SIMULATION
# ============================================================

if recommendation["type"] == "cool_roof":

    new_risk, reduction = simulate_intervention(
        risk,
        recommendation["type"],
        quantity,
        recommendation["suitable_area"]
    )

else:

    new_risk, reduction = simulate_intervention(
        risk,
        recommendation["type"],
        quantity
    )


p1, p2, p3 = st.columns(3)

with p1:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Current Risk
            </div>

            <div class="metric-value">
                {risk:.0f}
            </div>

            <div class="metric-small">
                {risk_label(risk)}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with p2:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Projected Risk
            </div>

            <div class="metric-value">
                {new_risk:.1f}
            </div>

            <div class="metric-small">
                {risk_label(new_risk)}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with p3:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Modelled Reduction
            </div>

            <div class="metric-value">
                {reduction:.1f}
            </div>

            <div class="metric-small">
                Heat Risk Index points
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# REFLECTIVE ROOF EXPLANATION
# ============================================================

if recommendation["type"] == "cool_roof":

    coverage = (
        quantity /
        recommendation["suitable_area"]
    ) * 100

    st.markdown(
        f"""
        <div class="technical-note">

        <b>Reflective material calculation</b>

        <br><br>

        Suitable roof area:
        <b>{recommendation["suitable_area"]:,} m²</b>

        <br>

        Selected treatment:
        <b>{quantity:,} m²</b>

        <br>

        Treatment coverage:
        <b>{coverage:.1f}%</b>

        <br><br>

        The model applies a configurable maximum reduction
        to the <b>heat component</b> of the Heat Risk Index.
        It does not claim a direct temperature reduction.

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# IMPLEMENTATION PLAN
# ============================================================

st.subheader("Implementation Plan")

if recommendation["type"] in [
    "trees",
    "urban_forest"
]:

    action = (
        f"Implement <b>{recommendation['name']}</b>: "
        f"plant approximately <b>{quantity}</b> trees "
        f"along <b>{recommendation['location']}</b>."
    )

elif recommendation["type"] == "pocket_park":

    action = (
        f"Implement <b> {recommendation['name']} </b>: "
        f"develop approximately <b>{quantity:,} m²</b> "
        f"at <b>{recommendation['location']}</b>."
    )

elif recommendation["type"] == "blue_green":

    action = (
        f"Implement <b>{recommendation['name']}</b>: "
        f"develop approximately <b>{quantity:,} m²</b> "
        f"of blue-green infrastructure at "
        f"<b>{recommendation['location']}</b>."
    )

elif recommendation["type"] == "cool_roof":

    action = (
        f"Implement <b>{recommendation['name']}</b>: "
        f"treat approximately <b>{quantity:,} m²</b> "
        f"of suitable roof area in "
        f"<b>{recommendation['location']}</b>."
    )

elif recommendation["type"] == "reflective_pavement":

    action = (
        f"Implement <b>{recommendation['name']}</b>: "
        f"treat approximately <b>{quantity:,} m²</b> "
        f"along <b>{recommendation['location']}</b>."
    )

else:

    action = (
        f"Implement <b>{recommendation['name']}</b> "
        f"along <b>{recommendation['location']}</b>."
    )


st.markdown(
    f"""
    <div class="recommendation">

        <div class="recommendation-title">
            SPECIFIC IMPLEMENTATION
        </div>

        <div class="recommendation-main">
            {action}
        </div>

        <br>

        <div class="site-description">

            Current Heat Risk:
            <b>{risk:.0f}/100</b>

            &nbsp; → &nbsp;

            Projected Heat Risk:
            <b>{new_risk:.1f}/100</b>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# IMPLEMENTATION MAP
# ============================================================

st.subheader("Where Will the Intervention Happen?")

implementation_map = folium.Map(
    location=[
        recommendation["lat"],
        recommendation["lon"]
    ],
    zoom_start=15,
    tiles="OpenStreetMap"
)

# Hotspot
folium.CircleMarker(
    location=[
        data["lat"],
        data["lon"]
    ],
    radius=18,
    color="red",
    fill=True,
    fill_opacity=0.25,
    popup=(
        f"Current Heat Risk: "
        f"{risk:.0f}/100"
    )
).add_to(implementation_map)


# Recommended location
folium.Marker(
    location=[
        recommendation["lat"],
        recommendation["lon"]
    ],
    popup=(
        f"<b>{recommendation['name']}</b><br>"
        f"{recommendation['location']}"
    ),
    tooltip=recommendation["name"]
).add_to(implementation_map)


# Candidate roads
for road in data["roads"]:

    folium.CircleMarker(
        location=[
            road["lat"],
            road["lon"]
        ],
        radius=5,
        color="blue",
        fill=True,
        fill_opacity=0.7,
        popup=(
            f"<b>{road['name']}</b><br>"
            f"Available space: "
            f"{road['space']:,} m²<br>"
            f"Tree capacity: "
            f"{road['trees']}"
        )
    ).add_to(implementation_map)


# Open spaces
for space in data["open_spaces"]:

    folium.CircleMarker(
        location=[
            space["lat"],
            space["lon"]
        ],
        radius=7,
        color="green",
        fill=True,
        fill_opacity=0.7,
        popup=(
            f"<b>{space['name']}</b><br>"
            f"Open space: "
            f"{space['area']:,} m²"
        )
    ).add_to(implementation_map)


st_folium(
    implementation_map,
    width=None,
    height=500,
    returned_objects=[],
    key="implementation_map"
)


# ============================================================
# COST
# ============================================================

st.subheader("Cost of Implementation")

initial_cost, five_year_cost = calculate_cost(
    recommendation["type"],
    quantity
)

cost1, cost2 = st.columns(2)

with cost1:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Initial Implementation
            </div>

            <div class="metric-value">
                ₹{initial_cost:,.0f}
            </div>

            <div class="metric-small">
                Estimated planning cost
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with cost2:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                5-Year Lifecycle Cost
            </div>

            <div class="metric-value">
                ₹{five_year_cost:,.0f}
            </div>

            <div class="metric-small">
                Includes estimated maintenance
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.caption(
    "Planning estimates only. Actual implementation costs "
    "vary by site, material, labour and municipal specifications."
)


# ============================================================
# ALL COOLING TECHNIQUES
# ============================================================

st.subheader("Cooling Techniques")

techniques = [
    (
        "Urban Forests & Trees",
        "Increase vegetation and tree canopy where land or roadside space is available."
    ),
    (
        "Green Corridors",
        "Create connected vegetation corridors along streets and pedestrian routes."
    ),
    (
        "Pocket Parks",
        "Convert suitable open spaces into small public cooling and green areas."
    ),
    (
        "Blue Infrastructure",
        "Use water-sensitive and blue-green design around suitable water or open-space areas."
    ),
    (
        "Reflective Cool Roofs",
        "Use reflective roof materials to reduce heat contribution from highly built-up areas."
    ),
    (
        "Reflective Pavements",
        "Use higher-reflectance pavement materials on suitable large paved surfaces."
    ),
    (
        "Shaded Pedestrian Corridors",
        "Add trees and/or shade structures to reduce pedestrian heat exposure."
    ),
    (
        "Green + Shade Corridors",
        "Combine vegetation and shade structures along high-heat roads."
    )
]

for technique, description in techniques:

    st.markdown(
        f"""
        <div class="site-card">

            <div class="site-title">
                {technique}
            </div>

            <div class="site-description">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# METHODOLOGY
# ============================================================

st.subheader("Methodology & Data")

with st.expander("How HeatScape works"):

    st.markdown("""
    ### Step 1 — Identify heat

    HeatScape uses surface temperature, vegetation,
    built-up intensity and population exposure.

    ### Step 2 — Calculate Heat Risk

    The prototype uses:

    **Heat Risk = 45% Surface Heat + 25% Built-up + 20% Vegetation Deficit + 10% Population Exposure**

    All factors are normalized to a 0–100 scale.

    ### Step 3 — Understand WHY

    HeatScape calculates the contribution of each factor
    to the final Heat Risk Index.

    ### Step 4 — Check available space

    The system evaluates candidate:

    - roadside space
    - open spaces
    - roof area
    - paved areas

    ### Step 5 — Select a cooling technique

    The recommendation can include:

    - Urban Forests & Trees
    - Green Corridors
    - Pocket Parks
    - Blue Infrastructure
    - Reflective Cool Roofs
    - Reflective Pavements
    - Shaded Pedestrian Corridors
    - Green + Shade Corridors

    ### Step 6 — Simulate

    The selected intervention is tested at a chosen scale
    and the resulting Heat Risk Index is projected.

    ### Reflective roof model

    For reflective roofs, the model calculates:

    **Treatment Coverage = Treated Roof Area / Suitable Roof Area**

    The coverage is then applied to the heat component of the
    Heat Risk Index using a configurable planning assumption.

    Therefore the output is a:

    **Projected Heat Risk Index reduction**

    rather than a claim that the physical temperature will
    decrease by a specific number of degrees.

    ### Data status

    The architecture is designed to use:

    - Landsat 8/9 → Surface Temperature
    - Sentinel-2 → NDVI
    - ESA WorldCover → Land Cover
    - WorldPop → Population
    - OpenStreetMap → Geographic Context

    The current prototype uses representative locality-level
    values and candidate intervention locations.

    These space estimates should be verified using detailed
    municipal/GIS/cadastral data before real-world implementation.
    """)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        HeatScape · Urban Heat Reduction Planner

        <br>

        <b>
        WHERE → WHY → WHAT → WHERE EXACTLY → WHAT IF → HOW MUCH
        </b>

    </div>
    """,
    unsafe_allow_html=True
)
