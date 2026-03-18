import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("."))

from src.components.header import render_header
from src.utils.navigation import init_navigation, navigate

import src.pages.home as home
import src.pages.space_weather as space_weather
import src.pages.reentry as reentry
import src.pages.cdm as cdm
import src.pages.rocket as rocket

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