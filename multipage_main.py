import youtube_comment_scrapper_app
import eda_app
import data_preprocess_eda_app
import sentiment_app
#import automatic_reply_app
import youtube_transcript_summariser_app
import youtube_comment_chatbot_app


import streamlit as st
PAGES = {
    "Input": youtube_comment_scrapper_app,
    "Data Preprocess": data_preprocess_eda_app,
    "EDA"  : eda_app,
    "Sentiment Analysis": sentiment_app,
    #"Automatic Reply": automatic_reply_app,
    "Transcript Summariser": youtube_transcript_summariser_app,
    "Comment ChatBot": youtube_comment_chatbot_app

}
st.sidebar.title('CRISP DM Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
