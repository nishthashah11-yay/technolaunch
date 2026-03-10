# ============================================================
# 🚀 Rocket Mission Visualizer
# Generative AI Project
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Rocket Mission Visualizer 🚀",
    page_icon="🚀",
    layout="wide"
)

# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "splash"

if "user" not in st.session_state:
    st.session_state.user = None

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.title{
font-size:50px;
font-weight:700;
text-align:center;
background:linear-gradient(90deg,#00ffd5,#00aaff);
-webkit-background-clip:text;
color:transparent;
}

.glass{
background:rgba(255,255,255,0.05);
padding:25px;
border-radius:15px;
border:1px solid rgba(255,255,255,0.1);
backdrop-filter:blur(10px);
}

.metric-card{
background:rgba(255,255,255,0.05);
padding:20px;
border-radius:12px;
text-align:center;
border:1px solid rgba(255,255,255,0.1);
}

.metric-value{
font-size:28px;
font-weight:600;
color:#00ffd5;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SPLASH SCREEN
# ============================================================

if st.session_state.page == "splash":

    st.markdown("<h1 class='title'>Rocket Mission Visualizer 🚀</h1>", unsafe_allow_html=True)

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i+1)

    st.session_state.page = "landing"
    st.rerun()

# ============================================================
# LANDING PAGE
# ============================================================

if st.session_state.page == "landing":

    st.markdown("<h1 class='title'>Rocket Mission Visualizer 🚀</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">
    Explore global space missions and simulate rocket physics.
    </div>
    """, unsafe_allow_html=True)

    if st.button("Get Started 🚀"):
        st.session_state.page = "signup"
        st.rerun()

# ============================================================
# SIGNUP PAGE
# ============================================================

if st.session_state.page == "signup":

    st.markdown("<h1 class='title'>Create Account</h1>", unsafe_allow_html=True)

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Enter Dashboard 🚀"):

        if username and email and password:

            st.session_state.user = username
            st.session_state.page = "dashboard"
            st.rerun()

        else:
            st.error("Please fill all fields")

# ============================================================
# DATA LOADER
# ============================================================

@st.cache_data
def load_dataset():

    try:
        df = pd.read_csv("space_missions_dataset.csv")
    except:
        df = pd.DataFrame()

    return df

# ============================================================
# ROCKET SIMULATION
# ============================================================

def rocket_simulation(thrust, mass, drag, burn_rate, steps=200):

    g = 9.81
    velocity = 0
    altitude = 0

    altitudes = []
    velocities = []

    for _ in range(steps):

        acceleration = (thrust - drag - mass*g) / mass

        velocity += acceleration
        altitude += velocity

        mass = max(mass - burn_rate, 1)

        altitudes.append(altitude)
        velocities.append(velocity)

    return altitudes, velocities

# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "dashboard":

    st.markdown(f"<h1 class='title'>Welcome {st.session_state.user}</h1>", unsafe_allow_html=True)

    df = load_dataset()

    if df.empty:
        st.error("Dataset not found")
        st.stop()

    # ============================================================
    # DATA CLEANING
    # ============================================================

    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()
    df = df.fillna(method="ffill")

    # ============================================================
    # SUCCESS FLAG (SAFE)
    # ============================================================

    status_col = None

    for col in df.columns:
        if "status" in col.lower():
            status_col = col
            break

    if status_col:
        df["Success_Flag"] = df[status_col].astype(str).str.contains(
            "success", case=False, na=False
        ).astype(int)
    else:
        df["Success_Flag"] = 0

    # ============================================================
    # SIDEBAR CONTROLS
    # ============================================================

    st.sidebar.title("Simulation Controls")

    payload = st.sidebar.slider("Payload Weight (kg)", 100, 10000, 2000)
    thrust = st.sidebar.slider("Rocket Thrust (kN)", 1000, 10000, 4000)
    fuel = st.sidebar.slider("Fuel Amount (tons)", 50, 1000, 300)
    drag = st.sidebar.slider("Drag Coefficient", 0.1, 1.5, 0.5)
    burn = st.sidebar.slider("Fuel Burn Rate", 1, 50, 10)
    steps = st.sidebar.slider("Simulation Steps", 50, 500, 200)

    # ============================================================
    # METRICS
    # ============================================================

    total_missions = len(df)
    success_rate = df["Success_Flag"].mean() * 100

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
        Total Missions
        <div class="metric-value">{total_missions}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
        Success Rate
        <div class="metric-value">{success_rate:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
        Payload
        <div class="metric-value">{payload} kg</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        efficiency = thrust / fuel
        st.markdown(f"""
        <div class="metric-card">
        Efficiency
        <div class="metric-value">{efficiency:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================
    # TABS
    # ============================================================

    tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs([
        "🚀 Simulation",
        "📊 Scatter",
        "📈 Line",
        "📊 Bar",
        "📦 Box",
        "🔥 Heatmap",
        "⚙ Settings"
    ])

    # ============================================================
    # TAB 1 — SIMULATION
    # ============================================================

    with tab1:

        mass = payload + fuel*100
        thrust_force = thrust*1000
        drag_force = drag*100

        altitudes, velocities = rocket_simulation(
            thrust_force, mass, drag_force, burn, steps
        )

        fig = go.Figure()

        fig.add_trace(go.Scatter(y=altitudes,name="Altitude"))

        fig.update_layout(template="plotly_dark",title="Altitude vs Time")

        st.plotly_chart(fig,use_container_width=True)

    # ============================================================
    # TAB 2 — SCATTER
    # ============================================================

    with tab2:

        st.subheader("Payload vs Fuel Consumption")


        numeric = df.select_dtypes(include=np.number)

        if len(numeric.columns)>=2:

            fig = px.scatter(
                df,
                x=numeric.columns[0],
                y=numeric.columns[1],
                color="Success_Flag"
            )

            fig.update_layout(template="plotly_dark")

            st.plotly_chart(fig,use_container_width=True)

    # ============================================================
    # TAB 3 — LINE
    # ============================================================

    with tab3:
        st.subheader("Mission Duration vs Distance from Earth")

        numeric = df.select_dtypes(include=np.number)

        fig = px.line(
            df,
            y=numeric.columns[0]
        )

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    # ============================================================
    # TAB 4 — BAR
    # ============================================================

    # ============================================================
# TAB 4 — BAR CHART
# ============================================================

# ============================================================
# TAB 4 — BAR CHART
# ============================================================

with tab4:

    st.subheader("Launch Vehicles Used")

    counts = df["Launch Vehicle"].value_counts()

    fig = px.bar(
        x=counts.index,
        y=counts.values,
        labels={"x": "Launch Vehicle", "y": "Number of Missions"},
        title="Missions by Launch Vehicle"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

    # ============================================================
    # TAB 5 — BOX
    # ============================================================

    with tab5:
        st.subheader("Crew Size vs Mission Success")


        numeric = df.select_dtypes(include=np.number)

        fig = px.box(df,y=numeric.columns[0])

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    # ============================================================
    # TAB 6 — HEATMAP
    # ============================================================

    with tab6:
        st.subheader("Heat Map")


        numeric = df.select_dtypes(include=np.number)

        corr = numeric.corr()

        fig = px.imshow(corr,text_auto=True)

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    # ============================================================
    # TAB 7 — SETTINGS
    # ============================================================

    with tab7:

        if st.button("Sign Out"):
            st.session_state.page = "landing"
            st.session_state.user = None
            st.rerun()

    # ============================================================
    # FEEDBACK
    # ============================================================

    st.divider()

    feedback = st.text_area("Share feedback")

    rating = st.slider("Rate the app",1,5,4)

    if st.button("Submit Feedback"):
        st.success("Thanks for your feedback!")
