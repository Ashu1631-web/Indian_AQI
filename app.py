import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="India AQI Dashboard 🌍",
    page_icon="🌫️",
    layout="wide"
)

# =====================================
# CITY FAMOUS PLACE ICONS 🏙️
# =====================================
city_icons = {
    "Delhi": "🏛️ India Gate",
    "Mumbai": "🌊 Gateway of India",
    "Jaipur": "🕌 Hawa Mahal",
    "Agra": "🏰 Taj Mahal",
    "Kolkata": "🌉 Howrah Bridge",
    "Chennai": "🛕 Marina Temple",
    "Bengaluru": "🌳 Lalbagh Garden",
    "Hyderabad": "🕌 Charminar",
    "Pune": "🏯 Shaniwar Wada",
    "Ahmedabad": "🕌 Sabarmati Ashram",
    "Lucknow": "🕌 Bara Imambara",
    "Varanasi": "🕉️ Ganga Ghats",
    "Amritsar": "🛕 Golden Temple",
    "Goa": "🏖️ Beach Paradise",
    "Indore": "🍲 Street Food Hub"
}

# =====================================
# LOAD DATA
# =====================================
@st.cache_data
def load_data():
    df = pd.read_csv("india_city_aqi_2
