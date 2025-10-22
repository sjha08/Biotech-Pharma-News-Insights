# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 1. Page config
# -----------------------------
st.set_page_config(
    page_title="Biotech & Pharma News Insights",
    layout="wide",
)

st.title("Biotech & Pharma News Insights Dashboard")
st.markdown("""
Interactive dashboard to explore research publication trends and therapeutic area activity
across biotech and pharma companies.
""")

# -----------------------------
# 2. Load sample data
# -----------------------------
# Replace this with your CSV file path
# Example: df = pd.read_csv("pharma_headlines.csv")

# For demonstration, we generate sample data
data = {
    "company": ["Genentech", "Pfizer", "Amgen", "Gilead", "Genentech", "Pfizer", "Amgen", "Gilead"],
    "publication_date": pd.date_range(start="2023-01-01", periods=8, freq="M"),
    "therapeutic_area": ["Oncology", "Immunology", "Oncology", "Virology", "Oncology", "Immunology", "Oncology", "Virology"],
    "headline": [
        "Cancer immunotherapy breakthrough",
        "New antiviral treatment approved",
        "CAR-T cell therapy success",
        "HIV research milestone",
        "AI-driven oncology research",
        "Vaccine efficacy study",
        "Novel oncology compound",
        "Antiviral pipeline expansion"
    ]
}

df = pd.DataFrame(data)

# -----------------------------
# 3. Sidebar filters
# -----------------------------
st.sidebar.header("Filter Options")
companies = df["company"].unique().tolist()
selected_companies = st.sidebar.multiselect("Select Company", companies, default=companies)

therapeutic_areas = df["therapeutic_area"].unique().tolist()
selected_areas = st.sidebar.multiselect("Select Therapeutic Area", therapeutic_areas, default=therapeutic_areas)

# Apply filters
filtered_df = df[(df["company"].isin(selected_companies)) & (df["therapeutic_area"].isin(selected_areas))]

# -----------------------------
# 4. Display filtered data
# -----------------------------
st.subheader("Filtered Headlines")
st.dataframe(filtered_df.reset_index(drop=True))

# -----------------------------
# 5. Trend visualization
# -----------------------------
st.subheader("Publication Trends Over Time")
trend_df = filtered_df.groupby(["publication_date", "company"]).size().reset_index(name="count")

fig = px.line(
    trend_df,
    x="publication_date",
    y="count",
    color="company",
    markers=True,
    title="Monthly Publication Counts by Company"
)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 6. Therapeutic area distribution
# -----------------------------
st.subheader("Therapeutic Area Distribution")
area_df = filtered_df["therapeutic_area"].value_counts().reset_index()
area_df.columns = ["Therapeutic Area", "Count"]

fig2 = px.pie(
    area_df,
    names="Therapeutic Area",
    values="Count",
    title="Distribution of Headlines by Therapeutic Area"
)
st.plotly_chart(fig2, use_container_width=True)
