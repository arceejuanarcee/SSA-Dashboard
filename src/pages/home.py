import streamlit as st
import base64
import matplotlib.pyplot as plt

from src.services.space_weather_api import get_daily_kp
from src.services.spacetrack_api import get_active_leo_satellites_by_country


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

        div[data-testid="stButton"] > button {{
            opacity: 0;
            height: 160px;
            width: 100%;
            position: absolute;
            top: 0;
            left: 0;
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


def spacer(height="2rem"):
    st.markdown(f"<div style='margin-top:{height};'></div>", unsafe_allow_html=True)


def render():
    st.markdown("""
        <style>
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 0rem;
        }

        h3 {
            margin-top: 0rem !important;
            margin-bottom: 0.2rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h3>Geomagnetic Storm Forecast</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        try:
            days, values = get_daily_kp()

            if values:
                fig, ax = plt.subplots(figsize=(5.2, 2.4))
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
                ax.tick_params(axis="x", labelsize=8)

                for i, v in enumerate(values):
                    ax.text(i, v + 0.1, f"{v:.1f}", ha="center", fontsize=8)

                plt.subplots_adjust(top=0.95, bottom=0.2)

                st.pyplot(fig, use_container_width=True)

        except Exception:
            st.warning("Space weather unavailable")

    with col2:
        st.markdown("<h3 style='font-size:16px;'>Top 10 Countries by Active LEO Satellites</h3>", unsafe_allow_html=True)

        try:
            identity = st.secrets["spacetrack"]["identity"]
            password = st.secrets["spacetrack"]["password"]

            labels, values, err = get_active_leo_satellites_by_country(identity, password)

            if err:
                st.error(err)

            elif values:
                fig2, ax2 = plt.subplots(figsize=(5.2, 2.4))

                bars = ax2.bar(labels, values)

                ax2.set_ylabel("Satellites", fontsize=8)
                ax2.tick_params(axis="x", rotation=45, labelsize=8)

                for i, v in enumerate(values):
                    ax2.text(i, v, str(v), ha="center", fontsize=7)

                plt.subplots_adjust(top=0.9, bottom=0.3)

                st.pyplot(fig2, use_container_width=True)

            else:
                st.warning("No data available")

        except Exception as e:
            st.error(f"Space-Track error: {e}")

    spacer("2.5rem")

    t1, t2 = st.columns(2)

    with t1:
        tile("Space Weather Forecast", "graphics/space_weather.jpg", "space_weather")

    with t2:
        tile("Orbital Debris Reentry", "graphics/reentry.jpg", "reentry")

    t3, t4 = st.columns(2)

    with t3:
        tile("CDM", "graphics/cdm.png", "cdm")

    with t4:
        tile("Rocket Launch Monitoring", "graphics/rocket.jpg", "rocket")