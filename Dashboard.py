import streamlit as st
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


st.set_page_config(page_title="African Game Survey", page_icon="😊",layout="wide")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 1rem;
                   
                }
        </style>
        """, unsafe_allow_html=True) 


df = pd.read_excel('African Games Industry Survey.xlsx')
df['developed a game'] = df['Have you developed a game?'].str.lower().str.split(',').str[0]

def extract_city_country(col):
    location_info = col.split(',')
    country = location_info[-1].strip()
    city = location_info[0].strip() if len(location_info) > 1 else 'N/A'
    return pd.Series([city, country], index=['city', 'country'])

# Apply the function to the DataFrame
df[['city', 'country']] = df['Where are you located?'].apply(extract_city_country)

df_developed_game = df[['country','developed a game']].groupby('developed a game').count()

non_studio_owners = df[df['Which of these best describe you?'].str.lower().str.strip() != 'game studio']
studio_owners = df[df['Which of these best describe you?'].str.lower().str.strip() == 'game studio']


sidebar = st.sidebar
dash_1 = st.container()
dash_2 = st.container()
dash_3 = st.container()
dash_4 = st.container()
dash_5 = st.container()
dash_6 = st.container()




with sidebar:
    st.header("Analysis")
    st.write("")
    fig_dev = go.Figure(data=[go.Pie(labels=df_developed_game.index,
                                    values=df_developed_game['country'],
                                    hole=.3, 
                                    pull=[0, 0.2],
                                   )])
    
    fig_dev.update_layout(showlegend=False,
                             height=300,
                             margin={'l': 20, 'r': 60, 't': 0, 'b': 0})
    fig_dev.update_traces(textposition='inside', textinfo='label+percent')
    
    st.plotly_chart(fig_dev,use_container_width=True)

    st.write("percentage of those who developed a game.")
    
    
    
with dash_1:
    st.markdown("<h1 style='text-align: center;'>African Games Industry Survey Analysis</h1>", unsafe_allow_html=True)
    st.write("")

with dash_2:
    disp1, disp2 = st.columns(2)

    with disp1:
        reg = df['What region are you based?'].value_counts()
        fig_reg = go.Figure(data=[go.Bar(x=reg.index, y=reg.values,text=reg.values,
                        textposition='auto',
                        marker=dict(
        color=reg.values,  # Use the values for coloring
        colorscale='Blues',  # Specify the colorscale name
       # Add a colorbar title
    ))])
        fig_reg.update_layout(showlegend=False,
                             height=300,
                             margin={'l': 20, 'r': 0, 't': 0, 'b': 5},
                             )
        
        
        
        st.plotly_chart(fig_reg,use_container_width=True)
        st.write("The Region where the survey participants are based in.")


    with disp2:
        country = df['country'].value_counts()
        fig_map = go.Figure(go.Choropleth(
        geojson='https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/africa.geojson',
        locations=country.index,
        z=country.values,
        locationmode='country names',
        colorscale='Reds',
        #colorbar=dict(title='Value'),
        hovertext=country.index + ': ' + country.values.astype(str),
        hoverinfo='text'
        ))

        #fig.update_geos(projection_type='mercator')
        fig_map.update_layout(geo=dict(
                bgcolor='rgba(0,0,0,0)',
                scope='africa',
                center=dict(lon=17, lat=3),
                projection_scale=1.1),
                        showlegend=False,
                        height=300,
                        margin={'l': 0, 'r': 0, 't': 0, 'b': 5})

        st.plotly_chart(fig_map,use_container_width=True)
        st.write("The Countries where the survey participants are based in.")




with dash_3:

    disp1, disp2 = st.columns(2)

    with disp1:
        platform = df['What platforms do you build for?'].str.split(",").values

        flattened_platform = [pl.strip() for sublist in platform for pl in sublist]
        # Count occurrences of each value
        counted_platform = Counter(flattened_platform)

        fig_plat = go.Figure(data=[go.Bar(x=list(counted_platform.keys())[:3], y=list(counted_platform.values())[:3],text=list(counted_platform.values())[:3],
                            textposition='auto',
                            marker=dict(
                                    color=list(counted_platform.values())[:3],  # Use the values for coloring
                                    colorscale='Reds',  # Specify the colorscale name
                                    #colorbar=dict(title='Count')
                                      )
                           
        )])
        fig_plat.update_layout(showlegend=False,
                                height=350,
                                margin={'l': 20, 'r': 0, 't': 30, 'b': 0})
        
        st.plotly_chart(fig_plat, use_container_width=True)
        st.write("The plot above shows the top 3 platforms people develop a game for.")




    with disp2:
        engine = df['What is the primary engine you use in developing games?'].value_counts()
        others_values = engine[engine < 3].index
        # Replace those values with 'Others'
        engine = df.replace(others_values, 'Others')
        engine = engine['What is the primary engine you use in developing games?'].value_counts()


        fig_eng = go.Figure(data=[go.Pie(labels=engine.index,
                                    values=engine.values,
                                    hole=.3, 
                                    pull=[0, 0.2,0.1,0,0],
                                   )])
        
        fig_eng.update_layout(showlegend=False,
                                height=350,
                                margin={'l': 0, 'r': 0, 't': 30, 'b': 0})
        fig_eng.update_traces(textposition='inside', textinfo='label+percent')
        
        st.plotly_chart(fig_eng,use_container_width=True)

        st.write("Most used game engine.")



with dash_4:
    st.write("")

    disp1, disp2 = st.columns(2)

    with disp2:
        gamecat = df['What category of games do you mostly create?'].str.split(",").values
        flattened_gamecat = [ct.strip() for sublist in gamecat for ct in sublist]
        # Count occurrences of each value
        counted_gamecat = Counter(flattened_gamecat)

        fig_game_cat = go.Figure(data=[go.Bar(x=list(counted_gamecat.keys())[:5], y=list(counted_gamecat.values())[:5],text=list(counted_gamecat.values())[:5],
                            textposition='auto',
                            marker=dict(
                                    color=list(counted_gamecat.values())[:5],  # Use the values for coloring
                                    colorscale='Reds',  # Specify the colorscale name
                                    #colorbar=dict(title='Count')
                                      )
                           
        )])
        fig_game_cat.update_layout(showlegend=False,
                                height=450,
                                margin={'l': 0, 'r': 0, 't': 60, 'b': 0})
        
        st.plotly_chart(fig_game_cat, use_container_width=True)
        st.write("The plot above shows the top 5 Game people develop a game for.")



    with disp1:

        tab1,tab2 = st.tabs(["None game studio owners gender",'None game studio owners age range'])


        with tab1:

            gender  = non_studio_owners['What\'s your gender?'].value_counts()

            fig_gender = go.Figure(data=[go.Pie(labels=gender.index,
                                    values=gender.values,
                                    #hole=.3, 
                                    pull=[0, 0,0.2],
                                   )])
        
            fig_gender.update_layout(showlegend=False,
                                    height=400,
                                    margin={'l': 0, 'r': 0, 't': 60, 'b': 0})
            fig_gender.update_traces(textposition='inside', textinfo='label+percent')
            
            st.plotly_chart(fig_gender,use_container_width=True)

            st.write("For none game studio owner the pie chart shows the ratio of their gender.")

        
        with tab2:

            age_range_counts = non_studio_owners['What\'s your age group?'].value_counts()

            # Create the bar chart
            fig_age = go.Figure(data=[go.Bar(x=age_range_counts.index, y=age_range_counts.values,text=age_range_counts.values)])

            # Update the layout for better visibility
            fig_age.update_layout(showlegend=False,
                height=400,
                margin=dict(l=0, r=0, t=10, b=0),
            )

            st.plotly_chart(fig_age,use_container_width=True)

            st.write("For none game studio owner the bar chart shows the distribution of their age range.")



with dash_5:
    

    # questions dataframe
    Q_df = df.copy()
    # get all countries
    all_countri= df.country.to_list()
    all_countri.append("All")
    all_countri = tuple(set(all_countri))
    all_countri = sorted(all_countri)

    factors = ("Power supply","High speed internet","Affordable internet","Training opportunities","Community events","Co-working space","Industry associations","Mobile network operators (like MTN or Safaricom)","Alternative payment methods (like mobile money)","Government support")
     

    st.write("")
    st.write("")
    st.markdown("<h2 style='text-align: center;'>Analysis on game development factors by countries</h2>", unsafe_allow_html=True)
    st.write("")
    #st.header("Analysis on game development factors by countries")
    st.markdown("<p style='text-align: center;'>this analysis provide insights on some development factors in some countries and thier current states.</p>", unsafe_allow_html=True)
    #st.write("this analysis provide insights on some development factors in some countries and thier current states.")

    
    d1,d2,d3 = st.columns(3)

    with d2:
        country_option = st.selectbox("Please select a country.",all_countri)

    if country_option == "All":
        current_df = Q_df
    else:
        current_df = Q_df[Q_df['country'] == country_option]

    
    st.write("")
    # factor selecting 
    e1,e2,e3 = st.columns(3)

    with e2:
         factor_slected = st.selectbox("Please select a factor to find out the responses based on importance and current state in the country selected.",
                                       factors)
         st.write("")
         st.write("")


    disp1, disp2 = st.columns(2)

    with disp1:


        importance = current_df[f"How important are the following to the development of the games industry in your country? [{factor_slected}]"].value_counts()
        
        fig_importance = go.Figure(data=[go.Bar(x=importance.index, y=importance.values,text=importance.values,
                        textposition='auto',
                        marker=dict(
        color=importance.values,  # Use the values for coloring
        colorscale='Blues',  # Specify the colorscale name
       # Add a colorbar title
    ))])
        fig_importance.update_layout(showlegend=False,
                             height=300,
                             margin={'l': 20, 'r': 0, 't': 0, 'b': 5},
                             )
        
        
        
        st.plotly_chart(fig_importance,use_container_width=True)
        st.write(f"The Importance of {factor_slected} in {country_option}.")


    
    with disp2:


        current_countri_state = current_df[f"How would you rate the current state of these infrastructure in your country? [{factor_slected}]"].value_counts()
        
        fig_current_countri_state = go.Figure(data=[go.Bar(x=current_countri_state.index, y=current_countri_state.values,text=current_countri_state.values,
                        textposition='auto',
                        marker=dict(
        color=current_countri_state.values,  # Use the values for coloring
        colorscale='Blues',  # Specify the colorscale name
       # Add a colorbar title
    ))])
        fig_current_countri_state.update_layout(showlegend=False,
                             height=300,
                             margin={'l': 20, 'r': 0, 't': 0, 'b': 5},
                             )
        
        
        
        st.plotly_chart(fig_current_countri_state,use_container_width=True)
        st.write(f"The Current state of {factor_slected} in {country_option}.")



with dash_6:

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("The frequently occured words for the survey question `What type of support does the industry need to succeed?`")
    st.write("")
    st.write("")
    text = " ".join(txt for txt in df['What type of support does the industry need to succeed?'])
    
    stopwords = set(STOPWORDS)

    wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(text)
    
 
    # plot the WordCloud image                      
    plt.figure(figsize = (4, 4), facecolor = None,dpi=200)
    plt.imshow(wordcloud)
    plt.axis("off")
    #plt.tight_layout(pad = 0)
    # Plot the word cloud image with Streamlit
    st.pyplot(plt,use_container_width=False)
        
                




            
        







