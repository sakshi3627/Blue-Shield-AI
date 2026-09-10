import streamlit as st
import requests
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Blue Shield AI",
    page_icon="🌊",
    layout="wide"
)


# ============================================================
# PAGE STYLE
# ============================================================

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


# ============================================================
# HEADER
# ============================================================

st.title("🌊 Blue Shield AI")

st.subheader(
    "AI-Powered Maritime Risk & Marine Ecosystem Protection System"
)

st.write(
    "**Detect → Analyse → Assess → Prioritize → Verify**"
)

st.divider()


# ============================================================
# SIDEBAR INPUTS
# ============================================================

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


# ============================================================
# MAP
# ============================================================

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
    "AIS, satellite and marine GIS observations can be "
    "integrated into this monitoring layer."
)


# ============================================================
# RISK LEVEL FUNCTION
# ============================================================

def get_risk_level(score):

    if score >= 70:
        return "HIGH", "🔴"

    elif score >= 40:
        return "MEDIUM", "🟠"

    else:
        return "LOW", "🟢"


# ============================================================
# GAUGE CHART FUNCTION
# ============================================================

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
            title={
                "text": title
            },
            number={
                "suffix": "/100"
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "bar": {
                    "color": bar_color
                },
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
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        paper_bgcolor="white"
    )

    return fig


# ============================================================
# ANALYZE BUTTON
# ============================================================

if analyze_button:

    # --------------------------------------------------------
    # PAYLOAD
    # --------------------------------------------------------

    payload = {

        "vessel_id": vessel_id,

        "speed_knots": speed_knots,

        "ais_gap_hours": ais_gap_hours,

        "spoofed_identity": spoofed_identity,

        "proximity_meters": proximity_meters,

        "in_mpa_zone": in_mpa_zone,

        "coral_reef_proximity": coral_reef_proximity,

        "benthic_sensitivity": benthic_sensitivity,

        "fishing_duration_hours": fishing_duration_hours
    }


    # --------------------------------------------------------
    # CONNECT TO FASTAPI
    # --------------------------------------------------------

    try:

        response = requests.post(
            "http://localhost:8000/analyze-risk",
            json=payload,
            timeout=10
        )


        # ====================================================
        # SUCCESS
        # ====================================================

        if response.status_code == 200:

            result = response.json()


            # ------------------------------------------------
            # GET SCORES
            # ------------------------------------------------

            iuu_score = float(
                result["iuu_risk_score"]
            )

            ecosystem_score = float(
                result["ecosystem_vulnerability_score"]
            )

            intervention_score = float(
                result["intervention_priority_score"]
            )

            priority = result["priority_level"]


            # =================================================
            # RISK SUMMARY
            # =================================================

            st.divider()

            st.header("📊 Risk Assessment Summary")


            col1, col2, col3, col4 = st.columns(4)


            # IUU RISK
            with col1:

                level, icon = get_risk_level(
                    iuu_score
                )

                st.metric(
                    label="⚠️ IUU Risk",
                    value=f"{iuu_score:.1f}/100",
                    delta=f"{icon} {level}"
                )


            # ECOSYSTEM
            with col2:

                level, icon = get_risk_level(
                    ecosystem_score
                )

                st.metric(
                    label="🌊 Ecosystem Vulnerability",
                    value=f"{ecosystem_score:.1f}/100",
                    delta=f"{icon} {level}"
                )


            # INTERVENTION
            with col3:

                level, icon = get_risk_level(
                    intervention_score
                )

                st.metric(
                    label="🎯 Intervention Priority",
                    value=f"{intervention_score:.1f}/100",
                    delta=f"{icon} {level}"
                )


            # OVERALL STATUS
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


            # =================================================
            # AI RISK ANALYSIS
            # =================================================

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


            # =================================================
            # PRIORITY ALERT
            # =================================================

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


            # =================================================
            # VESSEL INFORMATION
            # =================================================

            st.header("🚢 Vessel Detection & Status")


            info1, info2, info3 = st.columns(3)


            with info1:

                st.write(
                    f"**Vessel ID:** {result['vessel_id']}"
                )

                st.write(
                    f"**AIS Status:** {result['ais_status']}"
                )


            with info2:

                st.write(
                    f"**Protected Area:** "
                    f"{result['mpa_status']}"
                )

                st.write(
                    f"**Speed:** "
                    f"{speed_knots} knots"
                )


            with info3:

                if result["action_required"]:

                    st.write(
                        "**Action Required:** "
                        "🔴 Human Verification"
                    )

                else:

                    st.write(
                        "**Action Required:** "
                        "🟢 Routine Monitoring"
                    )

                st.write(
                    f"**Fishing Duration:** "
                    f"{fishing_duration_hours} hours"
                )


            # =================================================
            # RISK INDICATORS
            # =================================================

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
                    "⚠️ Vessel is close to a protected "
                    "or sensitive zone"
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

                    st.warning(
                        indicator
                    )


            # =================================================
            # EXPLAINABLE AI
            # =================================================

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
                    + "\n".join(
                        [
                            "• " + x
                            for x in explanation_parts
                        ]
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
                    "No major risk indicators were triggered "
                    "by the selected inputs."
                )


            # =================================================
            # SCORE INTERPRETATION
            # =================================================

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


            # =================================================
            # DECISION FLOW
            # =================================================

            st.header(
                "🔄 Blue Shield AI Decision Flow"
            )


            f1, f2, f3, f4, f5 = st.columns(5)


            with f1:

                st.info(
                    "🛰️ **DATA INPUT**\n\n"
                    "AIS\n"
                    "Satellite\n"
                    "Marine GIS"
                )


            with f2:

                st.info(
                    "🤖 **AI ANALYSIS**\n\n"
                    "Behaviour\n"
                    "Identity\n"
                    "Anomalies"
                )


            with f3:

                st.info(
                    "⚠️ **RISK ASSESSMENT**\n\n"
                    "IUU Risk\n"
                    "Risk Signals"
                )


            with f4:

                st.info(
                    "🌊 **ECOLOGICAL ASSESSMENT**\n\n"
                    "MPA\n"
                    "Coral Reef\n"
                    "Sensitivity"
                )


            with f5:

                st.info(
                    "🎯 **PRIORITIZE**\n\n"
                    "Priority Score\n"
                    "Human Verification"
                )


            # =================================================
            # FINAL RECOMMENDATION
            # =================================================

            st.divider()

            st.header(
                "🛡️ Blue Shield AI Recommendation"
            )


            if intervention_score >= 70:

                st.error(
                    "🔴 **HIGH PRIORITY**\n\n"
                    "Prioritize this incident for "
                    "human verification and further investigation."
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


            # =================================================
            # DISCLAIMER
            # =================================================

            st.info(
                "🛡️ **Decision-Support Disclaimer:** "
                "Blue Shield AI identifies potential "
                "high-risk maritime activity using available "
                "data signals. It does not declare a vessel "
                "illegal or establish guilt. Final enforcement "
                "decisions require human verification and "
                "appropriate evidence."
            )


        # ====================================================
        # API ERROR
        # ====================================================

        else:

            st.error(
                f"❌ API returned status code "
                f"{response.status_code}"
            )

            st.code(
                response.text
            )


    # ========================================================
    # CONNECTION ERROR
    # ========================================================

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to the FastAPI backend."
        )

        st.info(
            "Make sure Terminal 1 is running FastAPI."
        )

        st.code(
            "uvicorn app:app --reload --port 8000"
        )


    # ========================================================
    # TIMEOUT ERROR
    # ========================================================

    except requests.exceptions.Timeout:

        st.error(
            "❌ FastAPI took too long to respond."
        )


    # ========================================================
    # OTHER ERROR
    # ========================================================

    except Exception as e:

        st.error(
            f"❌ Unexpected error: {e}"
        )


# ============================================================
# BEFORE ANALYSIS
# ============================================================

else:

    st.info(
        "👈 Enter the vessel telemetry in the sidebar "
        "and click **ANALYZE VESSEL RISK** to generate "
        "the Blue Shield AI risk assessment."
    )