import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("🚨 Anomaly Report")

df = pd.read_csv(
    "data/weekly_sales.csv",
    parse_dates=["Order Date"]
)

# Isolation forest plot
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Order Date"],
    y=df["Sales"],
    mode="lines",
    name="Weekly Sales"
))

iso = df[df["Anomaly"] == -1]

fig.add_trace(go.Scatter(
    x=iso["Order Date"],
    y=iso["Sales"],
    mode="markers",
    marker=dict(color="red", size=10),
    name="Isolation Forest"
))

fig.update_layout(
    title="Isolation Forest Anomaly Detection"
)

st.plotly_chart(fig, use_container_width=True)

# z-score plot
fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=df["Order Date"],
    y=df["Sales"],
    mode="lines",
    name="Weekly Sales"
))

z = df[df["Z_Anomaly"] == True]

fig2.add_trace(go.Scatter(
    x=z["Order Date"],
    y=z["Sales"],
    mode="markers",
    marker=dict(color="orange", size=10),
    name="Z-score"
))

fig2.update_layout(
    title="Rolling Z-score Detection"
)

st.plotly_chart(fig2, use_container_width=True)

# Tables
st.subheader("Isolation Forest Anomalies")

st.dataframe(
    iso[["Order Date", "Sales"]],
    use_container_width=True
)

st.subheader("Rolling Z-score Anomalies")

st.dataframe(
    z[["Order Date", "Sales"]],
    use_container_width=True
)

# Summary Cards

c1, c2 = st.columns(2)

c1.metric(
    "Isolation Forest",
    len(iso)
)

c2.metric(
    "Z-score",
    len(z)
)