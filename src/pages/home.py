import streamlit as st
import base64
import matplotlib.pyplot as plt

from src.services.space_weather_api import get_daily_kp
from src.services.celestrak_api_api import get_active_leo_by_country


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
            margin-bottom: 0.4rem !important;
            font-size: 18px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3>Geomagnetic Storm Forecast</h3>", unsafe_allow_html=True)

        try:
            days, values = get_daily_kp()

            if values:
                fig, ax = plt.subplots(figsize=(6, 3))

                bars = ax.bar(days, values)

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

                for bar, color in zip(bars, colors):
                    bar.set_color(color)

                ax.set_ylim(0, 9)
                ax.set_ylabel("Kp Index (Geomagnetic Activity)", fontsize=10)

                ax.tick_params(axis="x", labelsize=9, rotation=0)
                ax.tick_params(axis="y", labelsize=9)

                for i, v in enumerate(values):
                    ax.text(i, v + 0.2, f"{v:.1f}", ha="center", fontsize=8)

                from matplotlib.patches import Patch
                legend_elements = [
                    Patch(facecolor="green", label="Quiet (0–2)"),
                    Patch(facecolor="yellow", label="Unsettled (3–4)"),
                    Patch(facecolor="orange", label="Active/Storm (5–6)"),
                    Patch(facecolor="red", label="Severe/Extreme (7–9)")
                ]
                ax.legend(handles=legend_elements, fontsize=7, loc="upper left")

                plt.tight_layout()
                st.pyplot(fig)

        except Exception:
            st.warning("Space weather unavailable")

    with col2:
        st.markdown("<h3>Top 10 Countries by Active LEO Satellites</h3>", unsafe_allow_html=True)

        try:
            labels, values, error = get_active_leo_by_country()

            if error:
                st.error(error)
            elif values:
                fig2, ax2 = plt.subplots(figsize=(6, 3))

                ax2.barh(labels, values)

                ax2.set_xlabel("Number of Active LEO Satellites", fontsize=10)
                ax2.tick_params(axis="x", labelsize=9)
                ax2.tick_params(axis="y", labelsize=9)

                for i, v in enumerate(values):
                    ax2.text(v + max(values)*0.01, i, str(v), va="center", fontsize=8)

                plt.tight_layout()
                st.pyplot(fig2)

        except Exception:
            st.warning("Satellite data unavailable")

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