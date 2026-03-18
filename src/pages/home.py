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
        return "#ff3b3b"

def tile(title, image_path, key, data, highlight=None, color="#00e0ff"):
    img = get_base64(image_path)

    data_html = ""
    for k, v in data.items():
        data_html += f"<div><b>{k}</b>: {v}</div>"

    highlight_html = ""
    if highlight:
        highlight_html = f"<div class='tile-highlight'>{highlight}</div>"

    st.markdown(f"""
        <style>
        .tile-container {{
            position: relative;
            margin-bottom: 20px;
        }}

        .tile-{key} {{
            height: 200px;
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
            font-weight: 500;
        }}

        .tile-info {{
            position: absolute;
            top: 15px;
            left: 20px;
            color: {color};
            font-size: 15px;
        }}

        .tile-highlight {{
            position: absolute;
            top: 15px;
            right: 20px;
            font-size: 28px;
            font-weight: bold;
            color: white;
        }}

        div[data-testid="stButton"] > button {{
            opacity: 0;
            height: 200px;
            width: 100%;
            position: absolute;
            top: 0;
            left: 0;
        }}
        </style>

        <div class="tile-container">
            <div class="tile-{key}">
                <div class="overlay-{key}">
                    <div class="tile-info">
                        {data_html}
                    </div>
                    {highlight_html}
                    <div class="tile-title">
                        {title}
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("", key=key):
        st.session_state["page"] = key


def render():

    sw = get_kp_index()
    kp = sw["kp"]
    status = sw["status"]
    kp_color = get_kp_color(kp)

    col1, col2 = st.columns(2)

    with col1:
        tile(
            "Space Weather Forecast",
            "graphics/space_weather.jpg",
            "space_weather",
            {
                "Kp Index": kp,
                "Geomagnetic": status
            },
            highlight=f"Kp {kp}",
            color=kp_color
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
            "graphics/cdm.jpg",
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