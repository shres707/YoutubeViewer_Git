import youtube_comment_scrapper_app
import eda_app
#import app2
import streamlit as st
PAGES = {
    "Input": youtube_comment_scrapper_app,
    "EDA"  : eda_app
    
}
st.sidebar.title('CRISP DM Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
