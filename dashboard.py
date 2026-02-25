import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from analytics import run_analytics
import numpy as np 
 
st.set_page_config(
    page_title='CRM Analytics Dashboard',
    layout='wide'
)

data = run_analytics()

st.title('Client Relationship Management Dashboard')
st.caption('Global Markets & Investment Banking | Client Services Technology')
st.divider()
 
col1, col2, col3, col4 = st.columns(4)
col1.metric('Total Clients',      len(data))
col2.metric('High Priority',      (data.priority == 'HIGH').sum(),    delta='Requires Action')
col3.metric('At Risk',            (data.risk_flag == 'AT RISK').sum(), delta='Needs Follow-up', delta_color='inverse')
col4.metric('Avg Engagement',     f"{data.engagement_score.mean():.1f}/100")

st.divider()
 
st.sidebar.header('Filters')
region   = st.sidebar.multiselect('Region',      data['region'].unique(),     default=data['region'].unique())
product  = st.sidebar.multiselect('Product',     data['product'].unique(),    default=data['product'].unique())
priority = st.sidebar.multiselect('Priority',    ['HIGH','MEDIUM','LOW'],default=['HIGH','MEDIUM','LOW'])
 
filtered = data[
    data['region'].isin(region) &
    data['product'].isin(product) &
    data['priority'].isin(priority)
]
 
col_a, col_b = st.columns(2)
 
with col_a:
    st.subheader('Engagement Score by Region')
    fig1 = px.box(filtered, x='region', y='engagement_score',
                  color='region', points='all',
                  color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig1, use_container_width=True)
 
with col_b:
    st.subheader('Pipeline: Clients by Deal Stage')
    stage_counts = filtered.groupby('deal_stage').size().reset_index(name='count')
    fig2 = px.funnel(stage_counts, x='count', y='deal_stage',
                     color_discrete_sequence=['#1F4E79'])
    st.plotly_chart(fig2, use_container_width=True)
 
col_c, col_d = st.columns(2)
 
with col_c:
    st.subheader('AUM Distribution by Priority')
    fig3 = px.histogram(filtered, x='aum_millions', color='priority',
                        nbins=20, barmode='overlay',
                        color_discrete_map={'HIGH':'#C00000','MEDIUM':'#FF8C00','LOW':'#2E75B6'})
    st.plotly_chart(fig3, use_container_width=True)
 
with col_d:
    st.subheader('Risk Flag Breakdown')
    risk_counts = filtered.groupby('risk_flag').size().reset_index(name='count')
    fig4 = px.pie(risk_counts, names='risk_flag', values='count',
                  color_discrete_map={'HEALTHY':'#70AD47','MONITOR':'#FF8C00','AT RISK':'#C00000'})
    st.plotly_chart(fig4, use_container_width=True)
 
st.divider()
st.subheader('Client Details')
display_cols = ['client_id','client_name','region','product','aum_millions',
                'deal_stage','engagement_score','priority','risk_flag','days_since_contact']
st.dataframe(
    filtered[display_cols].sort_values('engagement_score', ascending=False),
    use_container_width=True,
    height=400
)
