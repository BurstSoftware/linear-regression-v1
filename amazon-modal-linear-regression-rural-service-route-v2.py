import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ====================== CONFIG ======================
st.set_page_config(page_title="Warehouse Performance Dashboard", layout="wide")
st.title("📦 Warehouse Pick & Stow Performance")
st.markdown("**April 5th - April 12th** | 40-Hour Work Week Visualization")

# ====================== DATA ======================
# Pick Data (Opportunities)
pick_data = {
    "User": ["stajenni", "narossoh", "arrizola", "hasnsai", "uiyps", "danijac", "gpliegom", "mtiband r", "eliz ev", "hersmary"],
    "Opportunities": [804, 746, 614, 214, 208, 169, 362, 68, 176, 69]
}

# Stow Data (Opportunities)
stow_data = {
    "User": ["narossoh", "mnimhas", "matstrak", "gpliegom", "iqrayuss", "uiyps", "hersmary", "danijac", "hasnsai", "eliz ev"],
    "Opportunities": [1068, 668, 594, 580, 758, 330, 246, 168, 416, 204]
}

pick_df = pd.DataFrame(pick_data)
stow_df = pd.DataFrame(stow_data)

# ====================== SIMULATE HOURLY DATA ======================
def simulate_hourly_cumulative(total, hours=40, seed=42):
    np.random.seed(seed)
    # Realistic hourly rate with variation
    hourly_rate = np.random.normal(total / hours, total / hours * 0.15, hours)
    hourly_rate = np.maximum(hourly_rate, 0)
    cumulative = np.cumsum(hourly_rate)
    cumulative[-1] = total  # Ensure it ends exactly at total
    return cumulative

hours = list(range(41))  # 0 to 40 hours

# Generate simulated data for top users
top_users = ["narossoh", "stajenni", "uiyps", "hersmary", "mnimhas", "matstrak", "gpliegom"]

pick_sim = {}
stow_sim = {}

for user in top_users:
    pick_total = pick_df[pick_df["User"] == user]["Opportunities"].values
    stow_total = stow_df[stow_df["User"] == user]["Opportunities"].values
    
    pick_sim[user] = simulate_hourly_cumulative(pick_total[0] if len(pick_total) > 0 else 0, seed=hash(user))
    stow_sim[user] = simulate_hourly_cumulative(stow_total[0] if len(stow_total) > 0 else 0, seed=hash(user)+1)

# ====================== LAYOUT ======================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📤 Pick Volume Over Time")
    fig_pick = go.Figure()
    for user in top_users:
        fig_pick.add_trace(go.Scatter(
            x=hours, y=pick_sim[user],
            mode='lines+markers',
            name=user,
            marker=dict(size=4)
        ))
    fig_pick.update_layout(
        xaxis_title="Hours Worked (0-40)",
        yaxis_title="Cumulative Units Picked",
        height=500,
        hovermode="x unified"
    )
    st.plotly_chart(fig_pick, use_container_width=True)

with col2:
    st.subheader("📥 Stow Volume Over Time")
    fig_stow = go.Figure()
    for user in top_users:
        fig_stow.add_trace(go.Scatter(
            x=hours, y=stow_sim[user],
            mode='lines+markers',
            name=user,
            marker=dict(size=4)
        ))
    fig_stow.update_layout(
        xaxis_title="Hours Worked (0-40)",
        yaxis_title="Cumulative Units Stowed",
        height=500,
        hovermode="x unified"
    )
    st.plotly_chart(fig_stow, use_container_width=True)

# ====================== TOTAL CUMULATIVE ======================
st.subheader("📊 Total Pick + Stow Volume (Combined)")

fig_total = go.Figure()
for user in top_users:
    total_cum = pick_sim[user] + stow_sim[user]
    fig_total.add_trace(go.Scatter(
        x=hours, y=total_cum,
        mode='lines+markers',
        name=user,
        marker=dict(size=4)
    ))

fig_total.update_layout(
    xaxis_title="Hours Worked (0-40)",
    yaxis_title="Cumulative Total Units Handled",
    height=600,
    hovermode="x unified"
)

st.plotly_chart(fig_total, use_container_width=True)

# ====================== SUMMARY TABLE ======================
st.subheader("📋 Weekly Summary (Opportunities)")

summary = pd.merge(pick_df, stow_df, on="User", how="outer", suffixes=("_Pick", "_Stow")).fillna(0)
summary["Total"] = summary["Opportunities_Pick"] + summary["Opportunities_Stow"]
summary = summary.sort_values("Total", ascending=False)
st.dataframe(summary, use_container_width=True)

# ====================== FOOTER ======================
st.caption("Simulated hourly progression based on weekly totals • Built with Streamlit & Plotly")
