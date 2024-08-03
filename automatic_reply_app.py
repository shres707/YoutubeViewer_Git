import streamlit as st
#import openai
#openai.api_key="sk-proj-HrISrQDuBYm5CpYCACWXT3BlbkFJKngnJMYzzcfNjwdJ8DsM"

#from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from transformers import pipeline
#from langchain.llms import HuggingFaceLLM


def app():
  st.title("Automatic Reply")
  df_clean=st.session_state.test
  latest_comment = df_clean['Comment'].values[0]
  st.write('Latest Comment: '+latest_comment)
  prompt_template= """
  You are a helpful youtube comment replying bot. The following {comment} will be provided to you.
  Use following conditions to reply.
  If the comment is appreciative,positive feedback or neutral then reply 'Thanks for your feedback.'
  If the comment is critical feedback then reply 'Sorry for the inconvenience.We will look into the issue and getback'
  If the comment is question.Then you can try to answer the question in 25 words. If you don't know the ,then say you don't know.
  """

  reply_model_name="distilgpt2"
  #llm = OpenAI(temperature=0,openai_api_key=openai.api_key)
  #generator=pipeline('text-generation',model=model_name)
  #llm=HuggingFaceLLM(generator)
  #llm_chain = LLMChain(llm=llm,prompt=PromptTemplate.from_template(prompt_template))
  #st.write("Reply:"+llm_chain(latest_comment))
  reply_model=pipeline("text-generation",model=reply_model_name)
  response = reply_model(latest_comment)
  st.write("Reply: " + response)

