import streamlit as st
import base64
import matplotlib.pyplot as plt

from src.services.space_weather_api import get_daily_kp
from src.services.spacetrack_api import get_active_leo_by_country


def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def tile(title, image_path, key):
    img = get_base64(image_path)

    st.markdown(f"""
    <style>
    .tile-wrapper-{key} {{
        position: relative;
        height: 160px;
        margin-bottom: 16px;
    }}

    .tile-{key} {{
        height: 100%;
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

    .tile-title-{key} {{
        position: absolute;
        bottom: 12px;
        left: 16px;
        color: white;
        font-size: 16px;
        font-weight: 500;
    }}
    </style>

    <div class="tile-wrapper-{key}">
        <div class="tile-{key}">
            <div class="overlay-{key}">
                <div class="tile-title-{key}">{title}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("", key=f"btn_{key}"):
        st.session_state["page"] = key


def render():
    st.markdown("""
    <style>
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Geomagnetic Storm Forecast")

        try:
            days, values = get_daily_kp()

            if not values:
                st.warning("No Kp data available")
            else:
                fig, ax = plt.subplots(figsize=(6, 3))

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

                ax.set_ylabel("Kp Index")
                ax.set_ylim(0, 9)
                ax.tick_params(axis="x", rotation=20)

                for i, v in enumerate(values):
                    ax.text(i, v + 0.2, f"{v:.1f}", ha="center", fontsize=8)

                from matplotlib.patches import Patch
                ax.legend(handles=[
                    Patch(color='green', label='Quiet'),
                    Patch(color='yellow', label='Unsettled'),
                    Patch(color='orange', label='Active'),
                    Patch(color='red', label='Storm')
                ], fontsize=7)

                plt.tight_layout()
                st.pyplot(fig)

        except Exception as e:
            st.error(str(e))

    with col2:
        st.subheader("Top 10 Countries by Active LEO Satellites")

        labels, values, error = get_active_leo_by_country()

        if error:
            st.error(error)
        elif values:
            fig2, ax2 = plt.subplots(figsize=(6, 3))

            ax2.barh(labels, values)
            ax2.set_xlabel("Number of Satellites")
            ax2.set_xlim(0, max(values) * 1.2)

            for i, v in enumerate(values):
                ax2.text(v + max(values) * 0.02, i, str(v), va='center')

            plt.tight_layout()
            st.pyplot(fig2)

    st.markdown("<br>", unsafe_allow_html=True)

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