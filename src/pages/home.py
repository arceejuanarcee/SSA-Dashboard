import streamlit as st
import base64
from src.services.space_weather_api import get_kp_index

def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_kp_color(kp):
    if kp == "N/A":
        return "#aaaaaa"
    if kp < 4:
        return "#00ff88"
    elif kp < 5:
        return "#ffee00"
    else:
        return "#ff4c4c"

def tile(title, image_path, key, data, color="#00e0ff"):
    img = get_base64(image_path)

    data_html = ""
    for k, v in data.items():
        data_html += f"<div>{k}: {v}</div>"

    st.markdown(f"""
        <style>
        .tile-container {{
            position: relative;
        }}

        .tile-{key} {{
            height: 180px;
            border-radius: 10px;
            background-image: url("data:image/jpg;base64,{img}");
            background-size: cover;
            background-position: center;
            position: relative;
            overflow: hidden;
        }}

        .overlay-{key} {{
            position: absolute;
            inset: 0;
            background: rgba(5, 15, 25, 0.75);
        }}

        .tile-title {{
            position: absolute;
            bottom: 20px;
            left: 20px;
            color: #e6f1f5;
            font-size: 20px;
        }}

        .tile-info {{
            position: absolute;
            top: 15px;
            left: 20px;
            color: {color};
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

    sw = get_kp_index()
    kp_color = get_kp_color(sw["kp"])

    col1, col2 = st.columns(2)

    with col1:
        tile(
            "Space Weather Forecast",
            "graphics/space_weather.jpg",
            "space_weather",
            {
                "Kp": sw["kp"],
                "Condition": sw["status"]
            },
            kp_color
        )

    with col2:
        tile(
            "Orbital Debris Reentry",
            "graphics/reentry.jpg",
            "reentry",
            {
                "Object": "N/A",
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