import streamlit as st

def render_header():
    st.markdown("""
        <style>
        .header {
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
        }

        .header-title {
            color: white;
            font-size: 26px;
            font-weight: 500;
            margin-left: 20px;
        }

        .logo {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: 2px solid #0b2e3c;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }

        .page-content {
            margin-top: 100px;
        }
        </style>

        <div class="header">
            <div class="logo">Logo</div>
            <div class="header-title">
                Space Situational Awareness Dashboard
            </div>
        </div>

        <div class="page-content">
    """, unsafe_allow_html=True)