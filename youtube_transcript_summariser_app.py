import streamlit as st
import cohere
from youtube_transcript_api import YouTubeTranscriptApi
cohere_api_key = "eH1W45sG4i7AiEgI776DKgExK22QsTkCfWWdp7ue"
co = cohere.Client(cohere_api_key)

def get_id(url):
    u_pars = urlparse(url)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]

def get_transcript(video_id):
   transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
   transcript_data = [t['text'] for t in transcript_list]
   return transcript_data

def app():
  st.title("YouTube Transcript Summariser")
  if transcript_data not in st.session_state:
      st.session_state.url = url
      ID = get_id(url)
      # Extracting YouTube transcript
      transcript_data = get_transcript(ID)
      st.session_state.transcript_data = transcript_data

  transcript_data = st.session_state.transcript_data
  text = " ".join(transcript_data)

  response = co.summarize(
      text=text,
      length='auto',
      format='auto',
      model='summarize-xlarge',
      additional_command='',
      temperature=0.3,
  )

  # Get the summary from the response
  summary = response.summary
  st.write(summary)