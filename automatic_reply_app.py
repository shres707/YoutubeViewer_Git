import streamlit as st
import cohere
#import openai
#openai.api_key="sk-proj-HrISrQDuBYm5CpYCACWXT3BlbkFJKngnJMYzzcfNjwdJ8DsM"

#from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from transformers import pipeline,AutoTokenizer,AutoModelForCausalLM
#from langchain.llms import HuggingFaceLLM
cohere_api_key = "eH1W45sG4i7AiEgI776DKgExK22QsTkCfWWdp7ue"
co = cohere.Client(cohere_api_key)


def app():
  st.title("Automatic Reply")
  df_clean=st.session_state.test
  latest_comment = df_clean['Comment'].values[0]
  st.write('Latest Comment: '+latest_comment)
  prompt_template= f"""
    You are a helpful YouTube comment replying bot. Please provide a response based on the following conditions:
    - If the comment is appreciative, positive feedback, or neutral, reply 'Thanks for your feedback.'
    - If the comment is critical feedback, reply 'Sorry for the inconvenience. We will look into the issue and get back to you.'
    - If the comment is a question, try to answer the question in 25 words. If you don't know the answer, say you don't know.
    Comment: {latest_comment}
    Reply:
    """

  response = co.generate(
    model='command-xlarge-nightly',
    prompt=prompt_template,
    max_tokens=50,
    temperature=0.7,
    k=0,
    p=0.75,
    stop_sequences=["Reply:"]
  )
  reply = response.generations[0].text.strip()



  st.write("reply:"+reply)
