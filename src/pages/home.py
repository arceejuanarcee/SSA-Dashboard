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


def render():
    # FIX GLOBAL SPACING
    st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # TITLE (tight spacing)
    st.markdown(
        "<h3 style='margin-bottom:0.4rem;'>Geomagnetic Storm Forecast</h3>",
        unsafe_allow_html=True
    )

    # GRAPH LAYOUT (HALF WIDTH)
    graph_col, next_graph_col = st.columns(2)

    with graph_col:
        try:
            days, values = get_daily_kp()

            if values:
                fig, ax = plt.subplots(figsize=(5.2, 2.6))

                bars = ax.bar(days, values)

                # COLOR CODING
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
                ax.set_ylabel("Kp Index", fontsize=9)

                ax.tick_params(axis="x", labelsize=8)
                ax.tick_params(axis="y", labelsize=8)

                # VALUE LABELS
                for i, v in enumerate(values):
                    ax.text(i, v + 0.15, f"{v:.1f}", ha="center", fontsize=8)

                fig.tight_layout()
                st.pyplot(fig)

            else:
                st.warning("No NOAA data available")

        except Exception:
            st.warning("Space weather data unavailable")

    # RESERVED SPACE FOR SECOND GRAPH
    with next_graph_col:
        st.empty()

    # TILES SECTION
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