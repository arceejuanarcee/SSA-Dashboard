import streamlit as st
import base64
import matplotlib.pyplot as plt

from src.services.space_weather_api import get_daily_kp
from src.services.spacetrack_api import get_active_leo_by_country
from src.services.launch_scraper import fetch_china_launches


def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def tile(title, image_path, key):
    img = get_base64(image_path)

    st.markdown(f"""
        <style>
        .tile-container {{
            position: relative;
            margin-bottom: 16px;
        }}

        .tile-{key} {{
            height: 160px;
            border-radius: 12px;
            background-image: url("data:image/jpg;base64,{img}");
            background-size: cover;
            background-position: center;
            position: relative;
            overflow: hidden;
            cursor: pointer;
        }}

        .overlay-{key} {{
            position: absolute;
            inset: 0;
            background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.85));
        }}

        .tile-title {{
            position: absolute;
            bottom: 12px;
            left: 16px;
            color: white;
            font-size: 17px;
            font-weight: 500;
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


def render():
    st.markdown("""
        <style>
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 0rem;
        }

        h3 {
            margin-top: 0rem !important;
            margin-bottom: 0.3rem !important;
            font-size: 18px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3>Geomagnetic Storm Forecast</h3>", unsafe_allow_html=True)

        try:
            days, values = get_daily_kp()

            fig, ax = plt.subplots(figsize=(6, 3))

            colors = []
            for v in values:
                if v < 3:
                    colors.append("green")
                elif v < 5:
                    colors.append("yellow")
                elif v < 7:
                    colors.append("orange")
                else:
                    colors.append("red")

            bars = ax.bar(days, values, color=colors)

            ax.set_ylabel("Kp Index", fontsize=10)
            ax.tick_params(axis="x", rotation=20, labelsize=8)

            for i, v in enumerate(values):
                ax.text(i, v + 0.1, f"{v:.1f}", ha="center", fontsize=8)

            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='green', label='Quiet'),
                Patch(facecolor='yellow', label='Unsettled'),
                Patch(facecolor='orange', label='Active'),
                Patch(facecolor='red', label='Storm')
            ]
            ax.legend(handles=legend_elements, fontsize=8)

            st.pyplot(fig, use_container_width=True)

        except Exception:
            st.warning("Space weather unavailable")

    with col2:
        st.markdown("<h3>Top 10 Countries by Active LEO Satellites</h3>", unsafe_allow_html=True)

        try:
            labels, values = get_active_leo_by_country()

            fig2, ax2 = plt.subplots(figsize=(6, 3))

            ax2.barh(labels, values)

            ax2.set_xlabel("Number of Satellites", fontsize=10)
            ax2.tick_params(axis="y", labelsize=9)

            for i, v in enumerate(values):
                ax2.text(v + 50, i, str(v), va="center", fontsize=8)

            st.pyplot(fig2, use_container_width=True)

        except Exception:
            st.warning("Satellite data unavailable")

    st.markdown("<h3>Upcoming Launches (China CASC)</h3>", unsafe_allow_html=True)

    launches, error = fetch_china_launches()

    if error:
        st.error(error)

    elif launches:
        for launch in launches:
            st.markdown(f"""
            <div style="
                background:#ffffff;
                border-radius:10px;
                padding:12px 14px;
                margin-bottom:8px;
                color:#000;
                box-shadow:0 2px 6px rgba(0,0,0,0.2);
            ">
                <div style="font-weight:600; font-size:14px;">
                    {launch['rocket']}
                </div>

                <div style="font-size:12px; margin-top:4px;">
                    {launch['date']}
                </div>

                <div style="font-size:11px; color:#444; margin-top:2px;">
                    {launch['site']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.warning("No upcoming launches")

    t1, t2 = st.columns(2)

    with t1:
        tile("Space Weather Monitoring", "graphics/space_weather.jpg", "space_weather")

    with t2:
        tile("Orbital Debris Reentry", "graphics/reentry.jpg", "reentry")

    t3, t4 = st.columns(2)

    with t3:
        tile("CDM", "graphics/cdm.png", "cdm")

    with t4:
        tile("Rocket Launch Monitoring", "graphics/rocket.jpg", "rocket")