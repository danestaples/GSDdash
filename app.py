import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('GSD.csv')
    df['Profit Margin'] = df['Profit Margin'].str.replace('%', '').astype(float)
    return df

df = load_data()

st.set_page_config(layout="wide", page_title="Express vs Standard Profit Dashboard")
st.title("📦 Express vs Standard Shipping: Profit Margin Dashboard")
st.markdown("This dashboard provides an in-depth view of how shipping method affects profit margins. Use the filters and tabs to explore insights for Operations, Marketing, and Management.")

# Sidebar filters
st.sidebar.header("Filter Data")
year = st.sidebar.multiselect("Select Year", sorted(df['Year'].unique()), default=sorted(df['Year'].unique()))
market = st.sidebar.multiselect("Select Market", sorted(df['Market'].unique()), default=sorted(df['Market'].unique()))
region = st.sidebar.multiselect("Select Region", sorted(df['Region'].unique()), default=sorted(df['Region'].unique()))
ship_mode = st.sidebar.multiselect("Select Shipping Type", sorted(df['Express Flag'].unique()), default=sorted(df['Express Flag'].unique()))

# Filtered dataframe
filtered_df = df[
    (df['Year'].isin(year)) &
    (df['Market'].isin(market)) &
    (df['Region'].isin(region)) &
    (df['Express Flag'].isin(ship_mode))
]

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Summary", "🚚 Operations", "📈 Marketing"])

# TAB 1 - SUMMARY
with tab1:
    st.subheader("1. Shipping Volume Distribution")
    st.markdown("This chart shows the volume of Express vs Standard shipments.")
    count_chart = filtered_df['Express Flag'].value_counts().reset_index()
    fig1 = px.bar(count_chart, x='index', y='Express Flag', labels={'index': 'Shipping Type', 'Express Flag': 'Order Count'}, text_auto=True)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("2. Profit Margin Distribution by Shipping Type")
    st.markdown("Compare how profit margins vary between Express and Standard.")
    fig2 = px.box(filtered_df, x='Express Flag', y='Profit Margin', color='Express Flag')
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("3. Monthly Trends in Profit Margin")
    st.markdown("Track how profit margins shift over time by shipping type.")
    monthly = filtered_df.groupby(['Year-Month', 'Express Flag'])['Profit Margin'].mean().reset_index()
    fig3 = px.line(monthly, x='Year-Month', y='Profit Margin', color='Express Flag')
    st.plotly_chart(fig3, use_container_width=True)

# TAB 2 - OPERATIONS
with tab2:
    st.subheader("4. Average Ship Lag")
    st.markdown("Average shipping delay in days by shipping method.")
    fig4 = px.box(filtered_df, x='Express Flag', y='Ship Lag Adjusted', color='Express Flag')
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("5. Shipping Cost Distribution")
    st.markdown("Distribution of shipping costs between methods.")
    fig5 = px.histogram(filtered_df, x='Shipping.Cost', color='Express Flag', marginal='box')
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("6. Ship Mode vs Ship Lag")
    st.markdown("Understand operational delay by ship mode.")
    fig6 = px.box(filtered_df, x='Ship.Mode', y='Ship Lag', color='Express Flag')
    st.plotly_chart(fig6, use_container_width=True)

    st.subheader("7. Region-wise Shipping Delay")
    st.markdown("Region-wise average ship lag.")
    region_lag = filtered_df.groupby('Region')['Ship Lag'].mean().reset_index()
    fig7 = px.bar(region_lag, x='Region', y='Ship Lag', text_auto=True)
    st.plotly_chart(fig7, use_container_width=True)

# TAB 3 - MARKETING
with tab3:
    st.subheader("8. Profit Margin by Product Category")
    st.markdown("Profit margin distribution by category and shipping type.")
    fig8 = px.box(filtered_df, x='Category', y='Profit Margin', color='Express Flag')
    st.plotly_chart(fig8, use_container_width=True)

    st.subheader("9. Profit Margin by Sub-Category")
    st.markdown("Explore profit variations by product sub-category.")
    fig9 = px.box(filtered_df, x='Sub.Category', y='Profit Margin', color='Express Flag')
    st.plotly_chart(fig9, use_container_width=True)

    st.subheader("10. Market-wise Profitability")
    st.markdown("Profit margin comparison across different markets.")
    fig10 = px.box(filtered_df, x='Market', y='Profit Margin', color='Express Flag')
    st.plotly_chart(fig10, use_container_width=True)

    st.subheader("11. State-wise Average Profit Margin")
    st.markdown("See which states perform better or worse.")
    state_avg = filtered_df.groupby('State')['Profit Margin'].mean().reset_index()
    fig11 = px.choropleth(state_avg, locations='State', locationmode='USA-states', color='Profit Margin', scope="usa")
    st.plotly_chart(fig11, use_container_width=True)
