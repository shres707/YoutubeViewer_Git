import streamlit as st
import cohere
cohere_api_key = "eH1W45sG4i7AiEgI776DKgExK22QsTkCfWWdp7ue"
co = cohere.Client(cohere_api_key)

def app():
  st.title("YouTube Comment ChatBot")
  df_clean = st.session_state.test
  context = " ".join(df_clean['Comment'].dropna().tolist())

  user_question = st.text_input("Ask a Question")

  if "messages" not in st.session_state:
      st.session_state["messages"] = [{"role": "assistant", "content": "Hello there, how can I help you?"}]

      # Display previous messages
  for message in st.session_state.messages:
      st.write(f"**{message['role'].capitalize()}**: {message['content']}")

  if user_question:
      # Add user's question to the chat history
      st.session_state.messages.append({"role": "user", "content": user_question})
      st.write(f"**User**: {user_question}")

      # Get response from the Cohere model
      with st.spinner("Loading..."):
          ai_response = get_response_from_cohere(context, user_question)

      # Add the AI's response to the chat history
      st.write(f"**Assistant**: {ai_response}")
      st.session_state.messages.append({"role": "assistant", "content": ai_response})
