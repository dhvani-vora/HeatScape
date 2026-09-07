import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="HeatScape",
    page_icon="🌍",
    layout="wide"
)

# ---------- STYLE ----------
st.markdown("""
<style>
.main {
    background-color: #08111f;
}
.block-container {
    padding-top: 2rem;
}
h1 {
    font-size: 42px !important;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background: #111d2d;
    border: 1px solid #26364d;
}
.big-risk {
    font-size: 45px;
    font-weight: bold;
}
.small {
    color: #9aa9bc;
}
</style>
""", unsafe_allow_html=True)

# ---------- DEMO DATA ----------
hotspots = {
    "North Chennai": {
        "lst": 41.2,
        "ndvi": 0.18,
        "built": 78,
        "population": 85
    },
    "Central Chennai": {
        "lst": 39.8,
        "ndvi": 0.27,
        "built": 74,
        "population": 78
    },
    "South Chennai": {
        "lst": 37.1,
        "ndvi": 0.44,
        "built": 61,
        "population": 63
    }
}

# ---------- FUNCTIONS ----------
def normalize(value, minimum, maximum):
    if maximum == minimum:
        return 0
    return ((value - minimum) / (maximum - minimum)) * 100


def calculate_risk(lst, ndvi, built, population):

    heat = normalize(lst, 30, 45)
    vegetation_deficit = 100 - (ndvi * 100)
    population_exposure = population

    risk = (
        0.45 * heat +
        0.25 * built +
        0.20 * vegetation_deficit +
        0.10 * population_exposure
    )

    return min(100, max(0, risk))


def risk_category(risk):
    if risk >= 75:
        return "CRITICAL"
    elif risk >= 50:
        return "HIGH"
    elif risk >= 25:
        return "MODERATE"
    return "LOW"


# ---------- HEADER ----------
st.title("🌍 HeatScape")
st.write("Urban Heat Reduction Planner")

st.caption(
    "Identify heat hotspots → understand why → choose cooling actions → "
    "estimate cost and projected impact"
)

st.divider()

# ---------- HOTSPOT SELECTION ----------
st.subheader("🔥 1. Select a Chennai hotspot")

location = st.selectbox(
    "Choose area",
    list(hotspots.keys())
)

data = hotspots[location]

risk = calculate_risk(
    data["lst"],
    data["ndvi"],
    data["built"],
    data["population"]
)

category = risk_category(risk)

# ---------- METRICS ----------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Heat Risk", f"{risk:.0f}/100")
c2.metric("LST", f"{data['lst']} °C")
c3.metric("Built-up", f"{data['built']}%")
c4.metric("Vegetation", f"{data['ndvi'] * 100:.0f}%")

st.divider()

# ---------- WHY HOT ----------
st.subheader("🔎 2. Why is this area hot?")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### Main contributors")

    if data["lst"] > 38:
        st.error("🔥 High surface temperature")

    if data["built"] > 70:
        st.warning("🏙 High built-up intensity")

    if data["ndvi"] < 0.30:
        st.warning("🌱 Low vegetation")

    if data["population"] > 70:
        st.info("👥 High population exposure")

with col2:

    st.markdown("### Heat Risk Index")

    st.markdown(
        f'<div class="card">'
        f'<div class="big-risk">{risk:.0f}/100</div>'
        f'<b>{category}</b>'
        f'<p class="small">Transparent prototype planning index</p>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.latex(
        r"R = 0.45H + 0.25B + 0.20V + 0.10P"
    )

st.divider()

# ---------- INTERVENTION ----------
st.subheader("🌳 3. Simulate cooling interventions")

st.write(
    "Choose an intervention and see its estimated effect on the Heat Risk Index."
)

col1, col2, col3 = st.columns(3)

with col1:
    trees = st.slider(
        "🌳 Trees planted",
        0, 2000, 500, 100
    )

with col2:
    cool_roof = st.slider(
        "🏠 Cool roof area (m²)",
        0, 50000, 10000, 1000
    )

with col3:
    shade = st.slider(
        "🚶 Shade structures",
        0, 100, 10, 5
    )

# ---------- SIMULATION ----------
# Simple prototype assumptions
tree_effect = min(trees / 2000 * 12, 12)
roof_effect = min(cool_roof / 50000 * 10, 10)
shade_effect = min(shade / 100 * 5, 5)

total_reduction = tree_effect + roof_effect + shade_effect

predicted_risk = max(0, risk - total_reduction)

# ---------- COST ----------
tree_cost = trees * 500
roof_cost = cool_roof * 300
shade_cost = shade * 25000

total_cost = tree_cost + roof_cost + shade_cost

st.divider()

# ---------- RESULTS ----------
st.subheader("📊 4. Simulation Result")

before, after = st.columns(2)

with before:

    st.markdown("### BEFORE")

    st.metric(
        "Heat Risk",
        f"{risk:.0f}/100"
    )

    st.write(f"Status: **{category}**")

with after:

    st.markdown("### PROJECTED AFTER INTERVENTION")

    st.metric(
        "Heat Risk",
        f"{predicted_risk:.0f}/100",
        delta=f"-{total_reduction:.0f} points"
    )

    st.write(
        f"Projected status: **{risk_category(predicted_risk)}**"
    )

st.progress(
    min(predicted_risk / 100, 1.0),
    text="Projected Heat Risk"
)

st.caption(
    "⚠️ Illustrative model-based projection. "
    "Actual cooling impact requires local validation."
)

# ---------- COST ----------
st.divider()

st.subheader("💰 5. Estimated implementation cost")

cost_data = pd.DataFrame({
    "Intervention": [
        "Tree planting",
        "Cool roofs",
        "Shade structures"
    ],
    "Quantity": [
        f"{trees} trees",
        f"{cool_roof:,} m²",
        f"{shade} structures"
    ],
    "Estimated Cost": [
        f"₹{tree_cost:,.0f}",
        f"₹{roof_cost:,.0f}",
        f"₹{shade_cost:,.0f}"
    ]
})

st.table(cost_data)

st.markdown(
    f"### Estimated Total: ₹{total_cost:,.0f}"
)

st.caption(
    "Planning estimate using configurable prototype unit costs. "
    "Actual implementation costs vary by site."
)

# ---------- DATA SOURCES ----------
st.divider()

with st.expander("📚 Data sources & methodology"):

    st.write("HeatScape is designed to use:")

    st.write("""
    **Landsat 8/9 — USGS / NASA**
    → Land Surface Temperature

    **Sentinel-2 — Copernicus**
    → NDVI / Vegetation

    **ESA WorldCover — ESA**
    → Land cover / Built-up

    **WorldPop**
    → Population density

    **Greater Chennai Corporation / OpenStreetMap**
    → Roads, wards and water bodies
    """)

    st.write("Heat Risk Formula:")

    st.latex(
        r"R = 0.45H + 0.25B + 0.20V + 0.10P"
    )

    st.caption(
        "H = normalized heat, B = built-up intensity, "
        "V = vegetation deficit, P = population exposure."
    )

    st.caption(
        "The Heat Risk Index is a transparent prototype planning index, "
        "not a validated health-risk prediction."
    )
