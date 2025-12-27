import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuration ---
st.set_page_config(
    page_title="Freehold Household Head Data Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set the URL for the raw CSV data on GitHub
DATA_URL = 'https://raw.githubusercontent.com/nrhdyh/Smart_Agriculture/refs/heads/main/freehold_data_on_Climate_Smart_Agriculture.csv'
PLOTLY_TEMPLATE = 'plotly_dark'

# Define encoding mapping
encoding_mapping = {
    'Level of education': ['No formal education', 'Primary school', 'Secondary school', 'College/University', 'Vocational'],
    'Water harvesting': ['No Adoption', 'Adopted'],
    'Agroforestry': ['None', 'Low', 'Medium', 'High'],
    'Marital status': ['Single', 'Married', 'Divorced', 'Widowed'],
    'Perception of climate change': ['Low Perception', 'Medium Perception', 'High Perception'],
    'If household has a land use plan': ['No Plan', 'Has Plan']
}

# --- Data Loading ---
@st.cache_data
def load_data(url):
    try:
        data = pd.read_csv(url)
        data = data.rename(columns={'ï»¿Gender of household head': 'Gender of household head'})
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

freehold_df = load_data(DATA_URL)

# --- Streamlit Layout ---
st.title("📊 Freehold Household Head Data Analysis")

if freehold_df.empty:
    st.warning("Could not load data. Please check the URL and file format.")
else:
    # --- Objective 2 ---
    st.header("🔬 Objective 2: Climate-Smart Agriculture Insights")
    st.markdown("""
    The objective is to analyze water harvesting adoption by education level, the relationship between land size and agroforestry, 
    perceptions of climate change by marital status, and the proportion of households with a land use plan.
    """)

    # ===========================
    # 📦 INTERACTIVE SUMMARY BOXES
    # ===========================
    st.subheader("📈 Summary Highlights")

    # ---- Metrics Calculation ----
    adoption_rate = (freehold_df['Water harvesting'].mean() * 100) if 'Water harvesting' in freehold_df.columns else 0
    avg_land_size = round(freehold_df['Land size'].mean(), 2) if 'Land size' in freehold_df.columns else 0
    high_perception_rate = ((freehold_df['Perception of climate change'] == 2).sum() / len(freehold_df) * 100) if 'Perception of climate change' in freehold_df.columns else 0
    land_plan_rate = ((freehold_df['If household has a land use plan'] == 1).sum() / len(freehold_df) * 100) if 'If household has a land use plan' in freehold_df.columns else 0

    # ---- Layout for 4 boxes ----
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("### 💧 Water Harvesting Adoption")
        st.metric(label="Adoption Rate", value=f"{adoption_rate:.1f}%")
        st.progress(adoption_rate / 100)
        st.caption("Reflects the percentage of households that adopted water harvesting practices.")

    with c2:
        st.markdown("### 🌳 Average Land Size")
        st.metric(label="Mean Land Size", value=f"{avg_land_size} ha")
        st.progress(min(avg_land_size / 10, 1.0))
        st.caption("Represents the average size of land owned across all households.")

    with c3:
        st.markdown("### ☀️ High Climate Change Awareness")
        st.metric(label="High Perception", value=f"{high_perception_rate:.1f}%")
        st.progress(high_perception_rate / 100)
        st.caption("Shows the percentage of households with high climate change awareness.")

    with c4:
        st.markdown("### 🗺️ Land Use Planning")
        st.metric(label="Households with Plan", value=f"{land_plan_rate:.1f}%")
        st.progress(land_plan_rate / 100)
        st.caption("Percentage of households that have developed a land use plan.")

    st.markdown("---")

    st.subheader("Raw Data Sample")
    st.dataframe(freehold_df.head())
    st.markdown("---")

    # 1. Water Harvesting Adoption by Level of Education
    st.subheader("1. Water Harvesting Adoption by Level of Education")

    education_labels = encoding_mapping['Level of education']
    water_harvesting_labels = encoding_mapping['Water harvesting']

    fig_edu_water = px.histogram(
        freehold_df,
        x='Level of education',
        color='Water harvesting',
        title='Water Harvesting Adoption by Level of Education',
        template=PLOTLY_TEMPLATE,
        barmode='group'
    )

    fig_edu_water.update_layout(
        xaxis={'tickvals': list(range(len(education_labels))), 'ticktext': education_labels},
        legend=dict(title='Water Harvesting', orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig_edu_water.for_each_trace(
        lambda t: t.update(name=water_harvesting_labels[int(t.name)]) if t.name.isdigit() and int(t.name) < len(water_harvesting_labels) else t
    )

    st.plotly_chart(fig_edu_water, use_container_width=True)
    st.markdown("""
    The bar chart shows the relationship between education level and the adoption of water harvesting. 
    The chart can be seen as that people with no formal education have the highest number of adopters and followed by those with primary education. 
    In contrast, the number of adopters decreases as the level of education increases with the lowest adoption seen among individuals with secondary and college or university education. 
    This suggests that people with lower levels of education are more likely to adopt water harvesting practices because they rely more on traditional or self-sufficient methods for water use.
    """)
    st.markdown("---")

    # 2. Land Size vs. Agroforestry Levels
    st.subheader("2. Land Size vs. Agroforestry Levels")

    agroforestry_labels = encoding_mapping['Agroforestry']

    fig_land_agro = px.box(
        freehold_df,
        x='Agroforestry',
        y='Land size',
        title='Land Size vs. Agroforestry Levels',
        template=PLOTLY_TEMPLATE,
        points='all'
    )

    fig_land_agro.update_layout(
        xaxis={'tickvals': list(range(len(agroforestry_labels))), 'ticktext': agroforestry_labels},
        yaxis_title="Land Size",
        xaxis_title="Agroforestry Level"
    )

    st.plotly_chart(fig_land_agro, use_container_width=True)
    st.markdown("""
    This box plot compares the land sizes of households based on their level of agroforestry practice and their categorized into “None” and “Low.” 
    The chart shows that both groups have a similar median land size, meaning the typical amount of land owned is almost the same whether a household practices low-level agroforestry or none at all. 
    However, the spread of land sizes is wider for the “None” group with several households owning significantly larger plots as shown by the outliers above the main box. 
    Overall, the visualization suggests that land size alone does not strongly influence whether a household adopts agroforestry, as both small and large land owners can be found in either category.
    """)
    st.markdown("---")

    # 3. Perception of Climate Change by Marital Status
    st.subheader("3. Perception of Climate Change by Marital Status")

    marital_labels = encoding_mapping['Marital status']
    perception_labels = encoding_mapping['Perception of climate change']

    fig_marital_perception = px.histogram(
        freehold_df,
        x='Marital status',
        color='Perception of climate change',
        title='Perception of Climate Change by Marital Status',
        template=PLOTLY_TEMPLATE,
        barmode='group'
    )

    fig_marital_perception.update_layout(
        xaxis={'tickvals': list(range(len(marital_labels))), 'ticktext': marital_labels},
        legend=dict(title='Perception', orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig_marital_perception.for_each_trace(
        lambda t: t.update(name=perception_labels[int(t.name)]) if t.name.isdigit() and int(t.name) < len(perception_labels) else t
    )

    st.plotly_chart(fig_marital_perception, use_container_width=True)
    st.markdown("""
    The bar chart shows how the individuals perception of climate change differs based on their marital status. 
    It can be seen that single individuals make up most of the respondents and have both high and low levels of perception about climate change while only a few have a medium level of perception. 
    In contrast, married individuals are fewer in number and generally show lower levels of perception, with very few having a high perception. 
    Overall, this suggests that single individuals tend to be more aware or concerned about climate change compared to married individuals.
    """)
    st.markdown("---")

    # 4. Proportion of Households with a Land Use Plan
    st.subheader("4. Proportion of Households with a Land Use Plan")

    land_use_plan_labels = encoding_mapping['If household has a land use plan']
    land_use_plan_counts = freehold_df['If household has a land use plan'].value_counts().reset_index()
    land_use_plan_counts.columns = ['If household has a land use plan', 'Count']

    fig_land_use_plan = px.pie(
        land_use_plan_counts,
        values='Count',
        names='If household has a land use plan',
        title='Proportion of Households with a Land Use Plan',
        template=PLOTLY_TEMPLATE
    )

    fig_land_use_plan.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig_land_use_plan, use_container_width=True)
    st.markdown("""
    This pie chart shows the percentage of households that have a land use plan and those that has not. 
    The majority of households of **77.8%**, do not have any land use plan, while only **22.2%** have one. 
    This means that most households are not planning or organizing how their land is used. 
    The chart makes it clear that only a small portion of households are taking steps to manage their land properly. 
    This could mean that many people may not be aware of the benefits of land planning or may not have the resources to do it. 
    Overall, the chart highlights a need for more support or awareness to help households create land use plans.
    """)
    st.markdown("---")

