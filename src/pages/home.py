import streamlit as st
import base64
import matplotlib.pyplot as plt
from datetime import datetime

from src.services.space_weather_api import get_kp_forecast


def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def tile(title, image_path, key):
    img = get_base64(image_path)

    st.markdown(f"""
        <style>
        .tile-container {{
            position: relative;
            margin-bottom: 20px;
        }}

        .tile-{key} {{
            height: 160px;
            border-radius: 12px;
            background-image: url("data:image/jpg;base64,{img}");
            background-size: cover;
            background-position: center;
            position: relative;
            overflow: hidden;
        }}

        .overlay-{key} {{
            position: absolute;
            inset: 0;
            background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.85));
        }}

        .tile-title {{
            position: absolute;
            bottom: 15px;
            left: 18px;
            color: white;
            font-size: 18px;
        }}

        div[data-testid="stButton"] > button {{
            opacity: 0;
            height: 160px;
            width: 100%;
            position: absolute;
        }}
        </style>

        <div class="tile-container">
            <div class="tile-{key}">
                <div class="overlay-{key}">
                    <div class="tile-title">{title}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("", key=key):
        st.session_state["page"] = key


def render():
    times, values = get_kp_forecast()

    st.subheader("Geomagnetic Storm Forecast")

    if values and times:
        fig, ax = plt.subplots(figsize=(6, 1.8))

        x = list(range(len(values)))

        ax.bar(x, values)

        labels = []
        for t in times:
            try:
                dt = datetime.fromisoformat(t.replace("Z", ""))
                labels.append(dt.strftime("%H:%M"))
            except:
                labels.append("")

        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, fontsize=7)

        ax.set_ylim(0, 9)

        ax.set_ylabel("Kp", fontsize=8)
        ax.set_xlabel("UTC", fontsize=8)

        ax.tick_params(axis='y', labelsize=7)

        fig.tight_layout()

        st.pyplot(fig)
    else:
        st.warning("No NOAA forecast data available")

    col1, col2 = st.columns(2)

    with col1:
        tile("Space Weather Forecast", "graphics/space_weather.jpg", "space_weather")

    with col2:
        tile("Orbital Debris Reentry", "graphics/reentry.jpg", "reentry")

    col3, col4 = st.columns(2)

    with col3:
        tile("CDM", "graphics/cdm.png", "cdm")

    with col4:
        tile("Rocket Launch Monitoring", "graphics/rocket.jpg", "rocket")