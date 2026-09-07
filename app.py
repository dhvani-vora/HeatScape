import streamlit as st
import folium
from streamlit_folium import st_folium

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="HeatScape",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# STYLING
# -----------------------------

st.markdown("""
<style>

.main {
    background-color: #0b0f14;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: white;
}

p, label {
    color: #b8c1cc;
}

.metric-card {
    background: #151b23;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #252d38;
}

.recommendation {
    background: #16251c;
    border: 1px solid #2e6b43;
    padding: 25px;
    border-radius: 15px;
}

.warning {
    background: #251d13;
    border: 1px solid #72501f;
    padding: 20px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# DATA
# -----------------------------

hotspots = {
    "North Chennai": {
        "lat": 13.145,
        "lon": 80.285,
        "lst": 41.2,
        "ndvi": 0.18,
        "built": 78,
        "population": 85
    },

    "Central Chennai": {
        "lat": 13.0827,
        "lon": 80.2707,
        "lst": 39.8,
        "ndvi": 0.27,
        "built": 74,
        "population": 78
    },

    "South Chennai": {
        "lat": 12.965,
        "lon": 80.245,
        "lst": 37.1,
        "ndvi": 0.44,
        "built": 61,
        "population": 63
    }
}

# -----------------------------
# FUNCTIONS
# -----------------------------

def normalize(value, minimum, maximum):
    return max(0, min(100, ((value - minimum) / (maximum - minimum)) * 100))


def calculate_risk(lst, ndvi, built, population):

    heat = normalize(lst, 30, 45)

    vegetation_deficit = 100 - (ndvi * 100)

    risk = (
        0.45 * heat +
        0.25 * built +
        0.20 * vegetation_deficit +
        0.10 * population
    )

    return min(100, max(0, risk))


def get_category(risk):

    if risk < 25:
        return "Low"
    elif risk < 50:
        return "Moderate"
    elif risk < 75:
        return "High"
    else:
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
            "Increasing tree cover and connecting green spaces "
            "is the most suitable first intervention."
        )

    elif dominant == "Built-up Area":
        return (
            "🏠 Cool Roofs + Shade",
            "High built-up intensity is the dominant contributor. "
            "Cool roofs and shaded areas can reduce heat absorption."
        )

    elif dominant == "Population Exposure":
        return (
            "🚶 Shaded Public Spaces",
            "High population exposure makes public cooling "
            "infrastructure the priority."
        )

    else:
        return (
            "🌳 Green Corridor + Cool Roofs",
            "Surface heat is the dominant contributor, so a combined "
            "green and built-environment intervention is recommended."
        )


def calculate_simulation(
    risk,
    trees,
    roof_area,
    shade_structures
):

    tree_effect = min((trees / 2000) * 12, 12)

    roof_effect = min((roof_area / 50000) * 10, 10)

    shade_effect = min((shade_structures / 100) * 5, 5)

    total_reduction = (
        tree_effect +
        roof_effect +
        shade_effect
    )

    new_risk = max(0, risk - total_reduction)

    return new_risk


def risk_color(risk):

    if risk >= 75:
        return "red"
    elif risk >= 50:
        return "orange"
    elif risk >= 25:
        return "beige"
    else:
        return "green"


# -----------------------------
# HEADER
# -----------------------------

st.title("🌍 HeatScape")

st.write(
    "### Urban Heat Reduction Planner"
)

st.write(
    "Identify urban heat hotspots → understand why they are hot → "
    "choose the best cooling intervention → simulate the impact."
)

st.divider()

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("📍 Hotspot Selection")

selected = st.sidebar.selectbox(
    "Select Chennai region",
    list(hotspots.keys())
)

data = hotspots[selected]

# -----------------------------
# CALCULATE RISK
# -----------------------------

risk = calculate_risk(
    data["lst"],
    data["ndvi"],
    data["built"],
    data["population"]
)

category = get_category(risk)

# -----------------------------
# TOP METRICS
# -----------------------------

st.subheader(f"🔥 {selected}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Heat Risk",
        f"{risk:.0f}/100"
    )

with col2:
    st.metric(
        "Surface Temperature",
        f"{data['lst']} °C"
    )

with col3:
    st.metric(
        "Vegetation",
        f"{data['ndvi'] * 100:.0f}%"
    )

with col4:
    st.metric(
        "Built-up",
        f"{data['built']}%"
    )

st.write(f"**Risk Level:** {category}")

st.divider()

# -----------------------------
# MAP
# -----------------------------

st.subheader("🗺️ Chennai Heat Map")

m = folium.Map(
    location=[13.0827, 80.2707],
    zoom_start=11,
    tiles="CartoDB dark_matter"
)

for name, h in hotspots.items():

    r = calculate_risk(
        h["lst"],
        h["ndvi"],
        h["built"],
        h["population"]
    )

    folium.CircleMarker(
        location=[h["lat"], h["lon"]],
        radius=12 if name == selected else 8,
        popup=f"{name} — Risk {r:.0f}/100",
        tooltip=f"{name}: {r:.0f}/100",
        color=risk_color(r),
        fill=True,
        fill_opacity=0.8
    ).add_to(m)

st_folium(
    m,
    width=1100,
    height=500
)

st.caption(
    "Prototype map showing heat-risk hotspots. "
    "The final version will use real satellite-derived spatial data."
)

# -----------------------------
# HEAT FINGERPRINT
# -----------------------------

st.divider()

st.subheader("🧬 Heat Fingerprint")

st.write(
    "Instead of only saying an area is hot, HeatScape explains "
    "what is contributing to the risk."
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

    percentage = min(100, value)

    st.write(
        f"**{name}** — {percentage:.1f}"
    )

    st.progress(
        int(percentage)
    )

# -----------------------------
# RECOMMENDATION
# -----------------------------

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

# -----------------------------
# SIMULATION
# -----------------------------

st.divider()

st.subheader("🔬 Intervention Simulator")

st.write(
    "What happens if the city actually implements cooling measures?"
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

new_risk = calculate_simulation(
    risk,
    trees,
    roof_area,
    shade_structures
)

reduction = risk - new_risk

st.write("### Before → After")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Current Risk",
        f"{risk:.0f}/100"
    )

with col2:
    st.metric(
        "Projected Risk",
        f"{new_risk:.0f}/100"
    )

with col3:
    st.metric(
        "Risk Reduction",
        f"{reduction:.1f} points"
    )

# -----------------------------
# COST ESTIMATION
# -----------------------------

st.divider()

st.subheader("💰 Estimated Implementation Cost")

tree_cost = trees * 500

roof_cost = roof_area * 300

shade_cost = shade_structures * 25000

total_cost = (
    tree_cost +
    roof_cost +
    shade_cost
)

st.write(
    f"### ₹{total_cost:,.0f}"
)

st.write(
    f"""
    🌳 Trees: ₹{tree_cost:,.0f}  
    🏠 Cool roofs: ₹{roof_cost:,.0f}  
    🚶 Shade structures: ₹{shade_cost:,.0f}
    """
)

st.caption(
    "Planning estimate only. Actual implementation costs vary by site."
)

# -----------------------------
# BUDGET OPTIMIZER
# -----------------------------

st.divider()

st.subheader("💸 Budget Optimizer")

st.write(
    "How much cooling can we achieve with a limited public budget?"
)

budget = st.number_input(
    "Enter available budget (₹)",
    min_value=100000,
    max_value=100000000,
    value=10000000,
    step=500000
)

if budget > 0:

    possible_trees = int(budget / 500)

    possible_roofs = int(budget / 300)

    st.write(
        f"With **₹{budget:,.0f}**, the planner could theoretically fund:"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Maximum trees",
            f"{possible_trees:,}"
        )

    with col2:
        st.metric(
            "Maximum cool-roof area",
            f"{possible_roofs:,} m²"
        )

# -----------------------------
# METHODOLOGY
# -----------------------------

st.divider()

with st.expander("📊 Methodology & Data Sources"):

    st.write("""
    ### Heat Risk Formula

    Heat Risk =
    0.45 × Surface Heat +
    0.25 × Built-up +
    0.20 × Vegetation Deficit +
    0.10 × Population Exposure

    Each factor is normalized to a 0–100 scale.

    ### Planned real data sources

    • Landsat 8/9 → Land Surface Temperature (LST)

    • Sentinel-2 → NDVI / vegetation

    • Copernicus land-cover data → built-up area

    • WorldPop → population exposure

    • OpenStreetMap / GCC GIS → roads, water bodies and boundaries

    ### Important

    The current interface uses prototype hotspot values.
    The next data pipeline will replace these values with
    real satellite-derived measurements.
    """)

st.caption(
    "HeatScape — Data-driven urban heat reduction planning"
)
