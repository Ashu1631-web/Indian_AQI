import streamlit as st
import pandas as pd
import plotly.express as px

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
    df = pd.read_csv("india_city_aqi_2015_2023.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# =====================================
# SIDEBAR FILTERS
# =====================================
st.sidebar.title("🌍 AQI Dashboard Filters")

city = st.sidebar.selectbox("🏙️ Select City", df["city"].unique())

date_range = st.sidebar.date_input(
    "📅 Select Date Range",
    [df["date"].min(), df["date"].max()]
)

start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

filtered = df[
    (df["city"] == city) &
    (df["date"] >= start_date) &
    (df["date"] <= end_date)
]

# =====================================
# HEADER
# =====================================
place_name = city_icons.get(city, "🏙️ Famous City Spot")

st.title("🌫️ India Air Quality Analytics Dashboard")
st.markdown(f"## {place_name}")
st.markdown("### Professional Dashboard with 15 Graphs + Insights 🚀")

# =====================================
# KPI METRICS
# =====================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("🏙️ City", city)
col2.metric("📊 Avg AQI", round(filtere
