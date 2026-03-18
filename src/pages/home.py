import streamlit as st
import base64
import matplotlib.pyplot as plt

from src.services.space_weather_api import get_daily_kp


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
    st.subheader("Geomagnetic Storm Forecast")

    days, values = get_daily_kp()

    if values:
        fig, ax = plt.subplots(figsize=(5, 2.5))

        bars = ax.bar(days, values)

        for i, v in enumerate(values):
            if v < 3:
                bars[i].set_color("green")
            elif v < 5:
                bars[i].set_color("yellow")
            elif v < 7:
                bars[i].set_color("orange")
            else:
                bars[i].set_color("red")

        ax.set_ylim(0, 9)

        for i, v in enumerate(values):
            ax.text(i, v + 0.2, f"{v:.1f}", ha='center', fontsize=7)

        ax.tick_params(axis='x', labelsize=8)

        fig.tight_layout()

        col1, col2 = st.columns([1,1])
        with col1:
            st.pyplot(fig)
    else:
        st.warning("No NOAA data available")

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