import streamlit as st
import pandas as pd
import plotly.express as px
import json
from datetime import datetime
import requests

BACKEND_HOST = "testpilot-backend" # This MUST match the --name you gave your backend container
BACKEND_PORT = 8000

try:
    res = requests.get(f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/metrics")
    res.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
    st.write(res.json())
except requests.exceptions.ConnectionError as e:
    st.error(f"Could not connect to backend: {e}")
    st.info(f"Attempted to connect to http://{BACKEND_HOST}:{BACKEND_PORT}/api/metrics")
    st.warning("Ensure the backend container 'testpilot-backend' is running and healthy on the same Docker network.")
except requests.exceptions.HTTPError as e:
    st.error(f"Backend returned an error: {e}")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
df = pd.DataFrame(res.json())
# Sample test run data (can be replaced with API call)

st.set_page_config(page_title="📊 TestPilot Dashboard", layout="wide")


# =========================
# Metric Cards
# =========================
st.title("📊 AI SaaS - TestPilot Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🧪 Total Tests", len(df))
col2.metric("✅ Passed", df['status'].value_counts().get("passed", 0))
col3.metric("❌ Failed", df['status'].value_counts().get("failed", 0))
col4.metric("⚠️ Avg. Risk %", f"{int(df['risk_score'].mean())}%")

st.divider()

# =========================
# Charts Section
# =========================

# Pie Chart - Pass vs Fail
st.subheader("📊 Test Outcome Breakdown")
outcome_pie = px.pie(
    df,
    names='status',
    title="Pass vs Fail",
    color_discrete_map={"passed": "green", "failed": "red"}
)
st.plotly_chart(outcome_pie, use_container_width=True)

# Line Chart - Tests Over Time
st.subheader("📈 Tests Run Over Time")
df['date'] = pd.to_datetime(df['date'])
tests_per_day = df.groupby(df['date'].dt.date).size().reset_index(name='count')

line_chart = px.line(
    tests_per_day,
    x='date',
    y='count',
    title="Daily Test Runs",
    markers=True
)
st.plotly_chart(line_chart, use_container_width=True)

# Radar Chart - AI Test Metrics
st.subheader("🧠 AI Quality Metrics (Radar)")

avg_metrics = {
    "coverage": 82,
    "stability": 74,
    "clarity": 67,
    "speed": 71,
    "accuracy": 78
}

radar_df = pd.DataFrame(dict(
    r=list(avg_metrics.values()),
    theta=list(avg_metrics.keys())
))

radar_chart = px.line_polar(
    radar_df,
    r='r',
    theta='theta',
    line_close=True,
    title="AI Quality Metrics",
    template="plotly_dark"
)
st.plotly_chart(radar_chart, use_container_width=True)
