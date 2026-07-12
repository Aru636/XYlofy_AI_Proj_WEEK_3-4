import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📦 Product Demand Segments")

cluster = pd.read_csv("data/cluster_results.csv")


# cluster labels

labels = {
    0: "Low Volume, Stable Demand",
    1: "Premium High-Value Products",
    2: "High Volume, Stable Demand",
    3: "Growing Demand"
}

cluster["Cluster Name"] = cluster["Cluster"].map(labels)

# PCA scatter plots
fig = px.scatter(
    cluster,
    x="PC1",
    y="PC2",
    color="Cluster Name",
    text="Sub-Category",
    title="Product Demand Segments (PCA)"
)

fig.update_traces(textposition="top center")

st.plotly_chart(fig, use_container_width=True)

# Cluster Table

st.subheader("Sub-Category Clusters")

st.dataframe(
    cluster[
        [
            "Sub-Category",
            "Cluster Name",
            "TotalSales",
            "AverageOrderValue",
            "YoYGrowth"
        ]
    ],
    use_container_width=True
)

# Inventory Recommendations

st.subheader("Inventory Recommendations")

recommendations = pd.DataFrame({

"Cluster":[
"High Volume, Stable Demand",
"Premium High-Value Products",
"Low Volume, Stable Demand",
"Growing Demand"
],

"Recommendation":[
"Maintain high inventory and frequent replenishment.",
"Keep limited stock and replenish based on demand.",
"Maintain moderate inventory with periodic restocking.",
"Gradually increase inventory while monitoring demand."
]

})

st.table(recommendations)