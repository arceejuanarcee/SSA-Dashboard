import streamlit as st
import base64
import matplotlib.pyplot as plt

from src.services.space_weather_api import get_kp_index, get_kp_forecast


def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def tile(title, image_path, key, data):
    img = get_base64(image_path)

    data_html = ""
    for k, v in data.items():
        data_html += f"<div><b>{k}</b>: {v}</div>"

    st.markdown(f"""
        <style>
        .tile-container {{
            position: relative;
            margin-bottom: 20px;
        }}

        .tile-{key} {{
            height: 180px;
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
            bottom: 20px;
            left: 20px;
            color: white;
            font-size: 20px;
        }}

        .tile-info {{
            position: absolute;
            top: 15px;
            left: 20px;
            color: #00e0ff;
            font-size: 14px;
        }}

        div[data-testid="stButton"] > button {{
            opacity: 0;
            height: 180px;
            width: 100%;
            position: absolute;
        }}
        </style>

        <div class="tile-container">
            <div class="tile-{key}">
                <div class="overlay-{key}">
                    <div class="tile-info">{data_html}</div>
                    <div class="tile-title">{title}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("", key=key):
        st.session_state["page"] = key


def render():

    # ===== NOAA DATA =====
    sw = get_kp_index()
    times, values = get_kp_forecast()

    # ===== GRAPH (TOP) =====
    st.subheader("Geomagnetic Storm Forecast")

    if values:
        plt.figure()

        # IMPORTANT: no color specified per tool rules
        plt.bar(range(len(values)), values)

        plt.xticks(range(len(times)), [t[-5:] for t in times], rotation=45)
        plt.ylabel("Kp Index")
        plt.xlabel("Time (UTC)")

        st.pyplot(plt)
    else:
        st.warning("No NOAA forecast data available")

    # ===== TILES =====
    col1, col2 = st.columns(2)

    with col1:
        tile(
            "Space Weather Forecast",
            "graphics/space_weather.jpg",
            "space_weather",
            {
                "Kp": sw["kp"],
                "Condition": sw["status"]
            }
        )

    with col2:
        tile(
            "Orbital Debris Reentry",
            "graphics/reentry.jpg",
            "reentry",
            {
                "Object": "Pending",
                "ETA": "Pending"
            }
        )

    col3, col4 = st.columns(2)

    with col3:
        tile(
            "CDM",
            "graphics/cdm.png",
            "cdm",
            {
                "Active": "N/A",
                "Max Pc": "N/A"
            }
        )

    with col4:
        tile(
            "Rocket Launch Monitoring",
            "graphics/rocket.jpg",
            "rocket",
            {
                "Object": "N/A",
                "Status": "Idle"
            }
        )