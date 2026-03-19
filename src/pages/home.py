import streamlit as st
import matplotlib.pyplot as plt

from src.services.space_weather_api import get_daily_kp
from src.services.spacetrack_api import get_active_leo_by_country


def tile(title, image_path, key):
    container = st.container()

    with container:
        st.image(image_path, use_container_width=True)

        st.markdown(f"""
        <div style="
            position:relative;
            margin-top:-60px;
            padding-left:12px;
            padding-bottom:8px;
            color:white;
            font-weight:500;
            font-size:16px;
        ">
            {title}
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open", key=key):
            st.session_state["page"] = key


def render():
    st.markdown("""
    <style>
    .block-container {
        padding-top: 0.2rem !important;
        padding-bottom: 0rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Geomagnetic Storm Forecast")

        try:
            days, values = get_daily_kp()

            if values:
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
                ax.tick_params(axis="x", rotation=15)

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