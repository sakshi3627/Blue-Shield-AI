import streamlit as st
import plotly.graph_objects as go
import joblib
import numpy as np

st.set_page_config(
    page_title="Blue Shield AI",
    page_icon="🌊",
    layout="wide"
)

# -----------------------------
# Load trained AI model
# -----------------------------

model = joblib.load("iuu_behavior_model.pkl")


# -----------------------------
# Page styling
# -----------------------------

st.markdown("""
<style>
.stApp {
    background-color: #f5f8fb;
}

h1, h2, h3 {
    color: #063970;
}

div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #dce5ed;
    padding: 15px;
    border-radius: 12px;
}

div[data-testid="stMetricValue"] {
    color: #063970;
}

.stButton > button {
    width: 100%;
    background-color: #063970;
    color: white;
    font-weight: bold;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Functions
# -----------------------------

def get_risk_level(score):
    if score >= 70:
        return "HIGH", "🔴"
    elif score >= 40:
        return "MEDIUM", "🟠"
    else:
        return "LOW", "🟢"


def create_gauge(score, title):

    if score >= 70:
        bar_color = "#d62728"
    elif score >= 40:
        bar_color = "#ff9800"
    else:
        bar_color = "#2e9d59"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": title},
            number={"suffix": "/100"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": bar_color},
                "steps": [
                    {
                        "range": [0, 40],
                        "color": "#e8f5e9"
                    },
                    {
                        "range": [40, 70],
                        "color": "#fff3e0"
                    },
                    {
                        "range": [70, 100],
                        "color": "#ffebee"
                    }
                ]
            }
        )
    )

    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white"
    )

    return fig


# -----------------------------
# Header
# -----------------------------

st.title("🌊 Blue Shield AI")

st.subheader(
    "AI-Powered Maritime Risk & Marine Ecosystem Protection System"
)

st.write("**Detect → Analyse → Assess → Prioritize → Verify**")

st.divider()


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("⚓ Vessel Telemetry")

    vessel_id = st.text_input(
        "Vessel ID",
        value="V001"
    )

    st.subheader("📍 Vessel Location")

    lat = st.number_input(
        "Latitude",
        value=-3.1500,
        format="%.4f"
    )

    lon = st.number_input(
        "Longitude",
        value=130.2000,
        format="%.4f"
    )

    st.subheader("🚢 Vessel Behaviour")

    speed_knots = st.number_input(
        "Speed (knots)",
        min_value=0.0,
        value=4.2,
        step=0.1
    )

    ais_gap_hours = st.number_input(
        "AIS Gap (hours)",
        min_value=0.0,
        value=12.5,
        step=0.5
    )

    spoofed_identity = st.selectbox(
        "Identity Anomaly Detected?",
        options=[0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No",
        index=1
    )

    proximity_meters = st.number_input(
        "Proximity to MPA (meters)",
        min_value=0.0,
        value=150.0,
        step=50.0
    )

    st.subheader("🌊 Ecosystem Information")

    in_mpa_zone = st.selectbox(
        "Inside Marine Protected Area?",
        options=[0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No",
        index=1
    )

    coral_reef_proximity = st.number_input(
        "Coral Reef Proximity (meters)",
        min_value=0.0,
        value=80.0,
        step=10.0
    )

    benthic_sensitivity = st.number_input(
        "Benthic Sensitivity (0–10)",
        min_value=0.0,
        max_value=10.0,
        value=8.5,
        step=0.1
    )

    fishing_duration_hours = st.number_input(
        "Fishing Duration (hours)",
        min_value=0.0,
        value=6.0,
        step=0.5
    )

    st.divider()

    analyze_button = st.button(
        "🔍 ANALYZE VESSEL RISK"
    )


# -----------------------------
# Map
# -----------------------------

st.header("🗺️ Marine Monitoring Map")

map_data = [
    {
        "lat": lat,
        "lon": lon
    }
]

st.map(
    map_data,
    zoom=6
)

st.caption(
    "📍 Vessel location based on entered telemetry. "
    "Live AIS, satellite and marine GIS observations "
    "can be integrated into this monitoring layer."
)


# -----------------------------
# AI Analysis
# -----------------------------

if analyze_button:

    # Features used by trained Random Forest model
    features = np.array([[
        speed_knots,
        ais_gap_hours,
        spoofed_identity,
        proximity_meters
    ]])

    # Predict IUU probability
    iuu_probability = model.predict_proba(features)[0][1]

    iuu_score = round(
        float(iuu_probability * 100),
        2
    )

    # Ecosystem vulnerability
    mpa_factor = 40 if in_mpa_zone else 0

    coral_factor = max(
        0,
        (5000 - coral_reef_proximity) / 5000
    ) * 30

    benthic_factor = (
        benthic_sensitivity / 10
    ) * 30

    ecosystem_score = min(
        100,
        mpa_factor +
        coral_factor +
        benthic_factor
    )

    # Intervention priority
    intervention_score = (
        0.6 * iuu_score
        +
        0.4 * ecosystem_score
    )

    intervention_score = round(
        intervention_score,
        2
    )

    # Priority
    if intervention_score >= 70:
        priority = "HIGH PRIORITY"
    elif intervention_score >= 40:
        priority = "MEDIUM PRIORITY"
    else:
        priority = "LOW PRIORITY"


    # -----------------------------
    # Summary
    # -----------------------------

    st.divider()

    st.header("📊 Risk Assessment Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        level, icon = get_risk_level(
            iuu_score
        )

        st.metric(
            label="⚠️ IUU Risk",
            value=f"{iuu_score:.1f}/100",
            delta=f"{icon} {level}"
        )

    with col2:

        level, icon = get_risk_level(
            ecosystem_score
        )

        st.metric(
            label="🌊 Ecosystem Vulnerability",
            value=f"{ecosystem_score:.1f}/100",
            delta=f"{icon} {level}"
        )

    with col3:

        level, icon = get_risk_level(
            intervention_score
        )

        st.metric(
            label="🎯 Intervention Priority",
            value=f"{intervention_score:.1f}/100",
            delta=f"{icon} {level}"
        )

    with col4:

        if priority == "HIGH PRIORITY":

            st.metric(
                label="🚨 Overall Status",
                value="HIGH",
                delta="🔴 Human Verification"
            )

        elif priority == "MEDIUM PRIORITY":

            st.metric(
                label="🚨 Overall Status",
                value="MEDIUM",
                delta="🟠 Investigation"
            )

        else:

            st.metric(
                label="🚨 Overall Status",
                value="LOW",
                delta="🟢 Routine Monitoring"
            )


    # -----------------------------
    # Gauges
    # -----------------------------

    st.divider()

    st.header("📈 AI Risk Analysis")

    chart1, chart2, chart3 = st.columns(3)

    with chart1:

        st.plotly_chart(
            create_gauge(
                iuu_score,
                "IUU Risk"
            ),
            use_container_width=True
        )

    with chart2:

        st.plotly_chart(
            create_gauge(
                ecosystem_score,
                "Ecosystem Vulnerability"
            ),
            use_container_width=True
        )

    with chart3:

        st.plotly_chart(
            create_gauge(
                intervention_score,
                "Intervention Priority"
            ),
            use_container_width=True
        )


    # -----------------------------
    # Decision
    # -----------------------------

    st.header("🚨 Intervention Decision")

    if priority == "HIGH PRIORITY":

        st.error(
            "🔴 HIGH PRIORITY — "
            "Human Verification Required"
        )

    elif priority == "MEDIUM PRIORITY":

        st.warning(
            "🟠 MEDIUM PRIORITY — "
            "Further Investigation Recommended"
        )

    else:

        st.success(
            "🟢 LOW PRIORITY — "
            "Routine Monitoring"
        )


    # -----------------------------
    # Vessel information
    # -----------------------------

    st.header("🚢 Vessel Detection & Status")

    info1, info2, info3 = st.columns(3)

    with info1:

        st.write(
            f"**Vessel ID:** {vessel_id}"
        )

        ais_status = (
            "AIS OFF (DARK VESSEL)"
            if ais_gap_hours > 1
            else "AIS ACTIVE"
        )

        st.write(
            f"**AIS Status:** {ais_status}"
        )

    with info2:

        mpa_status = (
            "INSIDE PROTECTED AREA"
            if in_mpa_zone == 1
            else "OUTSIDE PROTECTED AREA"
        )

        st.write(
            f"**Protected Area:** {mpa_status}"
        )

        st.write(
            f"**Speed:** {speed_knots} knots"
        )

    with info3:

        if intervention_score >= 70:

            st.write(
                "**Action Required:** 🔴 Human Verification"
            )

        else:

            st.write(
                "**Action Required:** 🟢 Routine Monitoring"
            )

        st.write(
            f"**Fishing Duration:** "
            f"{fishing_duration_hours} hours"
        )


    # -----------------------------
    # Risk Indicators
    # -----------------------------

    st.header("🔍 Risk Indicators Detected")

    indicators = []

    if ais_gap_hours > 1:

        indicators.append(
            "⚠️ Significant AIS gap detected"
        )

    if spoofed_identity == 1:

        indicators.append(
            "⚠️ Vessel identity anomaly detected"
        )

    if in_mpa_zone == 1:

        indicators.append(
            "🪸 Vessel is inside a Marine Protected Area"
        )

    if coral_reef_proximity < 500:

        indicators.append(
            "🪸 Vessel is close to a coral reef"
        )

    if proximity_meters < 500:

        indicators.append(
            "⚠️ Vessel is close to a protected or sensitive zone"
        )

    if fishing_duration_hours > 5:

        indicators.append(
            "🎣 Extended fishing activity detected"
        )

    if benthic_sensitivity >= 7:

        indicators.append(
            "🌊 High ecosystem sensitivity detected"
        )


    if len(indicators) == 0:

        st.success(
            "🟢 No major risk indicators detected."
        )

    else:

        for indicator in indicators:

            st.warning(indicator)


    # -----------------------------
    # Explainable AI
    # -----------------------------

    st.header(
        "🧠 Explainable AI — "
        "Why Was This Vessel Prioritized?"
    )

    explanation_parts = []

    if ais_gap_hours > 1:

        explanation_parts.append(
            f"AIS reporting gap of "
            f"{ais_gap_hours:.1f} hours"
        )

    if spoofed_identity == 1:

        explanation_parts.append(
            "identity anomaly"
        )

    if in_mpa_zone == 1:

        explanation_parts.append(
            "presence inside a Marine Protected Area"
        )

    if coral_reef_proximity < 500:

        explanation_parts.append(
            f"proximity to coral reef "
            f"({coral_reef_proximity:.0f} m)"
        )

    if proximity_meters < 500:

        explanation_parts.append(
            f"proximity to protected area "
            f"({proximity_meters:.0f} m)"
        )

    if fishing_duration_hours > 5:

        explanation_parts.append(
            f"extended fishing activity "
            f"({fishing_duration_hours:.1f} hours)"
        )

    if benthic_sensitivity >= 7:

        explanation_parts.append(
            "high ecosystem sensitivity"
        )


    if explanation_parts:

        st.info(
            "The system prioritized this vessel "
            "because the following risk signals "
            "were detected:\n\n"
            +
            "\n".join(
                ["• " + x for x in explanation_parts]
            )
        )

        st.write(
            "These signals contribute to the "
            "IUU Risk Score and Ecosystem "
            "Vulnerability Score. These scores "
            "are then combined into the "
            "Intervention Priority Score."
        )

    else:

        st.success(
            "No major risk indicators were "
            "triggered by the selected inputs."
        )


    # -----------------------------
    # Score explanation
    # -----------------------------

    st.header("📌 Risk Score Interpretation")

    r1, r2, r3 = st.columns(3)

    with r1:

        st.write("**IUU Risk Score**")

        st.write(
            "Measures the level of suspicious "
            "maritime behaviour using signals "
            "such as AIS gaps, identity anomalies "
            "and vessel behaviour."
        )

    with r2:

        st.write(
            "**Ecosystem Vulnerability Score**"
        )

        st.write(
            "Represents the sensitivity of the "
            "marine environment around the vessel, "
            "including protected and sensitive areas."
        )

    with r3:

        st.write(
            "**Intervention Priority Score**"
        )

        st.write(
            "Combines activity risk and ecosystem "
            "vulnerability to help prioritize "
            "incidents for investigation."
        )


    # -----------------------------
    # Decision flow
    # -----------------------------

    st.header("🔄 Blue Shield AI Decision Flow")

    f1, f2, f3, f4, f5 = st.columns(5)

    with f1:

        st.info(
            "🛰️ **DATA INPUT**\n\n"
            "AIS\nSatellite\nMarine GIS"
        )

    with f2:

        st.info(
            "🤖 **AI ANALYSIS**\n\n"
            "Behaviour\nIdentity\nAnomalies"
        )

    with f3:

        st.info(
            "⚠️ **RISK ASSESSMENT**\n\n"
            "IUU Risk\nRisk Signals"
        )

    with f4:

        st.info(
            "🌊 **ECOLOGICAL ASSESSMENT**\n\n"
            "MPA\nCoral Reef\nSensitivity"
        )

    with f5:

        st.info(
            "🎯 **PRIORITIZE**\n\n"
            "Priority Score\nHuman Verification"
        )


    # -----------------------------
    # Recommendation
    # -----------------------------

    st.divider()

    st.header("🛡️ Blue Shield AI Recommendation")

    if intervention_score >= 70:

        st.error(
            "🔴 **HIGH PRIORITY**\n\n"
            "Prioritize this incident for human "
            "verification and further investigation."
        )

    elif intervention_score >= 40:

        st.warning(
            "🟠 **MEDIUM PRIORITY**\n\n"
            "Further investigation and monitoring "
            "are recommended."
        )

    else:

        st.success(
            "🟢 **LOW PRIORITY**\n\n"
            "Continue routine monitoring."
        )


    st.info(
        "🛡️ **Decision-Support Disclaimer:** "
        "Blue Shield AI identifies potential "
        "high-risk maritime activity using "
        "available data signals. It does not "
        "declare a vessel illegal or establish "
        "guilt. Final enforcement decisions "
        "require human verification and "
        "appropriate evidence."
    )

else:

    st.info(
        "👈 Enter vessel telemetry in the "
        "sidebar and click **ANALYZE VESSEL RISK** "
        "to generate the Blue Shield AI "
        "risk assessment."
    )
