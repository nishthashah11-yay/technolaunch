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
    page_title="Rocket Launch Dashboard",
    page_icon="🚀",
    layout="wide"
)

# ==================================================
# SESSION NAVIGATION (Crypto App Style)
# ==================================================

if "page" not in st.session_state:
    st.session_state.page = "dashboard"


# ==================================================
# TITLE
# ==================================================

st.title("🚀 Rocket Launch Path Visualization Dashboard")
st.write("Mathematics for AI – Space Mission Data Analysis & Rocket Simulation")


# ==================================================
# LOAD DATA
# ==================================================

# ==================================================
# DATA LOADING (FIXED FOR STREAMLIT CLOUD)
# ==================================================

@st.cache_data
def load_data():

    try:
        df = pd.read_csv("space_missions.csv")

    except FileNotFoundError:

        st.warning("space_missions.csv not found. Using sample dataset.")

        df = pd.DataFrame({
            "Launch Date": pd.date_range(start="2020-01-01", periods=20),
            "Mission Type": np.random.choice(["Orbital","Lunar","Mars","Satellite"],20),
            "Launch Vehicle": np.random.choice(["Falcon 9","Atlas V","Soyuz","Ariane 5"],20),
            "Distance from Earth": np.random.randint(200,100000,20),
            "Mission Duration": np.random.randint(1,400,20),
            "Mission Cost": np.random.randint(50,500,20),
            "Scientific Yield": np.random.randint(10,100,20),
            "Crew Size": np.random.randint(0,7,20),
            "Fuel Consumption": np.random.randint(500,5000,20),
            "Payload Weight": np.random.randint(100,2000,20),
            "Mission Success": np.random.choice(["Success","Failure"],20)
        })

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
# SIDEBAR FILTERS
# ==================================================

st.sidebar.header("⚙ Mission Filters")

mission_type = st.sidebar.selectbox(
    "Mission Type",
    df["Mission Type"].unique()
)

vehicle = st.sidebar.selectbox(
    "Launch Vehicle",
    df["Launch Vehicle"].unique()
)

distance_filter = st.sidebar.slider(
    "Maximum Distance From Earth",
    int(df["Distance from Earth"].min()),
    int(df["Distance from Earth"].max()),
    int(df["Distance from Earth"].mean())
)

filtered_df = df[
    (df["Mission Type"] == mission_type) &
    (df["Launch Vehicle"] == vehicle) &
    (df["Distance from Earth"] <= distance_filter)
]


# ==================================================
# METRICS DASHBOARD
# ==================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Missions", len(filtered_df))
col2.metric("Average Payload", round(filtered_df["Payload Weight"].mean(), 2))
col3.metric("Average Fuel Use", round(filtered_df["Fuel Consumption"].mean(), 2))
col4.metric("Average Cost", round(filtered_df["Mission Cost"].mean(), 2))


# ==================================================
# DASHBOARD TABS
# ==================================================

tabs = st.tabs([
    "Payload vs Fuel",
    "Mission Cost Analysis",
    "Duration vs Distance",
    "Crew Analysis",
    "Scientific Yield",
    "Correlation Heatmap",
    "Rocket Launch Simulation"
])


# ==================================================
# SCATTER PLOT
# Payload vs Fuel
# ==================================================

with tabs[0]:

    st.subheader("Payload Weight vs Fuel Consumption")

    fig = px.scatter(
        filtered_df,
        x="Payload Weight",
        y="Fuel Consumption",
        color="Mission Type",
        size="Crew Size",
        title="Payload vs Fuel Consumption"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==================================================
# BAR PLOT
# Mission Cost vs Success
# ==================================================

with tabs[1]:

    st.subheader("Mission Cost vs Success")

    cost_data = filtered_df.groupby("Mission Success")["Mission Cost"].mean().reset_index()

    fig = px.bar(
        cost_data,
        x="Mission Success",
        y="Mission Cost",
        color="Mission Success",
        title="Average Mission Cost (Success vs Failure)"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==================================================
# LINE PLOT
# Duration vs Distance
# ==================================================

with tabs[2]:

    st.subheader("Mission Duration vs Distance")

    fig = px.line(
        filtered_df.sort_values("Distance from Earth"),
        x="Distance from Earth",
        y="Mission Duration",
        title="Mission Duration vs Distance"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==================================================
# BOX PLOT
# Crew vs Success
# ==================================================

with tabs[3]:

    st.subheader("Crew Size vs Mission Success")

    fig = px.box(
        filtered_df,
        x="Mission Success",
        y="Crew Size",
        color="Mission Success",
        title="Crew Size Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==================================================
# SCATTER
# Scientific Yield vs Cost
# ==================================================

with tabs[4]:

    st.subheader("Scientific Yield vs Mission Cost")

    fig = px.scatter(
        filtered_df,
        x="Mission Cost",
        y="Scientific Yield",
        color="Mission Type",
        title="Scientific Yield vs Mission Cost"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==================================================
# CORRELATION HEATMAP
# ==================================================

with tabs[5]:

    st.subheader("Correlation Between Mission Variables")

    corr = filtered_df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(10,6))

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        ax=ax
    )

    st.pyplot(fig)


# ==================================================
# ROCKET SIMULATION (DIFFERENTIAL EQUATION MODEL)
# ==================================================

with tabs[6]:

    st.subheader("Rocket Launch Physics Simulation")

    col1, col2 = st.columns(2)

    thrust = col1.slider("Thrust (N)", 10000, 120000, 50000)
    payload = col1.slider("Payload Weight (kg)", 100, 2000, 500)

    drag = col2.slider("Drag Coefficient", 0.01, 0.5, 0.1)
    fuel = col2.slider("Fuel Mass (kg)", 5000, 20000, 10000)

    mass = payload + fuel
    g = 9.81

    time_steps = 150

    altitude = []
    velocity = []

    v = 0
    h = 0

    for t in range(time_steps):

        drag_force = drag * v**2

        acceleration = (thrust - mass*g - drag_force) / mass

        v = v + acceleration
        h = h + v

        fuel -= 25
        mass = payload + max(fuel, 0)

        altitude.append(h)
        velocity.append(v)

    sim_df = pd.DataFrame({
        "Time": range(time_steps),
        "Altitude": altitude,
        "Velocity": velocity
    })

    fig = px.line(
        sim_df,
        x="Time",
        y="Altitude",
        title="Rocket Altitude Over Time"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.line(
        sim_df,
        x="Time",
        y="Velocity",
        title="Rocket Velocity Over Time"
    )

    st.plotly_chart(fig2, use_container_width=True)
