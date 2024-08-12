import streamlit as st
import cohere
cohere_api_key = "eH1W45sG4i7AiEgI776DKgExK22QsTkCfWWdp7ue"
co = cohere.Client(cohere_api_key)

def app():
  st.title("YouTube Transcript Summariser")
  transcript_data = st.session_state.transcript_data

  response = co.summarize(
      text=transcript_data,
      length='auto',
      format='auto',
      model='summarize-xlarge',
      additional_command='',
      temperature=0.3,
  )

  # Get the summary from the response
  summary = response.summary
  st.write(summary)