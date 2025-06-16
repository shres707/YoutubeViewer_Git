import streamlit as st
import cohere
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Cohere client
cohere_api_key = "eH1W45sG4i7AiEgI776DKgExK22QsTkCfWWdp7ue"
co = cohere.Client(cohere_api_key)

# Initialize sentence transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')



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
    st.write("**Comments being analyzed:**")
    st.write(context)

    context = context.strip()

    history = " ".join([f"Query: {h['query']}\nResponse: {h['response']}" for h in chat_history]).strip()

    st.write("**Chat History:**")
    st.write(history)

    prompt = (
        f"{history}\n\n"
        "You are a chatbot that provides insights based on the given comments. \n\n"
        f"Comments: {context}\n\n"
        "Keep your response focused and concise. And if the comments don't have the relevant data, say 'I can't help you' \n\n"
        f"Question: {query}\n\n"
        "Reply:"
    )

    response = co.chat(
        model='command-xlarge-nightly',
        message=prompt,
        max_tokens=2000,
        temperature=0.7
        
    )

    reply = response.generations[0].text.strip()
    chat_history.append({"query": query, "response": reply})
    return reply


def draw_insights(comments, query, chat_history):
    similarity_threshold = 0.1
    top_n = 10

    comment_embeddings = embed_comments(comments)
    retrieved_comments = retrieve_relevant_comments(query, comment_embeddings, similarity_threshold, top_n)
    return get_response_from_cohere(retrieved_comments, query, chat_history)


def app():
    st.title("YouTube Comment ChatBot")
    df_clean = st.session_state.test
    context = df_clean['Comment'].dropna().tolist()


    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    elif st.session_state.get('clear_history', False):
        st.session_state['chat_history'] = []
        st.session_state['clear_history'] = False

    chat_history = st.session_state['chat_history']
    user_question = st.text_input("Ask a Question")

    if st.button("Clear Chat History"):
        st.session_state['chat_history'] = []
        st.session_state['clear_history'] = True
        chat_history = []
        st.write("Chat history cleared!")

    if user_question:
        st.session_state['chat_history'].append({"query": user_question, "response": ""})
        st.write(f"**User**: {user_question}")

        # Get response from the Cohere model
        with st.spinner("Loading..."):
            ai_response = draw_insights(context, user_question, chat_history)

    for message in st.session_state['chat_history']:
        st.write(f"**User**: {message['query']}")
        st.write(f"**Assistant**: {message['response']}")

