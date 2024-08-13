import streamlit as st
import cohere
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

cohere_api_key = "eH1W45sG4i7AiEgI776DKgExK22QsTkCfWWdp7ue"
co = cohere.Client(cohere_api_key)

# Initialize the SentenceTransformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def draw_insights(comments, query, chat_history):
    similarity_threshold = 0.1
    top_n = 5

    def embed_comments(comments):
        embeddings = model.encode(comments)
        return list(zip(comments, embeddings))

    def retrieve_relevant_comments(query, comment_embeddings, similarity_threshold=0.1, top_n=5):
        query_embedding = model.encode([query])[0].reshape(1, -1)

        similarities = []
        for comment, embedding in comment_embeddings:
            embedding_2d = embedding.reshape(1, -1)
            similarity = cosine_similarity(query_embedding, embedding_2d)[0][0]
            similarities.append((comment, similarity))

        filtered_comments = [comment for comment, similarity in similarities if similarity >= similarity_threshold]
        filtered_comments = sorted(
            filtered_comments,
            key=lambda comment: cosine_similarity(query_embedding, model.encode([comment]).reshape(1, -1))[0][0],
            reverse=True
        )

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


def app():
    st.title("YouTube Comment ChatBot")

    # Load the DataFrame and extract comments
    df_clean = st.session_state.test
    context = df_clean['Comment'].dropna().tolist()

    # Display chat history
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            st.write(f"**User**: {message['query']}")
            st.write(f"**Assistant**: {message['response']}")

    # User input for new query
    user_query = st.text_input("Enter your question:")
    if st.button("Submit") and user_query:
        # Generate response
        insights = draw_insights(comments, user_query, st.session_state.chat_history)

        # Display the response
        st.write(f"**Assistant**: {insights}")

        # Update chat history
        st.session_state.chat_history.append({"query": user_query, "response": insights})