import base64
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components

from src.services.space_weather_api import get_daily_kp
from src.services.spacetrack_api import get_active_leo_by_country


def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def tile(title, image_path, page_key, height=220):
    img_b64 = get_base64(image_path)

    html = f"""
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                background: transparent;
                overflow: hidden;
            }}

            .tile {{
                position: relative;
                width: 100%;
                height: {height}px;
                border-radius: 14px;
                overflow: hidden;
                cursor: pointer;
                background-image: url("data:image/jpeg;base64,{img_b64}");
                background-size: cover;
                background-position: center;
                font-family: Arial, sans-serif;
            }}

            .overlay {{
                position: absolute;
                inset: 0;
                background: linear-gradient(
                    to top,
                    rgba(0, 0, 0, 0.78) 0%,
                    rgba(0, 0, 0, 0.30) 55%,
                    rgba(0, 0, 0, 0.18) 100%
                );
            }}

            .title {{
                position: absolute;
                left: 16px;
                bottom: 14px;
                color: white;
                font-size: 16px;
                font-weight: 600;
                line-height: 1.2;
                text-shadow: 0 1px 2px rgba(0,0,0,0.6);
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
                try {{
                    const url = new URL(window.parent.location.href);
                    url.searchParams.set("page", "{page_key}");
                    window.parent.location.href = url.toString();
                }} catch (e) {{
                    try {{
                        const url = new URL(window.top.location.href);
                        url.searchParams.set("page", "{page_key}");
                        window.top.location.href = url.toString();
                    }} catch (err) {{}}
                }}
            }}
        </script>
    </body>
    </html>
    """

    components.html(html, height=height, scrolling=False)


def render():
    st.markdown("""
    <style>
    .block-container {
        padding-top: 0.15rem !important;
        padding-bottom: 0rem !important;
    }

    h3 {
        margin-top: 0rem !important;
        margin-bottom: 0.35rem !important;
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

    with col2:
        st.markdown("<h3>Top 10 Countries by Active LEO Satellites</h3>", unsafe_allow_html=True)

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

    st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)

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