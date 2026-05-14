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
# HANDLE MISSING SOCIAL DATA
# ======================================================

social_columns = [
    'poverty_rate',
    'tertiary_education'
]

df[social_columns] = (
    df.groupby('country')[social_columns]
    .ffill()
)

# ======================================================
# CLEAN YEAR COLUMN
# ======================================================

df['year'] = df['year'].astype(str)

# ======================================================
# FILTER LATEST YEAR
# ======================================================

latest = df[df['year'] == '2024']

# ======================================================
# CHART STYLE FUNCTION
# ======================================================

def style_chart(fig):

    fig.update_layout(
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        font_color='white',

        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    return fig

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

    st.caption("""
    Indicadores sociales faltantes fueron completados utilizando el último valor oficial disponible para mantener continuidad analítica regional.
    """)

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

latest_country = filtered[filtered['year'] == '2024']

# ======================================================
# GET KPI VALUES
# ======================================================

gdp = latest_country['gdp'].values[0]
gdp_per_capita = latest_country['gdp_per_capita'].values[0]
poverty = latest_country['poverty_rate'].values[0]
education = latest_country['tertiary_education'].values[0]

# ======================================================
# GDP GROWTH
# ======================================================

gdp_2019 = filtered[filtered['year'] == '2019']['gdp'].values[0]

growth = ((gdp - gdp_2019) / gdp_2019) * 100

# ======================================================
# ECONOMIC ANALYSIS LOGIC
# ======================================================

# GROWTH ANALYSIS

if growth > 20:
    growth_text = "una fuerte recuperación económica posterior a la pandemia"

elif growth > 0:
    growth_text = "un crecimiento económico moderado"

else:
    growth_text = "una desaceleración económica"

# POVERTY ANALYSIS

if poverty > 40:
    poverty_text = "altos niveles de vulnerabilidad social"

elif poverty > 20:
    poverty_text = "niveles moderados de pobreza"

else:
    poverty_text = "niveles relativamente bajos de pobreza"

# EDUCATION ANALYSIS

if education > 70:
    education_text = "una base sólida de capital humano"

elif education > 40:
    education_text = "un desarrollo educativo intermedio"

else:
    education_text = "desafíos estructurales en educación superior"

# ======================================================
# COUNTRY ANALYSIS SECTION
# ======================================================

st.divider()

analysis_col, kpi_col = st.columns([2, 1])

# ======================================================
# LEFT ANALYSIS
# ======================================================

with analysis_col:

    st.markdown(f"## Perfil Económico de {country}")

    st.markdown(f"""
    {country} presenta {growth_text} durante el periodo analizado entre 2015 y 2024.

    En términos sociales, el país mantiene {poverty_text}, lo que refleja diferencias estructurales en desarrollo económico y distribución de ingresos.

    Respecto al capital humano, los indicadores muestran {education_text}, factor que podría influir directamente en la capacidad de industrialización y crecimiento regional a largo plazo.

    Bajo un escenario de integración regional activa, economías con perfiles similares podrían beneficiarse de mayores niveles de inversión en infraestructura, manufactura y conectividad regional.
    """)

# ======================================================
# RIGHT KPI CARDS
# ======================================================

with kpi_col:

    st.markdown("## Indicadores Clave")

    top_kpis = st.columns(3)

    with top_kpis[0]:
        st.metric(
            "PIB 2024",
            f"${gdp / 1_000_000_000_000:.2f}T"
        )

    with top_kpis[1]:
        st.metric(
            "PIB per Cápita",
            f"${gdp_per_capita:,.0f}"
        )

    with top_kpis[2]:
        st.metric(
            "Pobreza",
            f"{poverty:.1f}%"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    bottom_left, edu_col, growth_col, bottom_right = st.columns([1,2,2,1])

    with edu_col:
        st.metric(
            "Educación",
            f"{education:.1f}%"
        )

    with growth_col:
        st.metric(
            "Growth Since 2019",
            f"{growth:.1f}%"
        )

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

style_chart(fig_gdp)

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

style_chart(fig_gdp_capita)

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

style_chart(fig_poverty)

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

style_chart(fig_education)

st.plotly_chart(
    fig_education,
    use_container_width=True
)

# ======================================================
# DATA NOTE
# ======================================================

st.caption("""
Nota: Algunos países presentan valores faltantes en indicadores sociales debido a disponibilidad limitada de datos en las fuentes originales del Banco Mundial.
""")
st.header("Simulación de Integración Pasiva")

# =====================================================
# CLEAN YEAR
# =====================================================

df['year'] = df['year'].astype(int)

# =====================================================
# KEEP ONLY GDP DATA
# =====================================================

gdp_df = df[['country', 'year', 'gdp']].copy()

# =====================================================
# REMOVE COUNTRIES WITH MISSING GDP
# =====================================================

pivot_check = gdp_df.pivot_table(
    index='country',
    columns='year',
    values='gdp'
)

valid_countries = pivot_check.dropna(
    subset=[2015, 2024]
).index

gdp_df = gdp_df[
    gdp_df['country'].isin(valid_countries)
]

# =====================================================
# GET INITIAL + FINAL GDP
# =====================================================

gdp_2015 = gdp_df[
    gdp_df['year'] == 2015
][['country', 'gdp']].rename(
    columns={'gdp': 'gdp_2015'}
)

gdp_2024 = gdp_df[
    gdp_df['year'] == 2024
][['country', 'gdp']].rename(
    columns={'gdp': 'gdp_2024'}
)

# =====================================================
# MERGE
# =====================================================

growth_df = gdp_2015.merge(
    gdp_2024,
    on='country'
)

# =====================================================
# CALCULATE CAGR
# =====================================================

growth_df['cagr'] = (
    (
        growth_df['gdp_2024']
        / growth_df['gdp_2015']
    ) ** (1 / 9)
) - 1

# =====================================================
# FUTURE YEARS
# =====================================================

future_years = [
    2035,
    2045,
    2055,
    2065,
    2075
]

# =====================================================
# CREATE PROJECTIONS
# =====================================================

projection_rows = []

for _, row in growth_df.iterrows():

    country = row['country']
    current_gdp = row['gdp_2024']
    cagr = row['cagr']

    for year in future_years:

        years_forward = year - 2024

        projected_gdp = (
            current_gdp
            * ((1 + cagr) ** years_forward)
        )

        projection_rows.append({
            'country': country,
            'year': year,
            'projected_gdp': projected_gdp,
            'cagr': cagr
        })

# =====================================================
# CREATE PROJECTION DATAFRAME
# =====================================================

projection_df = pd.DataFrame(projection_rows)

# =====================================================
# REGIONAL GDP
# =====================================================

regional_projection = projection_df.groupby(
    'year'
)['projected_gdp'].sum().reset_index()

# =====================================================
# REGIONAL CHART
# =====================================================

fig_region = px.line(
    regional_projection,
    x='year',
    y='projected_gdp',
    markers=True,
    title='Proyección Económica LATAM — Integración Pasiva'
)

style_chart(fig_region)

st.plotly_chart(
    fig_region,
    use_container_width=True
)

# =====================================================
# COUNTRY DROPDOWN SIMULATION
# =====================================================

country_selected = st.selectbox(
    "Selecciona un país para simulación",
    sorted(projection_df['country'].unique())
)

country_projection = projection_df[
    projection_df['country'] == country_selected
]

# =====================================================
# COUNTRY CHART
# =====================================================

fig_country = px.line(
    country_projection,
    x='year',
    y='projected_gdp',
    markers=True,
    title=f'Proyección Económica de {country_selected}'
)

style_chart(fig_country)

st.plotly_chart(
    fig_country,
    use_container_width=True
)

# =====================================================
# DISPLAY DATA
# =====================================================
projection_display = projection_df.rename(columns={
    'country': 'País',
    'year': 'Año',
    'projected_gdp': 'PIB Proyectado',
    'cagr': 'Crecimiento Anual'
})

filtered_projection = projection_display[
    projection_display['País'] == country_selected
]

st.dataframe(
    filtered_projection,
    use_container_width=True
)
# =====================================================
# ACTIVE INTEGRATION SIMULATION
# =====================================================

st.divider()

st.header("Simulación de Integración Activa")

st.markdown("""
Este escenario simula una Latinoamérica con mayor coordinación económica regional, donde las economías líderes impulsan inversión estratégica en infraestructura, manufactura, conectividad y desarrollo regional.
""")

# =====================================================
# COUNTRY GROUPS
# =====================================================

leader_countries = [
    'Mexico',
    'Brazil',
    'Chile'
]

middle_countries = [
    'Argentina',
    'Colombia',
    'Peru',
    'Costa Rica',
    'Panama',
    'Uruguay'
]

# =====================================================
# CREATE ACTIVE PROJECTIONS
# =====================================================

active_projection_rows = []

for _, row in growth_df.iterrows():

    country = row['country']
    current_gdp = row['gdp_2024']
    cagr = row['cagr']

    # =================================================
    # APPLY REGIONAL MULTIPLIERS
    # =================================================

    if country in leader_countries:

        adjusted_cagr = cagr * 0.95

    elif country in middle_countries:

        adjusted_cagr = cagr * 1.15

    else:

        adjusted_cagr = cagr * 1.35

    # =================================================
    # FUTURE PROJECTIONS
    # =================================================

    for year in future_years:

        years_forward = year - 2024

        projected_gdp = (
            current_gdp
            * ((1 + adjusted_cagr) ** years_forward)
        )

        active_projection_rows.append({
            'country': country,
            'year': year,
            'projected_gdp': projected_gdp,
            'adjusted_cagr': adjusted_cagr
        })

# =====================================================
# CREATE ACTIVE DATAFRAME
# =====================================================

active_projection_df = pd.DataFrame(
    active_projection_rows
)

# =====================================================
# REGIONAL ACTIVE GDP
# =====================================================

active_regional_projection = (
    active_projection_df
    .groupby('year')['projected_gdp']
    .sum()
    .reset_index()
)

# =====================================================
# REGIONAL ACTIVE CHART
# =====================================================

fig_active_region = px.line(
    active_regional_projection,
    x='year',
    y='projected_gdp',
    markers=True,
    title='Proyección Regional LATAM — Integración Activa'
)

style_chart(fig_active_region)

st.plotly_chart(
    fig_active_region,
    use_container_width=True
)

# =====================================================
# ACTIVE COUNTRY SELECTOR
# =====================================================

active_country_selected = st.selectbox(
    "Selecciona un país para simulación activa",
    sorted(active_projection_df['country'].unique())
)

# =====================================================
# FILTER COUNTRY
# =====================================================

active_country_projection = (
    active_projection_df[
        active_projection_df['country']
        == active_country_selected
    ]
)

# =====================================================
# ACTIVE COUNTRY CHART
# =====================================================

fig_active_country = px.line(
    active_country_projection,
    x='year',
    y='projected_gdp',
    markers=True,
    title=f'Proyección Activa de {active_country_selected}'
)

style_chart(fig_active_country)

st.plotly_chart(
    fig_active_country,
    use_container_width=True
)

# =====================================================
# ACTIVE TABLE
# =====================================================

active_display = active_projection_df.rename(columns={
    'country': 'País',
    'year': 'Año',
    'projected_gdp': 'PIB Proyectado',
    'adjusted_cagr': 'Crecimiento Ajustado'
})

filtered_active = active_display[
    active_display['País']
    == active_country_selected
]

st.dataframe(
    filtered_active,
    use_container_width=True
)

# =====================================================
# ACTIVE ANALYSIS
# =====================================================

st.markdown(f"""
### Análisis Regional — {active_country_selected}

Bajo un modelo de integración activa, {active_country_selected} podría experimentar un crecimiento económico influenciado por mayores niveles de cooperación regional, inversión estratégica y fortalecimiento de cadenas productivas latinoamericanas.

En este escenario, el crecimiento regional se distribuye de forma más equilibrada entre economías líderes, intermedias y vulnerables, reduciendo parcialmente las diferencias estructurales históricas de la región.
""")

# =====================================================
# METHODOLOGICAL NOTE
# =====================================================

st.divider()

st.subheader("Consideraciones Metodológicas")

st.markdown("""
Este proyecto representa una simulación exploratoria basada principalmente en tendencias históricas de crecimiento económico y algunos indicadores estructurales disponibles para la región.

Las proyecciones actuales no consideran variables complejas como crecimiento poblacional, envejecimiento demográfico, inflación, productividad laboral, automatización, estabilidad política, deuda pública, cambio climático, migración o transformaciones tecnológicas disruptivas.

El objetivo principal del proyecto es explorar posibles escenarios de integración económica regional y visualizar cómo distintas dinámicas de cooperación podrían impactar el crecimiento latinoamericano a largo plazo.

Actualmente el modelo continúa en desarrollo con el objetivo de integrar variables económicas, sociales y demográficas adicionales para construir simulaciones regionales más robustas y multidimensionales.
""")
