import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(page_title="Electric Pole Hazard Predictor", page_icon="⚡", layout="wide")

st.title("⚡ Urban Stray Electric Pole Current Leakage & Shock Hazard Predictor")
st.markdown("### AI-Driven Municipal Safety & Preventive Risk Mapping System")
st.write("This system calculates a multi-factor **Electrocution Risk Score** for urban street light poles during monsoon conditions to prevent public shock hazards before they occur.")

# Sidebar Controls for Environmental & City Simulation
st.sidebar.header("🌧️ Environmental Simulation Controls")
rainfall = st.sidebar.slider("Monsoon Rainfall Intensity (mm/hr)", 0, 100, 45)
waterlogging = st.sidebar.selectbox("Area Drainage & Waterlogging Status", ["Low", "Moderate", "Critical/Overflow"])
humidity = st.sidebar.slider("Ambient Humidity (%)", 40, 95, 85)

# Simulated Dataset of City Electric Poles
@st.cache_data
def load_pole_data():
    data = {
        "Pole_ID": [f"POL-{101+i}" for i in range(10)],
        "Location": ["Civil Lines", "Itwari Market", "Sitabuldi Main Rd", "Sadar Bazar", "Dharampeth", 
                     "Laxmi Nagar", "Pratap Nagar", "Manish Nagar", "Hingna T-Point", "Ramdaspeth"],
        "Pole_Age_Years": [12, 3, 15, 8, 2, 14, 5, 11, 7, 13],
        "Material": ["Cast Iron", "Galvanized Steel", "Cast Iron", "Galvanized Steel", "Aluminum", 
                     "Cast Iron", "Galvanized Steel", "Cast Iron", "Galvanized Steel", "Cast Iron"],
        "Last_Maintenance_Months": [18, 2, 24, 10, 1, 20, 6, 15, 9, 22]
    }
    return pd.DataFrame(data)

df = load_pole_data()

# AI Risk Scoring Logic (Heuristic Matrix)
def calculate_risk(row, rain, water_status, hum):
    score = 0
    
    # Factor 1: Pole Age weight
    score += row["Pole_Age_Years"] * 2.5
    
    # Factor 2: Material Risk (Cast Iron rusts faster and leaks current easily)
    if row["Material"] == "Cast Iron":
        score += 20
    else:
        score += 5
        
    # Factor 3: Maintenance delay weight
    score += row["Last_Maintenance_Months"] * 1.8
    
    # Factor 4: Environmental / Monsoon weight
    score += rain * 0.35
    score += (hum - 50) * 0.2
    
    if water_status == "Critical/Overflow":
        score += 30
    elif water_status == "Moderate":
        score += 15
    else:
        score += 0
        
    # Cap score between 0 and 100
    return min(max(int(score), 5), 99)

# Apply AI calculation to all poles
df["Hazard_Risk_Score"] = df.apply(lambda row: calculate_risk(row, rainfall, waterlogging, humidity), axis=1)

# Categorize Risk Status
def get_status(score):
    if score >= 75:
        return "🔴 CRITICAL HAZARD"
    elif score >= 50:
        return "🟠 MODERATE RISK"
    else:
        return "🟢 SAFE"

df["Status"] = df["Hazard_Risk_Score"].apply(get_status)

# Sort by highest risk first (Priority Queue / Heuristic Ranking)
df = df.sort_values(by="Hazard_Risk_Score", ascending=False).reset_index(drop=True)

# Main Dashboard Display
col1, col2, col3 = st.columns(3)
col1.metric("Total Poles Monitored", len(df))
col2.metric("Critical Hazards Detected", len(df[df["Status"] == "🔴 CRITICAL HAZARD"]))
col3.metric("System Status", "AI Active & Secure", "100% Deterministic")

st.markdown("---")
st.subheader("📍 City-Wide Pole Risk Assessment & Priority Inspection Table")
st.write("The table below ranks electric poles dynamically based on environmental conditions and historical wear-and-tear parameters:")

# Display the dataframe
st.dataframe(df, use_container_width=True)

# Highlight Top Critical Action Items
st.markdown("---")
st.subheader("🚨 Immediate Municipal Action Dispatch List")
critical_poles = df[df["Status"] == "🔴 CRITICAL HAZARD"]

if not critical_poles.empty:
    st.error(f"Attention: {len(critical_poles)} poles require immediate electrical shutdown and grounding inspection dispatch!")
    for idx, row in critical_poles.iterrows():
        st.markdown(f"- **{row['Pole_ID']} ({row['Location']})**: Risk Score **{row['Hazard_Risk_Score']}/100** — *Age: {row['Pole_Age_Years']} yrs, Last Maintained: {row['Last_Maintenance_Months']} months ago.*")
else:
    st.success("All monitored poles are currently within safe hazard limits under current weather parameters.")