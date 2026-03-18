import streamlit as st
import base64

def get_base64_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def render_header():
    logo_base64 = get_base64_image("graphics/logo.png")

    st.markdown(f"""
        <style>
        .header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 80px;
            background-color: #1f5f75;
            display: flex;
            align-items: center;
            padding: 0 30px;
            z-index: 1000;
        }}

        .header-title {{
            color: white;
            font-size: 26px;
            font-weight: 500;
            margin-left: 20px;
        }}

        .logo {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            overflow: hidden;
            border: 2px solid #0b2e3c;
        }}

        .logo img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .page-content {{
            margin-top: 100px;
        }}

        .stApp {{
            background-color: #f2f2f2;
        }}
        </style>

        <div class="header">
            <div class="logo">
                <img src="data:image/png;base64,{logo_base64}">
            </div>
            <div class="header-title">
                Space Situational Awareness Dashboard
            </div>
        </div>

        <div class="page-content">
    """, unsafe_allow_html=True)