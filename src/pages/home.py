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


def render():
    # MAXIMUM SPACING COMPRESSION
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

        div[data-testid="stVerticalBlock"] > div {
            gap: 0.2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # TITLE (VERY TIGHT)
    st.markdown("<h3>Geomagnetic Storm Forecast</h3>", unsafe_allow_html=True)

    # COLUMNS
    graph_col, next_graph_col = st.columns(2)

    with graph_col:
        try:
            days, values = get_daily_kp()

            if values:
                fig, ax = plt.subplots(figsize=(5.2, 2.4))

                bars = ax.bar(days, values)

                # COLOR LOGIC
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

                # REMOVE EXTRA TOP SPACE INSIDE PLOT
                ax.margins(y=0.05)

                ax.tick_params(axis="x", labelsize=8)
                ax.tick_params(axis="y", labelsize=8)

                # VALUE LABELS
                for i, v in enumerate(values):
                    ax.text(i, v + 0.1, f"{v:.1f}", ha="center", fontsize=8)

                # CRITICAL: REMOVE FIG PADDING
                plt.subplots_adjust(top=0.95, bottom=0.2)

                st.pyplot(fig, use_container_width=True)

            else:
                st.warning("No NOAA data available")

        except Exception:
            st.warning("Space weather data unavailable")

    # SECOND GRAPH SPACE
    with next_graph_col:
        st.empty()

    # TILES
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