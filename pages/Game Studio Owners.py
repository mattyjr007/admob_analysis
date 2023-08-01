import streamlit as st
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from Dashboard import df, studio_owners


st.set_page_config(page_title="Game Studio Owners", page_icon="🎮",layout="wide")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 1rem;
                   
                }
        </style>
        """, unsafe_allow_html=True) 




sidebar = st.sidebar
dash_1 = st.container()
dash_2 = st.container()
dash_3 = st.container()
dash_4 = st.container()




with sidebar:
    stuido_owners_cnt = df['Which of these best describe you?'].value_counts()

    st.header("African Game Studio Owners Analysis")
    st.write("")
    fig = go.Figure(data=[go.Pie(labels=stuido_owners_cnt.index,
                                    values=stuido_owners_cnt.values,
                                    #hole=.3, 
                                    #pull=[0, 0.2],
                                   )])
    
    fig.update_layout(showlegend=False,
                             height=300,
                             margin={'l': 20, 'r': 60, 't': 0, 'b': 0})
    fig.update_traces(textposition='inside', textinfo='label+percent')
    
    st.plotly_chart(fig,use_container_width=True)

    st.write("percentage of Game Studio Onwers.")



with dash_1:
    st.markdown("<h1 style='text-align: center;'>African Game studio owners analysis</h1>", unsafe_allow_html=True)
    st.write("")
  


with dash_2:
    
    disp1, disp2 = st.columns(2)

    with disp1:
        pub = studio_owners['How long have you been operating?'].value_counts()

        fig_reg = go.Figure(data=[go.Bar(x=pub.index, y=pub.values,text=pub.values,
                        textposition='auto',
                       )])
        fig_reg.update_layout(showlegend=False,
                             height=300,
                             margin={'l': 20, 'r': 0, 't': 0, 'b': 5},
                             )
        
        
        
        st.plotly_chart(fig_reg,use_container_width=True)
        st.write("Number of year in operation for studio owners.")


    with disp2:
        reg = df['How many employees do you have?'].value_counts()
        fig_reg = go.Figure(data=[go.Bar(x=reg.index, y=reg.values,text=reg.values,
                        textposition='auto',
                       )])
        fig_reg.update_layout(showlegend=False,
                             height=300,
                             margin={'l': 20, 'r': 0, 't': 0, 'b': 5},
                             )
        
        
        
        st.plotly_chart(fig_reg,use_container_width=True)
        st.write("Number of Employees range for studio owners.")




with dash_3:
    
    disp1, disp2 = st.columns(2)

    with disp1:
        pub = studio_owners['To date, how many games do you have published?'].value_counts()

        fig_reg = go.Figure(data=[go.Bar(x=pub.index, y=pub.values,text=pub.values,
                        textposition='auto',
                       )])
        
        fig_reg.update_layout(showlegend=False,
                             height=300,
                             margin={'l': 20, 'r': 0, 't': 0, 'b': 5},
                             )
        
        
        st.plotly_chart(fig_reg,use_container_width=True)
        st.write("Number of games published.")


    with disp2:
        rev = df['What was your 2022 revenue?'].value_counts()
        fig_rev = go.Figure(data=[go.Bar(x=rev.index, y=rev.values,text=rev.values,
                        textposition='auto',
                       )])
        fig_rev.update_layout(showlegend=False,
                             height=300,
                             margin={'l': 20, 'r': 0, 't': 0, 'b': 5},
                             )
        
        
        
        st.plotly_chart(fig_rev,use_container_width=True)
        st.write("2022 Revenue range for studio owners.")

   