import streamlit as st
import base64

def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def tile(title, image_path, key):
    img = get_base64(image_path)

    st.markdown(f"""
        <style>
        .tile-{key} {{
            height: 160px;
            border-radius: 8px;
            background-image: url("data:image/jpg;base64,{img}");
            background-size: cover;
            background-position: center;
            position: relative;
            border: 2px solid #0a2c3a;
            cursor: pointer;
            transition: transform 0.2s ease;
        }}

        .tile-{key}:hover {{
            transform: scale(1.02);
        }}

        .overlay-{key} {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(11, 61, 92, 0.75);
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
        }}

        .tile-text {{
            color: white;
            font-size: 20px;
            font-weight: 500;
            text-align: center;
        }}
        </style>

        <div class="tile-{key}" onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', value: '{key}'}}, '*');">
            <div class="overlay-{key}">
                <div class="tile-text">{title}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("hidden", key=key):
        st.session_state["page"] = key


def render():

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