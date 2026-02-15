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

col2.metric(
    "📊 Avg AQI",
    round(filtered["aqi"].mean(), 2)
)

col3.metric(
    "🔥 Max AQI",
    int(filtered["aqi"].max())
)

col4.metric(
    "🌱 Min AQI",
    int(filtered["aqi"].min())
)

# =====================================
# INSIGHTS SECTION
# =====================================
st.subheader("🧠 Key Insights")

best_day = filtered.loc[filtered["aqi"].idxmin()]
worst_day = filtered.loc[filtered["aqi"].idxmax()]

st.info(
    f"""
✅ Best Air Quality Day: {best_day['date'].date()} 🌱 (AQI: {best_day['aqi']})  
❌ Worst Air Quality Day: {worst_day['date'].date()} 🔥 (AQI: {worst_day['aqi']})  
📌 Most Common Category: {filtered['aqi_category'].mode()[0]}
"""
)

# =====================================
# DOWNLOAD BUTTON
# =====================================
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered.to_csv(index=False),
    file_name=f"{city}_AQI_Data.csv",
    mime="text/csv"
)

# =====================================
# GRAPH SECTION
# =====================================
st.subheader("📊 15 Interactive Graphs")

# -------- Graph 1 AQI Trend --------
fig1 = px.line(
    filtered, x="date", y="aqi",
    title="1️⃣ AQI Trend Over Time 📈",
    markers=True
)
st.plotly_chart(fig1, use_container_width=True)

# -------- Graph 2 PM2.5 --------
fig2 = px.area(
    filtered, x="date", y="pm25",
    title="2️⃣ PM2.5 Pollution 🌫️"
)
st.plotly_chart(fig2, use_container_width=True)

# -------- Graph 3 PM10 --------
fig3 = px.line(
    filtered, x="date", y="pm10",
    title="3️⃣ PM10 Levels 🚗"
)
st.plotly_chart(fig3, use_container_width=True)

# -------- Graph 4 NO2 --------
fig4 = px.bar(
    filtered, x="date", y="no2",
    title="4️⃣ NO2 Concentration 🏭",
    color="no2"
)
st.plotly_chart(fig4, use_container_width=True)

# -------- Graph 5 SO2 --------
fig5 = px.scatter(
    filtered, x="date", y="so2",
    title="5️⃣ SO2 Scatter 🌋",
    size="so2",
    color="so2"
)
st.plotly_chart(fig5, use_container_width=True)

# ----
