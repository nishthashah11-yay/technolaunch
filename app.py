# ==================================================
# IMPORTS
# ==================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Rocket Launch Visualization",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Rocket Launch Path Visualization Dashboard")
st.write("Mathematics for AI – Rocket Launch Analysis & Simulation")

# ==================================================
# DATA LOADING
# ==================================================

@st.cache_data
def load_data():
    df = pd.read_csv("space_missions.csv")
    return df

df = load_data()

# ==================================================
# DATA CLEANING
# ==================================================

df["Launch Date"] = pd.to_datetime(df["Launch Date"], errors="coerce")

numeric_cols = [
    "Distance from Earth",
    "Mission Duration",
    "Mission Cost",
    "Scientific Yield",
    "Crew Size",
    "Fuel Consumption",
    "Payload Weight"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

# ==================================================
# SIDEBAR CONTROLS
# ==================================================

st.sidebar.header("⚙ Filters")

mission_type = st.sidebar.selectbox(
    "Mission Type",
    df["Mission Type"].unique()
)

vehicle = st.sidebar.selectbox(
    "Launch Vehicle",
    df["Launch Vehicle"].unique()
)

distance_filter = st.sidebar.slider(
    "Distance from Earth",
    int(df["Distance from Earth"].min()),
    int(df["Distance from Earth"].max())
)

filtered_df = df[
    (df["Mission Type"] == mission_type) &
    (df["Launch Vehicle"] == vehicle) &
    (df["Distance from Earth"] <= distance_filter)
]

# ==================================================
# METRICS
# ==================================================

col1, col2, col3 = st.columns(3)

col1.metric("Total Missions", len(filtered_df))
col2.metric("Avg Payload", round(filtered_df["Payload Weight"].mean(),2))
col3.metric("Avg Fuel Consumption", round(filtered_df["Fuel Consumption"].mean(),2))

# ==================================================
# VISUALIZATIONS
# ==================================================

tabs = st.tabs([
    "Payload vs Fuel",
    "Mission Cost",
    "Duration vs Distance",
    "Crew vs Success",
    "Scientific Yield",
    "Correlation Heatmap",
    "Rocket Simulation"
])

# ==================================================
# SCATTER → PAYLOAD VS FUEL
# ==================================================

with tabs[0]:

    fig = px.scatter(
        filtered_df,
        x="Payload Weight",
        y="Fuel Consumption",
        color="Mission Type",
        title="Payload Weight vs Fuel Consumption"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# BAR → COST VS SUCCESS
# ==================================================

with tabs[1]:

    cost_data = filtered_df.groupby("Mission Success")["Mission Cost"].mean().reset_index()

    fig = px.bar(
        cost_data,
        x="Mission Success",
        y="Mission Cost",
        title="Mission Cost: Success vs Failure"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# LINE → DURATION VS DISTANCE
# ==================================================

with tabs[2]:

    fig = px.line(
        filtered_df,
        x="Distance from Earth",
        y="Mission Duration",
        title="Mission Duration vs Distance"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# BOX → CREW SIZE VS SUCCESS
# ==================================================

with tabs[3]:

    fig = px.box(
        filtered_df,
        x="Mission Success",
        y="Crew Size",
        title="Crew Size vs Mission Success"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# SCATTER → SCIENTIFIC YIELD VS COST
# ==================================================

with tabs[4]:

    fig = px.scatter(
        filtered_df,
        x="Mission Cost",
        y="Scientific Yield",
        color="Mission Type",
        title="Scientific Yield vs Mission Cost"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# HEATMAP
# ==================================================

with tabs[5]:

    corr = filtered_df[numeric_cols].corr()

    fig, ax = plt.subplots()

    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

    st.pyplot(fig)

# ==================================================
# ROCKET SIMULATION
# ==================================================

with tabs[6]:

    st.subheader("Rocket Launch Simulation")

    thrust = st.slider("Thrust", 10000, 100000, 50000)
    payload = st.slider("Payload Weight", 100, 2000, 500)
    drag = st.slider("Drag Factor", 0.01, 0.5, 0.1)
    fuel = st.slider("Fuel Mass", 5000, 20000, 10000)

    mass = payload + fuel

    time_steps = 100

    altitude = []
    velocity = []

    v = 0
    h = 0

    g = 9.81

    for t in range(time_steps):

        drag_force = drag * v**2

        acceleration = (thrust - mass*g - drag_force) / mass

        v = v + acceleration
        h = h + v

        fuel -= 20
        mass = payload + max(fuel,0)

        altitude.append(h)
        velocity.append(v)

    sim_df = pd.DataFrame({
        "Time": range(time_steps),
        "Altitude": altitude,
        "Velocity": velocity
    })

    fig = px.line(sim_df, x="Time", y="Altitude", title="Rocket Altitude Over Time")

    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.line(sim_df, x="Time", y="Velocity", title="Rocket Velocity Over Time")

    st.plotly_chart(fig2, use_container_width=True)
