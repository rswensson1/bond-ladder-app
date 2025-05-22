import streamlit as st
import requests
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt

load_dotenv()

# --- Simple Login Setup ---
USERNAME = os.getenv("APP_USERNAME", "brianna")
PASSWORD = os.getenv("APP_PASSWORD", "beacon123")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Login Required")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if "login_attempted" not in st.session_state:
        st.session_state.login_attempted = False

    if st.button("Login") or st.session_state.login_attempted:
        if username == USERNAME and password == PASSWORD:
            st.session_state.authenticated = True
        else:
            if not st.session_state.login_attempted:
                st.error("Invalid username or password")
        st.session_state.login_attempted = True
    if not st.session_state.authenticated:
        st.stop()

# --- Main App ---
st.title("Smart Treasury Ladder Builder - Prepared for Brianna Sprengel, Beacon Hill.")

investment_amount = st.number_input("Investment Amount ($)", min_value=1000, step=1000, value=100000)
ladder_years = st.slider("Ladder Duration (Years)", min_value=1, max_value=30, value=5)
reinvest = st.checkbox("Reinvest matured bonds (compounding interest)", value=False)

if st.button("Build Ladder"):
    payload = {
        "investment_amount": investment_amount,
        "ladder_years": ladder_years,
        "reinvest": reinvest
    }
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    try:
        response = requests.post(f"{backend_url}/build-ladder", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.subheader("Treasury Ladder Output")
            st.dataframe(data)

            # Plot yield curve with ladder overlay
            st.subheader("Yield Curve with Ladder Rungs")
            ladder_data = [row for row in data if row["maturity"] != "TOTAL"]
            labels = [row["maturity"] for row in ladder_data]
            yields = [row["yield_"] for row in ladder_data]

            plt.figure(figsize=(10, 5))
            plt.plot(labels, yields, marker='o', linestyle='-', label='Ladder Rungs')
            plt.xlabel("Maturity")
            plt.ylabel("Yield (%)")
            plt.title("Treasury Yield Curve with Ladder Rungs")
            plt.grid(True)
            plt.legend()
            st.pyplot(plt)
        else:
            st.error(f"Error: {response.status_code}")
    except Exception as e:
        st.error(f"Request failed: {e}")
