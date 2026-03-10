# ============================================================
# 🚀 Rocket Mission Visualizer
# IDAI104 Generative AI Project
# Student: Jashith Hemendra Rathod
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import math
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Rocket Mission Visualizer 🚀",
    page_icon="🚀",
    layout="wide"
)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "splash"

if "user" not in st.session_state:
    st.session_state.user = None

# ============================================================
# CUSTOM CSS (GLASSMORPHISM + NEON STYLE)
# ============================================================

st.markdown("""
<style>

body {
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
}

.title {
font-size:48px;
font-weight:700;
text-align:center;
background:linear-gradient(90deg,#00ffd5,#7effff);
-webkit-background-clip:text;
color:transparent;
}

.glass-container{
background:rgba(255,255,255,0.05);
padding:30px;
border-radius:15px;
border:1px solid rgba(255,255,255,0.1);
backdrop-filter:blur(12px);
margin-top:20px;
}

.metric-card{
background:rgba(255,255,255,0.05);
padding:20px;
border-radius:12px;
text-align:center;
border:1px solid rgba(255,255,255,0.1);
}

.metric-label{
font-size:14px;
color:#bbbbbb;
}

.metric-value{
font-size:28px;
font-weight:600;
color:#00ffd5;
}

.neon-btn button{
background:linear-gradient(90deg,#00ffd5,#00aaff);
border:none;
border-radius:30px;
padding:10px 25px;
font-weight:600;
}

.glow-header{
font-size:22px;
font-weight:600;
color:#00ffd5;
margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SPLASH SCREEN
# ============================================================

if st.session_state.page == "splash":

    st.markdown(
        """
        <h1 class='title'>🚀 Rocket Mission Visualizer</h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='glass-container'>
        Welcome to the Rocket Mission Visualizer platform.
        This system analyzes space mission datasets,
        performs rocket physics simulations,
        and visualizes mission trends using interactive graphs.
        </div>
        """,
        unsafe_allow_html=True
    )

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.02)
        progress.progress(i + 1)

    st.session_state.page = "landing"
    st.rerun()

# ============================================================
# LANDING PAGE
# ============================================================

if st.session_state.page == "landing":

    st.markdown(
        """
        <h1 class='title'>Rocket Mission Visualizer 🚀</h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='glass-container'>
        Explore global space missions, analyze rocket launches,
        and simulate rocket trajectories using physics-based models.

        Features:
        • Interactive mission dataset explorer  
        • Rocket physics simulations  
        • Mission analytics dashboard  
        • AI-powered insights
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        if st.button("🚀 Get Started"):
            st.session_state.page = "signup"
            st.rerun()

# ============================================================
# SIGNUP PAGE
# ============================================================

if st.session_state.page == "signup":

    st.markdown(
        """
        <h1 class='title'>Create Account</h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Enter Dashboard 🚀"):

        if username and email and password:

            st.session_state.user = username
            st.session_state.page = "dashboard"
            st.success("Account created successfully!")
            time.sleep(1)
            st.rerun()

        else:
            st.error("Please fill all fields")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# DATASET LOADING
# ============================================================

@st.cache_data
def load_dataset():

    try:
        df = pd.read_csv("space_missions_dataset.csv")
    except:
        df = pd.DataFrame()

    return df

# ============================================================
# ROCKET PHYSICS SIMULATION FUNCTION
# ============================================================

def rocket_simulation(thrust, mass, drag, burn_rate, steps=200):

    g = 9.81

    velocity = 0
    altitude = 0

    altitudes = []
    velocities = []

    for i in range(steps):

        acceleration = (thrust - drag - mass * g) / mass

        velocity = velocity + acceleration
        altitude = altitude + velocity

        mass = max(mass - burn_rate, 1)

        altitudes.append(altitude)
        velocities.append(velocity)

    return altitudes, velocities

# ============================================================
# DASHBOARD PAGE (START)
# ============================================================

if st.session_state.page == "dashboard":

    st.markdown(
        f"""
        <h1 class='title'>Welcome {st.session_state.user} 🚀</h1>
        """,
        unsafe_allow_html=True
    )

    df = load_dataset()

    if df.empty:
        st.warning("Dataset not found. Please upload space_missions_dataset.csv")
        st.stop()

    st.markdown("<div class='glass-container'>Dataset Loaded Successfully</div>", unsafe_allow_html=True)





# ============================================================
# DATA CLEANING
# ============================================================

df.columns = df.columns.str.strip()

df = df.drop_duplicates()

df = df.fillna(method="ffill")

# Convert date column if present
for col in df.columns:
    if "date" in col.lower():
        try:
            df[col] = pd.to_datetime(df[col])
        except:
            pass

# ============================================================
# FEATURE ENGINEERING
# ============================================================

numeric_cols = df.select_dtypes(include=np.number).columns

df["Mission_Index"] = np.arange(len(df))

df["Success_Flag"] = df.get("Mission_Status", "").astype(str).str.contains("Success", case=False)

df["Success_Flag"] = df["Success_Flag"].astype(int)

# ============================================================
# BASIC DATASET STATS
# ============================================================

total_missions = len(df)

success_rate = df["Success_Flag"].mean() * 100

numeric_summary = df[numeric_cols].describe()

# ============================================================
# SIDEBAR CONTROLS
# ============================================================

st.sidebar.markdown("## 🚀 Simulation Controls")

payload_weight = st.sidebar.slider(
    "Payload Weight (kg)",
    100,
    10000,
    2000
)

rocket_thrust = st.sidebar.slider(
    "Rocket Thrust (kN)",
    1000,
    10000,
    4000
)

fuel_amount = st.sidebar.slider(
    "Fuel Amount (tons)",
    50,
    1000,
    300
)

drag_coeff = st.sidebar.slider(
    "Drag Coefficient",
    0.1,
    1.5,
    0.5
)

burn_rate = st.sidebar.slider(
    "Fuel Burn Rate",
    1,
    50,
    10
)

time_steps = st.sidebar.slider(
    "Simulation Steps",
    50,
    500,
    200
)

# ============================================================
# MISSION FILTERS
# ============================================================

st.sidebar.markdown("## 📊 Mission Filters")

if "Company" in df.columns:
    company_filter = st.sidebar.selectbox(
        "Launch Company",
        ["All"] + sorted(df["Company"].dropna().unique().tolist())
    )
else:
    company_filter = "All"

if "Location" in df.columns:
    location_filter = st.sidebar.selectbox(
        "Launch Location",
        ["All"] + sorted(df["Location"].dropna().unique().tolist())
    )
else:
    location_filter = "All"

# Apply filters
filtered_df = df.copy()

if company_filter != "All":
    filtered_df = filtered_df[filtered_df["Company"] == company_filter]

if location_filter != "All":
    filtered_df = filtered_df[filtered_df["Location"] == location_filter]

# ============================================================
# DASHBOARD METRICS
# ============================================================

total_filtered = len(filtered_df)

success_filtered = filtered_df["Success_Flag"].sum()

success_rate_filtered = (success_filtered / total_filtered) * 100 if total_filtered else 0

avg_payload = payload_weight

fuel_efficiency = rocket_thrust / fuel_amount

# ============================================================
# METRIC CARDS DISPLAY
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-label">Total Missions</div>
        <div class="metric-value">{total_filtered}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-label">Success Rate</div>
        <div class="metric-value">{success_rate_filtered:.2f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-label">Payload Weight</div>
        <div class="metric-value">{avg_payload} kg</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-label">Fuel Efficiency</div>
        <div class="metric-value">{fuel_efficiency:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# ADDITIONAL METRICS
# ============================================================

col5, col6, col7, col8 = st.columns(4)

max_payload = payload_weight * 1.5
mission_cost = rocket_thrust * fuel_amount * 10
avg_drag = drag_coeff * 100
estimated_orbit = rocket_thrust / payload_weight

with col5:
    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-label">Max Payload</div>
        <div class="metric-value">{max_payload:.0f} kg</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col6:
    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-label">Mission Cost</div>
        <div class="metric-value">${mission_cost:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col7:
    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-label">Drag Impact</div>
        <div class="metric-value">{avg_drag:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col8:
    st.markdown(
        f"""
        <div class="metric-card">
        <div class="metric-label">Orbit Potential</div>
        <div class="metric-value">{estimated_orbit:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# DATA PREVIEW
# ============================================================

st.markdown("### Mission Dataset Preview")

st.dataframe(filtered_df.head(50))

# ============================================================
# PREPARE DATA FOR VISUALIZATION
# ============================================================

numeric_df = filtered_df.select_dtypes(include=np.number)

correlation_matrix = numeric_df.corr()

mission_counts = None

if "Company" in filtered_df.columns:
    mission_counts = filtered_df["Company"].value_counts().head(10)

location_counts = None

if "Location" in filtered_df.columns:
    location_counts = filtered_df["Location"].value_counts().head(10)

















# ============================================================
# TAB STRUCTURE
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🚀 Simulation",
    "📊 Scatter Plot",
    "📉 Line Chart",
    "📊 Bar Chart",
    "📦 Box Plot",
    "🔥 Correlation Heatmap",
    "⚙ Settings"
])

# ============================================================
# TAB 1 — ROCKET SIMULATION
# ============================================================

with tab1:

    st.subheader("Rocket Trajectory Simulation")

    mass = payload_weight + fuel_amount * 100
    thrust = rocket_thrust * 1000
    drag = drag_coeff * 100

    altitudes, velocities = rocket_simulation(
        thrust,
        mass,
        drag,
        burn_rate,
        steps=time_steps
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=altitudes,
            mode="lines",
            name="Altitude"
        )
    )

    fig.update_layout(
        title="Altitude vs Time",
        template="plotly_dark",
        xaxis_title="Time Step",
        yaxis_title="Altitude"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            y=velocities,
            mode="lines",
            name="Velocity"
        )
    )

    fig2.update_layout(
        title="Velocity vs Time",
        template="plotly_dark"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    **Simulation Insight**

    The rocket trajectory is calculated using Newtonian physics.

    Acceleration = (Thrust − Drag − Gravity) / Mass

    Higher thrust increases altitude potential while higher drag
    reduces velocity and efficiency.
    """)

# ============================================================
# TAB 2 — SCATTER PLOT
# ============================================================

with tab2:

    st.subheader("Payload vs Mission Index")

    if len(numeric_df.columns) >= 2:

        x_col = numeric_df.columns[0]
        y_col = numeric_df.columns[1]

        fig = px.scatter(
            filtered_df,
            x=x_col,
            y=y_col,
            color="Success_Flag",
            title="Scatter Plot Analysis"
        )

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Not enough numeric columns for scatter plot")

# ============================================================
# TAB 3 — LINE CHART
# ============================================================

with tab3:

    st.subheader("Mission Trend Over Time")

    if "Mission_Index" in filtered_df.columns:

        fig = px.line(
            filtered_df,
            x="Mission_Index",
            y=numeric_df.columns[0],
            title="Mission Metric Trend"
        )

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 4 — BAR CHART
# ============================================================

with tab4:

    st.subheader("Top Launch Companies")

    if mission_counts is not None:

        fig = px.bar(
            mission_counts,
            x=mission_counts.index,
            y=mission_counts.values,
            title="Launch Frequency by Company"
        )

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 5 — BOX PLOT
# ============================================================

with tab5:

    st.subheader("Payload Distribution")

    if len(numeric_df.columns) > 0:

        fig = px.box(
            filtered_df,
            y=numeric_df.columns[0],
            title="Distribution Analysis"
        )

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 6 — CORRELATION HEATMAP
# ============================================================

with tab6:

    st.subheader("Correlation Heatmap")

    if len(numeric_df.columns) > 1:

        fig = px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            title="Feature Correlation"
        )

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 7 — SETTINGS
# ============================================================

with tab7:

    st.subheader("User Settings")

    notifications = st.toggle("Enable Notifications")

    st.write("Notifications:", "Enabled" if notifications else "Disabled")

    st.divider()

    if st.button("Sign Out"):

        st.session_state.page = "landing"
        st.session_state.user = None
        st.rerun()

# ============================================================
# FEEDBACK SECTION
# ============================================================

st.divider()

st.subheader("User Feedback")

feedback = st.text_area("Share your experience")

rating = st.slider("Rate the platform", 1, 5, 4)

if st.button("Submit Feedback"):

    st.success("Thank you for your feedback!")
