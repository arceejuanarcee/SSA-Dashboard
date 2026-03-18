import streamlit as st
from src.services.space_weather_api import get_kp_index

def render():
    st.title("Space Weather Details")

    sw = get_kp_index()

    st.write(f"Kp Index: {sw['kp']}")
    st.write(f"Condition: {sw['status']}")

    if st.button("Back"):
        st.session_state["page"] = "home"