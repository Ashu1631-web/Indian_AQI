import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="India AQI Dashboard 🌍",
    page_icon="🌫️",
    layout="wide"
)

# =====================================
# DARK MODE TOGGLE 🌙
# =====================================
theme = st.sidebar.radio("🎨 Select Theme", ["Light Mode ☀️", "Dark Mode 🌙"])

if theme == "Dark Mode 🌙":
    st.markdown(
        """
        <style>
        body {background-color: #0E1117; color: white;}
        </style>
        """,
        unsafe_allow_html=True
    )

# =====================================
# CITY COORDINATES (Map Support) 🗺️
# =====================================
city_coords = {
    "Delhi": [28.61, 77.20],
    "Mumbai": [19.07, 72.87],
    "Kolkata": [22.57, 88.36],
    "Chennai": [13.08, 80.27],
    "Bengaluru": [12.97, 77.59],
    "Hyderabad": [17.38, 78.48],
    "Pune": [18.52, 73.85],
    "Ahmedabad": [23.02, 72.57],
    "Jaipur": [26.91, 75.79],
    "Lucknow": [26.85, 80.94]
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
st.title("🌫️ India Air Quality Premium Dashboard")
st.markdown("### Charts + Map + Gauge Health Status + Insights 🚀")

# =====================================
# KPI METRICS
# =====================================
col1, col2, col3, col4 = st.columns(4)

avg_aqi = round(filtered["aqi"].mean(), 2)

col1.metric("🏙️ City", city)
col2.metric("📊 Avg AQI", avg_aqi)
col3.metric("🔥 Max AQI", int(filtered["aqi"].max()))
col4.metric("🌱 Min AQI", int(filtered["aqi"].min()))

# =====================================
# DOWNLOAD BUTTON
# =====================================
st.download_button(
    "📥 Download Filtered Data",
    filtered.to_csv(index=False),
    file_name=f"{city}_AQI_Data.csv",
    mime="text/csv"
)

# =====================================
# INDIA AQI MAP 🗺️
# =====================================
st.subheader("🗺️ AQI Map (Major Cities)")

map_data = []
for c in city_coords:
    city_df = df[df["city"] == c]
    if len(city_df) > 0:
        lat, lon = city_coords[c]
        map_data.append([c, lat, lon, city_df["aqi"].mean()])

map_df = pd.DataFrame(map_data, columns=["city", "lat", "lon", "avg_aqi"])

fig_map = px.scatter_mapbox(
    map_df,
    lat="lat",
    lon="lon",
    size="avg_aqi",
    color="avg_aqi",
    hover_name="city",
    zoom=3.5,
    title="🌍 India AQI Distribution Map",
    mapbox_style="open-street-map"
)
st.plotly_chart(fig_map, use_container_width=True)
st.caption("📌 Insight: Highest AQI cities appear darker & larger.")

# =====================================
# GAUGE AQI WITH HEALTH LEVELS 🚦
# =====================================
st.subheader("🚥 AQI Gauge Meter with Health Status")

if avg_aqi <= 50:
    status = "🟢 Good (Healthy Air)"
elif avg_aqi <= 100:
    status = "🟡 Moderate (Acceptable)"
elif avg_aqi <= 200:
    status = "🟠 Unhealthy (Sensitive Groups)"
elif avg_aqi <= 300:
    status = "🔴 Very Unhealthy"
else:
    status = "☠️ Hazardous (Danger Zone)"

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=avg_aqi,
    title={"text": f"Average AQI Status: {status}"},
    gauge={
        "axis": {"range": [0, 500]},
        "steps": [
            {"range": [0, 50], "color": "lightgreen"},
            {"range": [51, 100], "color": "yellow"},
            {"range": [101, 200], "color": "orange"},
            {"range": [201, 300], "color": "red"},
            {"range": [301, 500], "color": "darkred"},
        ],
        "threshold": {
            "line": {"color": "black", "width": 4},
            "value": avg_aqi
        }
    }
))
st.plotly_chart(fig_gauge, use_container_width=True)
st.caption(f"📌 Insight: Current AQI = **{avg_aqi}**, Status = **{status}**")

# =====================================
# REQUIRED CHARTS SECTION 📊
# =====================================
st.subheader("📊 All Required AQI Charts")

# 1 Line Chart
fig1 = px.line(filtered, x="date", y="aqi", title="📈 Line Chart - AQI Trend")
st.plotly_chart(fig1, use_container_width=True)
st.caption("Insight: Trend shows pollution increasing/decreasing over time.")

# 2 Area Chart
fig2 = px.area(filtered, x="date", y="pm25", title="🌫️ Area Chart - PM2.5 Levels")
st.plotly_chart(fig2, use_container_width=True)
st.caption("Insight: Higher PM2.5 means dangerous breathing conditions.")

# 3 Bar Chart
fig3 = px.bar(filtered.head(20), x="date", y="aqi", title="📊 Bar Chart - Daily AQI")
st.plotly_chart(fig3, use_container_width=True)

# 4 Pie Chart
fig4 = px.pie(filtered, names="aqi_category", title="🍩 Pie Chart - AQI Categories")
st.plotly_chart(fig4, use_container_width=True)

# 5 Scatter Plot
fig5 = px.scatter(filtered, x="pm25", y="aqi",
                  title="🔥 Scatter Plot - PM2.5 vs AQI", color="aqi")
st.plotly_chart(fig5, use_container_width=True)

# 6 Box Plot
fig6 = px.box(filtered, y="pm25", title="📦 Box Plot - PM2.5 Spread")
st.plotly_chart(fig6, use_container_width=True)

# 7 Heatmap
corr = filtered[["pm25", "pm10", "no2", "so2", "co", "o3", "aqi"]].corr()
fig7 = px.imshow(corr, text_auto=True, title="🌡️ Heatmap - Pollutant Correlation")
st.plotly_chart(fig7, use_container_width=True)

# 8 Waterfall Chart
fig8 = go.Figure(go.Waterfall(
    orientation="v",
    measure=["relative", "relative", "relative", "total"],
    x=["PM2.5", "PM10", "NO2", "Total AQI"],
    y=[20, 15, 10, avg_aqi]
))
fig8.update_layout(title="💧 Waterfall Chart - AQI Contribution")
st.plotly_chart(fig8, use_container_width=True)
st.caption("Insight: Shows step-by-step pollutant contribution to AQI.")

# 9 Gantt / Timeline Chart
timeline = filtered.head(10).copy()
timeline["Start"] = timeline["date"]
timeline["Finish"] = timeline["date"] + pd.Timedelta(days=2)

fig9 = px.timeline(
    timeline,
    x_start="Start",
    x_end="Finish",
    y="aqi_category",
    title="📅 Gantt Timeline - AQI Category Duration"
)
st.plotly_chart(fig9, use_container_width=True)
st.caption("Insight: Timeline shows AQI categories across days.")

# =====================================
# FINAL MESSAGE
# =====================================
st.success("✅ FINAL Dashboard Ready: Charts + Map + Gauge + Insights 🚀")
