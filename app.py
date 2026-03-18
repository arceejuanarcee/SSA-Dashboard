import streamlit as st

from src.components.header import render_header
from src.utils.navigation import init_navigation, navigate

from src.pages import home, space_weather, reentry, cdm, rocket

st.set_page_config(layout="wide")

init_navigation()
render_header()

page = navigate()

if page == "home":
    home.render()

elif page == "space_weather":
    space_weather.render()

elif page == "reentry":
    reentry.render()

elif page == "cdm":
    cdm.render()

elif page == "rocket":
    rocket.render()

st.markdown("</div>", unsafe_allow_html=True)