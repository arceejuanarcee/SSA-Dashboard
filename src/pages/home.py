import base64
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components

from src.services.space_weather_api import get_daily_kp
from src.services.spacetrack_api import get_active_leo_by_country
from src.services.launch_scraper import fetch_china_launches


def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def tile(title, image_path, page_key, height=220):
    img_b64 = get_base64(image_path)

    components.html(f"""
    <html>
    <head>
    <style>
        body {{
            margin:0;
            padding:0;
            background:transparent;
            overflow:hidden;
        }}

        .tile {{
            position:relative;
            width:100%;
            height:{height}px;
            border-radius:14px;
            overflow:hidden;
            cursor:pointer;
            background-image:url("data:image/jpeg;base64,{img_b64}");
            background-size:cover;
            background-position:center;
        }}

        .overlay {{
            position:absolute;
            inset:0;
            background:linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.8));
        }}

        .title {{
            position:absolute;
            bottom:14px;
            left:16px;
            color:white;
            font-size:16px;
            font-weight:600;
        }}
    </style>
    </head>

    <body>
        <div class="tile" onclick="goToPage()">
            <div class="overlay"></div>
            <div class="title">{title}</div>
        </div>

        <script>
        function goToPage() {{
            const url = new URL(window.parent.location.href);
            url.searchParams.set("page", "{page_key}");
            window.parent.location.href = url.toString();
        }}
        </script>
    </body>
    </html>
    """, height=height)


def render():
    st.markdown("""
    <style>
    .block-container {
        padding-top: 0.1rem !important;
        padding-bottom: 0rem !important;
    }

    h3 {
        margin-top: 0rem !important;
        margin-bottom: 0.25rem !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    page_from_query = st.query_params.get("page")
    if page_from_query:
        st.session_state["page"] = page_from_query

    col1, col2 = st.columns(2)

    # LEFT: GEOMAGNETIC GRAPH + LAUNCHES
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

                for bar, c in zip(bars, colors):
                    bar.set_color(c)

                ax.set_ylabel("Kp Index")
                ax.set_ylim(0, 9)
                ax.tick_params(axis="x", rotation=15, labelsize=9)
                ax.tick_params(axis="y", labelsize=9)

                for i, v in enumerate(values):
                    ax.text(i, v + 0.15, f"{v:.1f}", ha="center", fontsize=8)

                from matplotlib.patches import Patch
                ax.legend(
                    handles=[
                        Patch(color="green", label="Quiet"),
                        Patch(color="yellow", label="Unsettled"),
                        Patch(color="orange", label="Active"),
                        Patch(color="red", label="Storm"),
                    ],
                    fontsize=7,
                    loc="upper right",
                )

                plt.tight_layout()
                st.pyplot(fig, width="stretch")

            else:
                st.warning("No Kp data available.")

        except Exception as e:
            st.error(str(e))

        st.markdown("<h3>Upcoming Launches (China CASC)</h3>", unsafe_allow_html=True)

        launches, error = fetch_china_launches()

        if error:
            st.error(error)

        elif launches:
            fig3, ax3 = plt.subplots(figsize=(6, 3))
            ax3.axis("off")

            y_positions = list(range(len(launches)))[::-1]

            for i, launch in enumerate(launches):
                rocket = launch.get("rocket", "Unknown")
                date = launch.get("date", "TBD")
                site = launch.get("site", "Unknown Site")

                text = f"{rocket}\n{date}\n{site}"

                ax3.text(
                    0.02,
                    y_positions[i],
                    text,
                    fontsize=9,
                    va="center"
                )

            ax3.set_xlim(0, 1)
            ax3.set_ylim(-1, len(launches))

            plt.tight_layout()
            st.pyplot(fig3, width="stretch")

        else:
            st.warning("No upcoming launches")

    # RIGHT: SATELLITES GRAPH
    with col2:
        st.markdown("<h3>Top Countries by Active LEO Satellites</h3>", unsafe_allow_html=True)

        try:
            labels, values, error = get_active_leo_by_country()

            if error:
                st.error(error)

            elif values:
                fig2, ax2 = plt.subplots(figsize=(6, 3))

                ax2.barh(labels, values)

                ax2.set_xlabel("Number of Satellites")
                ax2.set_xlim(0, max(values) * 1.2)

                ax2.tick_params(axis="x", labelsize=9)
                ax2.tick_params(axis="y", labelsize=9)

                for i, v in enumerate(values):
                    ax2.text(v + max(values) * 0.02, i, str(v), va="center", fontsize=8)

                plt.tight_layout()
                st.pyplot(fig2, width="stretch")

            else:
                st.warning("No satellite data available.")

        except Exception as e:
            st.error(str(e))

    st.markdown("<div style='margin-top:0.3rem;'></div>", unsafe_allow_html=True)

    t1, t2 = st.columns(2)

    with t1:
        tile("Space Weather Monitoring", "graphics/space_weather.jpg", "space_weather")

    with t2:
        tile("Orbital Debris Reentry", "graphics/reentry.jpg", "reentry")

    t3, t4 = st.columns(2)

    with t3:
        tile("Conjunction Analysis", "graphics/cdm.png", "cdm")

    with t4:
        tile("Rocket Launch Monitoring", "graphics/rocket.jpg", "rocket")