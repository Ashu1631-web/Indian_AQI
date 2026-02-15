import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
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
# CITY COORDINATES (for Map) 🗺️
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
st.markdown("### Dark Mode + AQI Map + Forecast Prediction 🚀")

# =====================================
# KPI METRICS
# =====================================
col1, col2, col3 = st.columns(3)

col1.metric("🏙️ City Selected", city)
col2.metric("📊 Avg AQI", round(filtered["aqi"].mean(), 2))
col3.metric("🔥 Max AQI", int(filtered["aqi"].max()))

# =====================================
# DOWNLOAD BUTTON
# =====================================
st.download_button(
    "📥 Download Filtered Data",
    filtered.to_csv(index=False),
    file_name=f"{city}_AQI.csv",
    mime="text/csv"
)

# =====================================
# INDIA AQI MAP 🗺️
# =====================================
st.subheader("🗺️ India AQI Map (Major Cities)")

map_data = []

for c in city_coords:
    city_df = df[df["city"] == c]
    if len(city_df) > 0:
        avg = city_df["aqi"].mean()
        lat, lon = city_coords[c]
        map_data.append([c, lat, lon, avg])

map_df = pd.DataFrame(map_data, columns=["city", "lat", "lon", "avg_aqi"])

fig_map = px.scatter_mapbox(
    map_df,
    lat="lat",
    lon="lon",
    size="avg_aqi",
    color="avg_aqi",
    hover_name="city",
    zoom=3.5,
    title="🌍 AQI Across Major Indian Cities",
    mapbox_style="open-street-map"
)

st.plotly_chart(fig_map, use_container_width=True)
st.caption("📌 Insight: Map shows highest polluted metro cities in India.")

# =====================================
# AQI FORECAST PREDICTION 🤖
# =====================================
st.subheader("🤖 AQI Forecast Prediction (Next 7 Days)")

if len(filtered) > 30:
    temp = filtered.copy()
    temp = temp.sort_values("date")

    temp["day_index"] = np.arange(len(temp))

    X = temp[["day_index"]]
    y = temp["aqi"]

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.arange(len(temp), len(temp) + 7).reshape(-1, 1)
    predictions = model.predict(future_days)

    future_dates = pd.date_range(temp["date"].max(), periods=7)

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Predicted_AQI": predictions
    })

    fig_forecast = px.line(
        forecast_df,
        x="Date",
        y="Predicted_AQI",
        markers=True,
        title="📈 AQI Forecast for Next 7 Days"
    )

    st.plotly_chart(fig_forecast, use_container_width=True)
    st.caption("📌 Insight: Forecast uses ML regression trend prediction.")

else:
    st.warning("⚠️ Not enough data for prediction (need 30+ records).")

# =====================================
# MAIN CHARTS (15+)
# =====================================
st.subheader("📊 AQI Analytics Charts")

# Line Chart
fig1 = px.line(filtered, x="date", y="aqi", title="AQI Trend 📈")
st.plotly_chart(fig1, use_container_width=True)
st.caption("📌 Insight: AQI spikes indicate pollution events.")

# Area Chart
fig2 = px.area(filtered, x="date", y="pm25", title="PM2.5 Pollution 🌫️")
st.plotly_chart(fig2, use_container_width=True)
st.caption("📌 Insight: PM2.5 is most dangerous pollutant for lungs.")

# Stacked Area
fig3 = px.area(filtered, x="date", y=["pm25", "pm10"], title="PM2.5 vs PM10 ⚖️")
st.plotly_chart(fig3, use_container_width=True)

# Step Chart
fig4 = px.line(filtered, x="date", y="aqi", title="Step AQI Change 🚦")
fig4.update_traces(line_shape="hv")
st.plotly_chart(fig4, use_container_width=True)

# Histogram
fig5 = px.histogram(filtered, x="aqi", title="AQI Distribution 📊")
st.plotly_chart(fig5, use_container_width=True)

# Pie Category
fig6 = px.pie(filtered, names="aqi_category", title="AQI Category 🍩")
st.plotly_chart(fig6, use_container_width=True)

# Heatmap
corr = filtered[["pm25", "pm10", "no2", "so2", "co", "o3", "aqi"]].corr()
fig7 = px.imshow(corr, text_auto=True, title="Correlation Heatmap 🌡️")
st.plotly_chart(fig7, use_container_width=True)

# Gauge Chart
avg_aqi = filtered["aqi"].mean()
fig8 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=avg_aqi,
    title={"text": "Gauge AQI 🚥"},
    gauge={"axis": {"range": [0, 500]}}
))
st.plotly_chart(fig8, use_container_width=True)

# Pictograph
st.subheader("🌱 AQI Emoji Status")
cat = filtered["aqi_category"].mode()[0]

if cat == "Good":
    st.success("🌱🌱🌱 Air Quality is GOOD")
elif cat == "Moderate":
    st.warning("😷😷 Air Quality is MODERATE")
else:
    st.error("🔥🔥🔥 Air Quality is POOR")

# =====================================
# FINAL MESSAGE
# =====================================
st.success("✅ Premium Dashboard Ready: Dark Mode + Map + Forecast + Analytics 🚀")
