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
# RED BLACK UI THEME
# ============================================================

st.markdown("""
<style>

/* APP BACKGROUND */

.stApp{
background-color:#070707;
color:white;
}

/* TITLE */

.title{
font-size:50px;
font-weight:700;
text-align:center;
background:linear-gradient(90deg,#ff0000,#ff4d4d);
-webkit-background-clip:text;
color:transparent;
}

/* GLASS PANEL */

.glass{
background:linear-gradient(145deg,#141414,#0f0f0f);
padding:25px;
border-radius:16px;
box-shadow:0px 0px 25px rgba(255,0,0,0.45);
}

/* METRIC CARD */

.metric-card{
background:linear-gradient(145deg,#1a1a1a,#111111);
padding:20px;
border-radius:14px;
text-align:center;
box-shadow:0px 0px 20px rgba(255,0,0,0.4);
}

.metric-value{
font-size:30px;
font-weight:700;
color:#ff4d4d;
}

/* BUTTONS */

.stButton>button{
background-color:#1f6feb;
color:white;
border-radius:8px;
padding:10px 20px;
border:none;
font-weight:600;
box-shadow:0px 0px 12px rgba(255,0,0,0.6);
}

.stButton>button:hover{
background-color:#3b82f6;
box-shadow:0px 0px 20px rgba(255,0,0,1);
}

/* EXPLANATION BOX */

.explain-box{
background:#111;
padding:20px;
border-radius:12px;
margin-bottom:15px;
box-shadow:0px 0px 15px rgba(255,0,0,0.3);
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
    Explore real mission data and understand the physics of rocket launches.
    This dashboard combines simulation with real mission analysis to study
    payload, thrust, drag and rocket performance.
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

    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()
    df = df.fillna(method="ffill")

    # ============================================================
    # SIDEBAR CONTROLS
    # ============================================================

    st.sidebar.title("Simulation Controls")

    payload = st.sidebar.slider("Payload Weight (kg)",100,10000,2000)
    thrust = st.sidebar.slider("Rocket Thrust (kN)",1000,10000,4000)
    fuel = st.sidebar.slider("Fuel Amount (tons)",50,1000,300)
    drag = st.sidebar.slider("Drag Coefficient",0.1,1.5,0.5)
    burn = st.sidebar.slider("Fuel Burn Rate",1,50,10)
    steps = st.sidebar.slider("Simulation Steps",50,500,200)

    # ============================================================
    # METRICS
    # ============================================================

    total_missions = len(df)

    col1,col2,col3 = st.columns(3)

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
        Payload
        <div class="metric-value">{payload} kg</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        efficiency = thrust/fuel
        st.markdown(f"""
        <div class="metric-card">
        Efficiency
        <div class="metric-value">{efficiency:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    # ============================================================
    # TABS
    # ============================================================

    tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8 = st.tabs([
    "🚀 Simulation",
    "📊 Scatter",
    "📈 Line",
    "📊 Bar",
    "📦 Box",
    "🔥 Heatmap",
    "📚 Data Explanation",
    "⚙ Settings"
    ])

    # ============================================================
    # SIMULATION
    # ============================================================

    with tab1:

        mass = payload + fuel*100
        thrust_force = thrust*1000
        drag_force = drag*100

        altitudes, velocities = rocket_simulation(
        thrust_force,mass,drag_force,burn,steps)

        fig = go.Figure()

        fig.add_trace(go.Scatter(y=altitudes,name="Altitude"))

        fig.update_layout(
        template="plotly_dark",
        title="Altitude vs Time"
        )

        st.plotly_chart(fig,use_container_width=True)

    # ============================================================
    # SCATTER
    # ============================================================

    with tab2:

        numeric = df.select_dtypes(include=np.number)

        if len(numeric.columns)>=2:

            fig = px.scatter(
            df,
            x=numeric.columns[0],
            y=numeric.columns[1]
            )

            fig.update_layout(template="plotly_dark")

            st.plotly_chart(fig,use_container_width=True)

    # ============================================================
    # LINE
    # ============================================================

    with tab3:

        numeric = df.select_dtypes(include=np.number)

        fig = px.line(df,y=numeric.columns[0])

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    # ============================================================
    # BAR
    # ============================================================

    with tab4:

        counts = df["Launch Vehicle"].value_counts()

        fig = px.bar(
        x=counts.index,
        y=counts.values,
        labels={"x":"Launch Vehicle","y":"Number of Missions"},
        title="Missions by Launch Vehicle"
        )

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    # ============================================================
    # BOX
    # ============================================================

    with tab5:

        numeric = df.select_dtypes(include=np.number)

        fig = px.box(df,y=numeric.columns[0])

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    # ============================================================
    # HEATMAP
    # ============================================================

    with tab6:

        numeric = df.select_dtypes(include=np.number)

        corr = numeric.corr()

        fig = px.imshow(corr,text_auto=True)

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    # ============================================================
    # DATA EXPLANATION
    # ============================================================

    with tab7:

        st.markdown("<div class='explain-box'><b>Newton’s Second Law</b><br>"
        "Force = Mass × Acceleration. Rockets accelerate upward when thrust "
        "overcomes gravity and drag. As fuel burns, rocket mass decreases "
        "which increases acceleration.</div>", unsafe_allow_html=True)

        st.markdown("<div class='explain-box'><b>Thrust</b><br>"
        "Thrust is the force produced by rocket engines when fuel gases are "
        "expelled at high velocity. According to Newton's Third Law, pushing "
        "gases downward produces an equal upward force that lifts the rocket."
        "</div>", unsafe_allow_html=True)

        st.markdown("<div class='explain-box'><b>Drag</b><br>"
        "Drag is air resistance opposing rocket motion. Drag depends on "
        "speed, air density and rocket shape. Engineers design rockets "
        "to be aerodynamic to reduce drag.</div>", unsafe_allow_html=True)

        st.markdown("<div class='explain-box'><b>Payload</b><br>"
        "Payload is the cargo carried by the rocket such as satellites "
        "or astronauts. Increasing payload increases rocket mass and "
        "requires greater thrust and fuel.</div>", unsafe_allow_html=True)

        st.markdown("<div class='explain-box'><b>Guiding Questions + Answers</b><br>"
        "<b>How does adding payload affect altitude?</b><br>"
        "More payload increases rocket mass which reduces acceleration "
        "and lowers achievable altitude.<br><br>"
        "<b>How does increasing thrust affect launch success?</b><br>"
        "Higher thrust increases acceleration and helps rockets overcome "
        "gravity and drag.<br><br>"
        "<b>Does lower drag improve speed?</b><br>"
        "Yes. Lower drag allows rockets to maintain higher velocities.<br><br>"
        "<b>How long to reach orbit?</b><br>"
        "Most rockets reach orbit within about 8-12 minutes after launch."
        "</div>", unsafe_allow_html=True)

    # ============================================================
    # SETTINGS
    # ============================================================

    with tab8:

        if st.button("Sign Out"):
            st.session_state.page="landing"
            st.session_state.user=None
            st.rerun()

    # ============================================================
    # FEEDBACK
    # ============================================================

    st.divider()

    feedback = st.text_area("Share feedback")

    rating = st.slider("Rate the app",1,5,4)

    if st.button("Submit Feedback"):
        st.success("Thanks for your feedback!")
