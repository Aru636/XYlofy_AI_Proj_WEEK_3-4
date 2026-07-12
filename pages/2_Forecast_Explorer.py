import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("🔮 Forecast Explorer")

forecast = pd.read_csv("data/forecast_results.csv")

metrics = pd.read_csv("data/metrics.csv")

# //dropdown
segment = st.selectbox(

    "Select Category or Region",

    forecast["Segment"].unique()

)
# //slider
months = st.slider(

    "Forecast Horizon",

    1,

    3,

    3

)


# filter

result = (

    forecast[
        forecast["Segment"] == segment
    ]

    .head(months)

)

# plot

fig = px.line(

    result,

    x="Month",

    y="Forecast",

    markers=True,

    title=f"{segment} Forecast"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# table
st.dataframe(
    result,
    use_container_width=True
)

# Metrics
col1,col2,col3 = st.columns(3)

col1.metric(
    "MAE",
    f"{metrics.loc[0,'MAE']:.2f}"
)

col2.metric(
    "RMSE",
    f"{metrics.loc[0,'RMSE']:.2f}"
)

col3.metric(
    "MAPE",
    f"{metrics.loc[0,'MAPE']:.2f}%"
)