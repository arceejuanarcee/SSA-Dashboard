import streamlit as st

def render():
    st.title("Space Weather Forecast")

    st.write("Kp Index: 5.2")
    st.write("Condition: Geomagnetic Storm")
    st.write("Trend: Increasing")

    if st.button("Back"):
        st.session_state["page"] = "home"