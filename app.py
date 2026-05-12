import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="LATAM: Simulación de Integración Económica",
    layout="wide"
)

# ======================================================
# LOAD DATA
# ======================================================

df = pd.read_csv("latam_clean_dataset.csv")

# ======================================================
# CLEAN YEAR COLUMN
# ======================================================

df['year'] = df['year'].astype(str)

# ======================================================
# FILTER LATEST YEAR
# ======================================================

latest = df[df['year'] == '2024']

# ======================================================
# LATAM MAP
# ======================================================

fig_map = px.choropleth(
    latest,
    locations='country_code',
    color='gdp',
    hover_name='country',
    color_continuous_scale='Tealgrn',
    projection='natural earth',

    hover_data={
        'gdp': ':,.0f'
    }
)

fig_map.update_layout(
    paper_bgcolor='#0E1117',
    plot_bgcolor='#0E1117',
    font_color='white',

    height=650,

    margin=dict(
        l=0,
        r=0,
        t=0,
        b=0
    ),

    coloraxis_showscale=False,

    geo=dict(
        bgcolor='#0E1117',
        showframe=False,
        showcoastlines=False,
        fitbounds="locations",
        visible=False
    )
)

# ======================================================
# HERO SECTION
# ======================================================

col1, col2 = st.columns([1, 1.2])

# ======================================================
# LEFT COLUMN
# ======================================================
with col1:

    st.title("LATAM: Simulación de Integración Económica")

    st.markdown("""
    Este proyecto explora el potencial económico de Latinoamérica bajo un modelo hipotético de integración regional, utilizando datos históricos de PIB, educación, comercio y desarrollo humano.
    """)

    st.markdown("## Escenarios de Análisis")

    st.markdown("""
    ### Integración Pasiva

    Los países mantienen su desarrollo individual actual con niveles limitados de cooperación regional.
    """)

    st.markdown("---")

    st.markdown("""
    ### Integración Activa

    Un modelo de inversión estratégica donde las economías líderes reinvierten en infraestructura, manufactura, educación y conectividad regional.
    """)

    st.markdown("---")

    st.markdown("""
    ## Objetivo

    Visualizar, mediante dashboards interactivos y modelos probabilísticos, cómo la cooperación regional podría transformar las diferencias estructurales en crecimiento económico conjunto.
    """)

# ======================================================
# RIGHT COLUMN
# ======================================================

with col2:

    st.markdown(
    "<h3 style='text-align: center;'>Mapa Económico de Latinoamérica</h3>",
    unsafe_allow_html=True
)

    st.plotly_chart(
        fig_map,
        use_container_width=True
    )

    st.markdown("## Top 5 Economías por PIB")

    top_gdp = latest.sort_values(
        by='gdp',
        ascending=False
    ).head(5)

    kpi_cols = st.columns(5)

    for col, (_, row) in zip(kpi_cols, top_gdp.iterrows()):

        with col:

            gdp_trillion = row['gdp'] / 1_000_000_000_000

            st.metric(
                label=row['country'],
                value=f"${gdp_trillion:.2f}T"
            )

# ======================================================
# COUNTRY SELECTOR
# ======================================================

st.divider()

st.subheader("Análisis Individual por País")

country = st.selectbox(
    "Selecciona un país",
    sorted(df['country'].unique())
)

filtered = df[df['country'] == country]

# ======================================================
# GDP CHART
# ======================================================

fig_gdp = px.line(
    filtered,
    x='year',
    y='gdp',
    title=f'PIB de {country} a través del tiempo',
    markers=True
)

fig_gdp.update_layout(
    paper_bgcolor='#0E1117',
    plot_bgcolor='#0E1117',
    font_color='white'
)

st.plotly_chart(
    fig_gdp,
    use_container_width=True
)

# ======================================================
# GDP PER CAPITA
# ======================================================

fig_gdp_capita = px.line(
    filtered,
    x='year',
    y='gdp_per_capita',
    title=f'PIB Per Cápita de {country}',
    markers=True
)

fig_gdp_capita.update_layout(
    paper_bgcolor='#0E1117',
    plot_bgcolor='#0E1117',
    font_color='white'
)

st.plotly_chart(
    fig_gdp_capita,
    use_container_width=True
)

# ======================================================
# POVERTY RATE
# ======================================================

fig_poverty = px.line(
    filtered,
    x='year',
    y='poverty_rate',
    title=f'Pobreza en {country}',
    markers=True
)

fig_poverty.update_layout(
    paper_bgcolor='#0E1117',
    plot_bgcolor='#0E1117',
    font_color='white'
)

st.plotly_chart(
    fig_poverty,
    use_container_width=True
)

# ======================================================
# EDUCATION
# ======================================================

fig_education = px.line(
    filtered,
    x='year',
    y='tertiary_education',
    title=f'Educación Terciaria en {country}',
    markers=True
)

fig_education.update_layout(
    paper_bgcolor='#0E1117',
    plot_bgcolor='#0E1117',
    font_color='white'
)

st.plotly_chart(
    fig_education,
    use_container_width=True
)

st.caption("""
Nota: Algunos países presentan valores faltantes en indicadores sociales como pobreza y educación terciaria debido a disponibilidad limitada de datos en las fuentes originales del Banco Mundial.
""")
