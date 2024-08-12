import streamlit as st

def app():
  st.title("YouTube Transcript Summariser")
  transscript_data = st.session_state.transcript_data

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