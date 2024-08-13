import streamlit as st
import cohere
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

cohere_api_key = "eH1W45sG4i7AiEgI776DKgExK22QsTkCfWWdp7ue"
co = cohere.Client(cohere_api_key)

# Initialize the SentenceTransformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Initialize the chat history
chat_history = []


def draw_insights(comments, query, chat_history):
    similarity_threshold = 0.1
    top_n = 5

    def embed_comments(comments):
        embeddings = model.encode(comments)
        return list(zip(comments, embeddings))

    def retrieve_relevant_comments(query, comment_embeddings, similarity_threshold=0.1, top_n=5):
        query_embedding = model.encode([query])[0]

        similarities = [(comment, cosine_similarity([query_embedding], [embedding])[0][0])
                        for comment, embedding in comment_embeddings]

        filtered_comments = [comment for comment, similarity in similarities if similarity >= similarity_threshold]
        filtered_comments = sorted(filtered_comments,
                                   key=lambda x: cosine_similarity([query_embedding], [model.encode([x])[0]])[0][0],
                                   reverse=True)

        return filtered_comments[:top_n]

    def get_response_from_cohere(retrieved_comments, query, chat_history):
        context = " ".join(retrieved_comments)

        history = " ".join([f"Query: {h['query']}\nResponse: {h['response']}" for h in chat_history])

        prompt = (
            f"{history}\n\n"
            f"Comments: {context}\n\n"
            f"Question: {query}\n\n"
            "You are a chatbot that provides insights based on the given comments. "
            "Analyze the context and answer the question precisely using only the relevant information from the comments. "
            "If the comments do not provide enough information to answer the question, state: 'I don't have enough data to answer that.' "
            "Keep your response focused and concise. Reply:"
        )

        response = co.generate(
            model='command-xlarge-nightly',
            prompt=prompt,
            max_tokens=1000,
            temperature=0.7,
            k=0,
            p=0.75,
            stop_sequences=["Reply:"]
        )

        reply = response.generations[0].text.strip()
        chat_history.append({"query": query, "response": reply})
        return reply

    comment_embeddings = embed_comments(comments)
    retrieved_comments = retrieve_relevant_comments(query, comment_embeddings, similarity_threshold, top_n)
    return get_response_from_cohere(retrieved_comments, query, chat_history)


def chat_session(comments):
    global chat_history
    while True:
        query = st.text_input("Enter your question (or type 'exit' to end): ")
        print(query)
        if query.lower() == 'exit':
            break
        insights = draw_insights(comments, query, chat_history)
        st.write(f"Response: {insights}")


def app():
    st.title("YouTube Comment ChatBot")
    df_clean = st.session_state.test
    context = " ".join(df_clean['Comment'].dropna().tolist())
    chat_session(context)

    '''user_question = st.text_input("Ask a Question")

    if st.button("Clear Chat History"):
        st.session_state["messages"] = []

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
        st.session_state.messages.append({"role": "assistant", "content": ai_response})'''
