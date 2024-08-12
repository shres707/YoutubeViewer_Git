import streamlit as st
import cohere
cohere_api_key = "eH1W45sG4i7AiEgI776DKgExK22QsTkCfWWdp7ue"
co = cohere.Client(cohere_api_key)

def app():
  st.title("YouTube Comment ChatBot")
  df_clean = st.session_state.test
  context = " ".join(df_clean['Comment'].dropna().tolist())

  user_question = st.text_input("Ask a Question")

  if "messages" not in st.session_state.keys():
      st.session_state["messages"] = [{"role": "assistant", "content": "Hello there, how can I help you?"}]

  if "messages" in st.session_state.keys():
      for message in st.session_state.messages:
          with st.chat_message(message["role"]):
              st.write(message["content"])

  if user_question is not None:
      st.session_state.messages.append({"role": "user", "content": user_question})

      with st.chat_message("user"):
          st.write(user_question)

      if st.session_state.messages[-1]["role"] != "assistant":
          with st.chat_message("assistant"):
              with st.spinner("Loading"):
                  ai_response = get_response_from_cohere(context, user_question)
                  st.write(ai_response)

          new_ai_message = {"role": "assistant", "content": ai_response}
          st.session_state.messages.append(new_ai_message)
