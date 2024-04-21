import streamlit as st
import pandas as pd
import plotly.express as px
import regex as re

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('/home/elad/Downloads/analyst_assignment_soccer_comparison_BI.csv') # change the path
    df['time_min'] = df['time'].map(lambda x: int(re.search('[0-9]+', x).group()))
    return df

df = load_data()

tabs = ["Odds Over Time", "Score and Corners Analysis", "High-risk Areas"]
selected_tab = st.sidebar.radio("Select Tab", tabs)

if selected_tab == "Odds Over Time":
    number = st.number_input('Insert an event_id')
    st.write(df[df['event_id'] == number])

    markets = df['compared market name '].unique()
    selection = df['compared selection name  '].unique()

    market_button = st.sidebar.checkbox('Include Market in graph')
    selected_market = st.sidebar.selectbox("Select Market", markets)
    selection_button = st.sidebar.checkbox('Include Selection in graph')
    selected_selection = st.sidebar.selectbox("Select Selection", selection)

    if market_button and not selection_button: # only market
        filtered_df = df[(df["compared market name "] == selected_market)]
    elif not market_button and selection_button:
        filtered_df = df[(df["compared selection name  "] == selected_selection)]
    elif market_button and selection_button:
        filtered_df = df[(df["compared market name "] == selected_market) & (df["compared selection name  "] == selected_selection)]

    if (not market_button and not selection_button) or len(filtered_df)==0:
        st.write('None Avilable Data')
    else:
        fig = px.scatter(filtered_df, x="time_min", y=['ALFABET_final_odds', 'compared_model_odds'],
                    labels={"variable": "Odds Type", "value": "Odds", "Time": "Time",'compared_model_odds':'compared_model_odds', 'event_id':'event_id'},
                    hover_data={'event_id':True},
                    height=600, width=900)
        st.plotly_chart(fig)


elif selected_tab == "Score and Corners Analysis":
    number = st.number_input('Insert an event_id')
    st.write(df[df['event_id'] == number])

    score = st.sidebar.checkbox('Include match score in graph')
    match_score_range_home = st.sidebar.slider("Match Score Home", min_value=0, max_value=10, step=1)
    match_score_range_away = st.sidebar.slider("Match Score Away", min_value=0, max_value=10, step=1)
    M = f'Score(home={match_score_range_home}, away={match_score_range_away})'
    st.sidebar.write("Match ", M)
    corner = st.sidebar.checkbox('Include corner score in graph')
    corener_score_range_home = st.sidebar.slider("Coreners Score Home", min_value=0, max_value=10, step=1)
    corener_score_range_away = st.sidebar.slider("Coreners Score Away", min_value=0, max_value=10, step=1)
    C = f"Score(home={corener_score_range_home}, away={corener_score_range_away})"
    st.sidebar.write("Corner", C)

    if not score and corner: # only with corner
        filtered_df = df[(df['Model Input  - current corners score'] == C)]
    elif score and not corner: # only with score
        filtered_df = df[(df['Model Input  - current_match_score'] == M)]
    elif score and corner: #BOTH
        filtered_df = df[(df['Model Input  - current corners score'] == C) & (df['Model Input  - current_match_score'] == M)]

    if (not score and not corner) or len(filtered_df)==0:
        st.write('None Avilable Data')
    else:
        fig = px.scatter(filtered_df, x="time_min", y=['ALFABET_final_odds', 'compared_model_odds'],
                    labels={"variable": "Odds Type", "value": "Odds", "Time": "Time",'compared_model_odds':'compared_model_odds', 'event_id':'event_id'},
                    hover_data={'event_id':True, 'compared_model_odds':False},
                    height=600, width=900)
        st.plotly_chart(fig)
