import streamlit as st
import base64

def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def tile(title, image_path, key):
    img = get_base64(image_path)

    st.markdown(f"""
        <style>
        .tile-container {{
            position: relative;
        }}

        .tile-{key} {{
            height: 170px;
            border-radius: 10px;
            background-image: url("data:image/jpg;base64,{img}");
            background-size: cover;
            background-position: center;
            position: relative;
            cursor: pointer;
            overflow: hidden;
        }}

        .overlay-{key} {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(5, 15, 25, 0.75);
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .tile-text {{
            color: #e6f1f5;
            font-size: 20px;
            font-weight: 500;
        }}

        div[data-testid="stButton"] > button[kind="secondary"] {{
            opacity: 0;
            height: 170px;
            position: absolute;
            top: 0;
            left: 0;
        }}
        </style>

        <div class="tile-container">
            <div class="tile-{key}">
                <div class="overlay-{key}">
                    <div class="tile-text">{title}</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("", key=key):
        st.session_state["page"] = key


def render():

    col1, col2 = st.columns(2)

    with col1:
        tile("Space Weather Forecast", "graphics/space_weather.jpg", "space_weather")

    with col2:
        tile("Orbital Debris Reentry", "graphics/reentry.jpg", "reentry")

    col3, col4 = st.columns(2)

    with col3:
        tile("CDM", "graphics/cdm.jpg", "cdm")

    with col4:
        tile("Rocket Launch Monitoring", "graphics/rocket.jpg", "rocket")