import streamlit as st
#import openai
#openai.api_key="sk-proj-HrISrQDuBYm5CpYCACWXT3BlbkFJKngnJMYzzcfNjwdJ8DsM"

#from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from transformers import pipeline,AutoTokenizer,AutoModelForCausalLM
#from langchain.llms import HuggingFaceLLM


def app():
  st.title("Automatic Reply")
  df_clean=st.session_state.test
  latest_comment = df_clean['Comment'].values[0]
  st.write('Latest Comment: '+latest_comment)
  prompt_template= f"""
  You are a helpful YouTube comment replying bot. The following comment will be provided to you.
    Reply based on the following conditions:
    - If the comment is appreciative, positive feedback, or neutral, reply 'Thanks for your feedback.'
    - If the comment is critical feedback, reply 'Sorry for the inconvenience. We will look into the issue and get back to you.'
    - If the comment is a question, try to answer the question in 25 words. If you don't know the answer, say you don't know.
    Comment: {latest_comment}
  """

  reply_model_name="gpt2"
  #llm = OpenAI(temperature=0,openai_api_key=openai.api_key)
  #generator=pipeline('text-generation',model=model_name)
  #llm=HuggingFaceLLM(generator)
  #llm_chain = LLMChain(llm=llm,prompt=PromptTemplate.from_template(prompt_template))
  #st.write("Reply:"+llm_chain(latest_comment))
  reply_tokenizer = AutoTokenizer.from_pretrained(reply_model_name)
  reply_model = AutoModelForCausalLM.from_pretrained(reply_model_name)
  #reply_tokenizer=AutoTokenizer.from_pretrained(reply_model_name)
  #reply_tokenizer.add_special_tokens({'pad_token':'[PAD]'})
  #reply_model = TFAutoModelForCausalLM.from_pretrained(reply_model_name)
  #reply_model.resize_token_embeddings(len(reply_tokenizer))
  if reply_tokenizer.pad_token is None:
    reply_tokenizer.pad_token = reply_tokenizer.eos_token

  prompt=prompt_template.format(comment=latest_comment)
  inputs = reply_tokenizer(prompt, return_tensors="pt", truncation=True, padding=True, max_length=512)

  # Generate the output
  outputs = reply_model.generate(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"],
                                 max_new_tokens=100, temperature=0.7,    # Control creativity
        top_p=0.9,          # Control the diversity
        top_k=50    )
  reply = reply_tokenizer.decode(outputs[0], skip_special_tokens=True)
  reply = reply[len(prompt):].strip()



  st.write("reply:"+reply)
