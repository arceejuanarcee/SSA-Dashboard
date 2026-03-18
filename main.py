import streamlit as st

st.set_page_config(
    page_title="SSA Dashboard",
    layout="wide"
)

st.title("SSA Dashboard")
st.caption("Space Situational Awareness System")

status_col1, status_col2, status_col3 = st.columns(3)

status_col1.metric("System Status", "Operational")
status_col2.metric("Last Update", "2026-03-18 09:00 UTC")
status_col3.metric("Data Sources", "NOAA | Space-Track | Celestrak")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Space Weather")
    st.metric("Kp Index", "5.2")
    st.write("Condition: Geomagnetic Storm")
    st.write("Trend: Increasing")

with col2:
    st.subheader("Orbital Debris Reentry")
    st.write("Object ID: 54231")
    st.write("Reentry Window: 03:39 – 04:27 UTC")
    st.write("Uncertainty: ±24 minutes")
    st.button("Open Prediction")

col3, col4 = st.columns(2)

with col3:
    st.subheader("CDM Monitoring")
    st.metric("Active Conjunctions", "3")
    st.write("Maximum Collision Probability: 2.3e-4")
    st.write("Risk Level: Medium")

with col4:
    st.subheader("Rocket Debris Monitoring")
    st.write("Latest Object: CZ-6A Debris")
    st.write("Orbit Status: Decaying")
    st.write("Tracking: Active")

left_panel, right_panel = st.columns(2)

with left_panel:
    st.subheader("Activity Feed")
    st.text(
        "[08:12] New TIP detected – Object 54231\n"
        "[08:05] Kp Index increased to storm level\n"
        "[07:50] CDM update – elevated probability"
    )

with right_panel:
    st.subheader("Risk Summary")
    st.write(
        "- Elevated geomagnetic activity may increase atmospheric drag\n"
        "- One object with narrow reentry uncertainty window\n"
        "- No critical conjunction threats at this time"
    )