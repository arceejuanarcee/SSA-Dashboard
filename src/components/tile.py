import streamlit as st

def tile(title, key):
    if st.button(title, key=key, use_container_width=True):
        st.session_state["page"] = key