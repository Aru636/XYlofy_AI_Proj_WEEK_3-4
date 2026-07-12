import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📊 Sales Overview Dashboard")

df = pd.read_csv(
    "data/Sample - Superstore.csv",
    parse_dates=["Order Date"]
)

df['Order Date'] = pd.to_datetime(df['Order Date'],format="%d/%m/%Y")
df['Ship Date'] = pd.to_datetime(df['Ship Date'],format="%d/%m/%Y")

# KPI CARDs

total_sales = df["Sales"].sum()
total_orders = len(df)
avg_sales = df["Sales"].mean()
# avg_profit = df["Profit"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Average Order Value", f"${avg_sales:,.2f}")
# col4.metric("Average Profit", f"${avg_profit:,.2f}")


# Sidebar filter

st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

categories = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

filtered = df[
    (df["Region"].isin(regions))
    &
    (df["Category"].isin(categories))
]

# Sales by Year

filtered["Year"] = filtered["Order Date"].dt.year

year_sales = (
    filtered
    .groupby("Year")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    year_sales,
    x="Year",
    y="Sales",
    title="Total Sales by Year"
)

st.plotly_chart(fig, width='stretch')

# Monthly Sales Trend

monthly = (
    filtered
    .set_index("Order Date")
    .resample("ME")["Sales"]
    .sum()
    .reset_index()
)

fig = px.line(
    monthly,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig, width='stretch')

# Sales by Region

region_sales = (
    filtered
    .groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region_sales,
    values="Sales",
    names="Region",
    title="Sales by Region"
)

st.plotly_chart(fig, width='stretch')

# Sales by Category

category_sales = (
    filtered
    .groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category",
    title="Sales by Category"
)

st.plotly_chart(fig, width='stretch')