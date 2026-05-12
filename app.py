import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="LATAM Economic Bloc",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("data/latam_clean_dataset.csv")

# =========================
# TITLE
# =========================

st.title("LATAM Economic Bloc Simulation")

st.markdown("""
Interactive dashboard exploring economic development,
trade, education, and regional indicators across Latin America.
""")

# =========================
# COUNTRY SELECTOR
# =========================

country = st.selectbox(
    "Select a country",
    sorted(df['country'].unique())
)

filtered = df[df['country'] == country]

# =========================
# GDP CHART
# =========================

fig = px.line(
    filtered,
    x='year',
    y='gdp',
    title=f'{country} GDP Over Time'
)

st.plotly_chart(fig, use_container_width=True)
