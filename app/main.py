import streamlit as st
import pandas as pd
import plotly.express as px
from app.db.database import get_connection

st.set_page_config(page_title="Threat Intelligence Dashboard", layout="wide")

def load_data():
    """Loads all threat data from the database into a DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM threats", conn)
    conn.close()
    return df

# Load data
df = load_data()

# Title
st.title("🛡️ AI-Powered Threat Intelligence Dashboard")
st.markdown("Live threat data aggregated from AlienVault OTX and AbuseIPDB")

# AI Summary Section
st.divider()
st.subheader("🤖 AI Threat Summary")

if st.button("Generate Latest Summary"):
    with st.spinner("Analyzing recent threats with Gemini..."):
        from app.ai.summarizer import generate_summary
        summary = generate_summary()
        st.info(summary)
else:
    st.caption("Click the button above to generate an AI-powered summary of the latest threats.")

st.divider()

# Top metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Threats", len(df))
col2.metric("High Severity", len(df[df['severity'] == 'high']))
col3.metric("OTX Threats", len(df[df['source'] == 'OTX']))
col4.metric("AbuseIPDB Threats", len(df[df['source'] == 'AbuseIPDB']))

st.divider()

# Charts row
col1, col2 = st.columns(2)

with col1:
    st.subheader("Threats by Source")
    source_counts = df['source'].value_counts().reset_index()
    source_counts.columns = ['source', 'count']
    fig1 = px.pie(source_counts, names='source', values='count', hole=0.4)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Severity Breakdown")
    severity_counts = df['severity'].value_counts().reset_index()
    severity_counts.columns = ['severity', 'count']
    fig2 = px.bar(severity_counts, x='severity', y='count', color='severity',
                  color_discrete_map={'high': '#ff4444', 'medium': '#ffaa00', 'low': '#44ff44'})
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Country breakdown
st.subheader("Top Countries by Threat Count")
country_counts = df['country'].value_counts().head(10).reset_index()
country_counts.columns = ['country', 'count']
fig3 = px.bar(country_counts, x='country', y='count')
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Filters
st.subheader("🔍 Threat Data Explorer")
col1, col2 = st.columns(2)
with col1:
    source_filter = st.multiselect("Filter by Source", options=df['source'].unique(), default=df['source'].unique())
with col2:
    severity_filter = st.multiselect("Filter by Severity", options=df['severity'].unique(), default=df['severity'].unique())

filtered_df = df[(df['source'].isin(source_filter)) & (df['severity'].isin(severity_filter))]

st.dataframe(
    filtered_df[['source', 'indicator', 'indicator_type', 'threat_type', 'severity', 'country', 'timestamp']],
    use_container_width=True,
    height=400
)