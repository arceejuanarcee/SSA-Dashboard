import streamlit as st
from src.components.tile import tile

def render():
    st.markdown("""
        <style>
        .tile-container {
            display: flex;
            justify-content: space-around;
            margin-top: 60px;
        }

        .tile-row {
            display: flex;
            justify-content: space-around;
            margin-top: 60px;
        }

        .stButton button {
            height: 140px;
            font-size: 20px;
            background-color: #1f5f75;
            color: white;
            border: 2px solid #0b2e3c;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        tile("Space Weather Forecast", "space_weather")

    with col2:
        tile("Orbital Debris Reentry", "reentry")

    col3, col4 = st.columns(2)

    with col3:
        tile("CDM", "cdm")

    with col4:
        tile("Rocket Launch Monitoring", "rocket")