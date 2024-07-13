import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report


def app():
  st.title("EDA")
  df=st.session_state.test
  st.header('**Input DataFrame**')
  st.write(df)
  pr = ProfileReport(df, explorative=True)
  st.header('**Pandas Profiling Report**')
  st_profile_report(pr)
  
  
  
  #st.dataframe(df)
  
  
  