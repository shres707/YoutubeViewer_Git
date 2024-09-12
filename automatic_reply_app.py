import streamlit as st
import cohere
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from youtube_transcript_api import YouTubeTranscriptApi

cohere_api_key = "eH1W45sG4i7AiEgI776DKgExK22QsTkCfWWdp7ue"
co = cohere.Client(cohere_api_key)

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


def get_transcript(video_id):
   transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
   transcript_data = [t['text'] for t in transcript_list]
   return transcript_data



def embed_text(text):
    return model.encode([text])[0]


def chunk_text(text, chunk_size=50):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])


def generate_reply(comment, video_summary):
    summary_chunks = list(chunk_text(video_summary, chunk_size=50))

    comment_embedding = embed_text(comment)

    relevant_chunks = []
    for chunk in summary_chunks:
        chunk_embedding = embed_text(chunk)
        similarity = cosine_similarity([comment_embedding], [chunk_embedding])[0][0]
        if similarity > 0.1:
            relevant_chunks.append(chunk)

    if not relevant_chunks:
        #aggregated_context = "Try answering the question from your own database and if you can not answer then reply, 'sorry I can not help you with it'"
        return "Sorry I can't help you."  # Fallback if no relevant chunks are found

        # Aggregate all relevant chunks into one context
    aggregated_context = " ".join(relevant_chunks)

    # Generate a single reply using the aggregated context
    prompt_template = f"""
    You are a helpful YouTube comment replying bot. The video is about: "{aggregated_context}"

    Please provide a response based on the following conditions:
    - If the comment is positive or neutral, reply 'Thanks for your feedback.'
    - If the comment is critical, reply 'We will consider your feedback, thank you!'
    - If the comment is a question, answer it in 25 words or less using the video summary as context. If you don't know the answer, say 'Sorry I can't help you'.

    Comment: {comment}
    Reply:
    """

    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt_template,
        max_tokens=1000,
        temperature=0.7,
        k=0,
        p=0.75,
        stop_sequences=["Reply:"]
    )
    reply = response.generations[0].text.strip()

    return reply


def app():
    st.title("Automatic Reply")
    df_clean = st.session_state.test
    latest_comment = df_clean['Comment'].values[0]
    # Use HTML and CSS to style the boxes
    st.markdown("""
             <style>
             .box {
                 border: 2px solid #d0d0d0;
                 border-radius: 5px;
                 padding: 10px;
                 margin: 10px 0;
                 font-size: 14px;
                 font-weight: bold;
             }
             .label {
                font-size: 30px;
                font-weight: bold;
                text-decoration: underline;
                margin-top: 20px;
            }
             </style>
             """, unsafe_allow_html=True)

    st.markdown('<p class="label">Latest Comment:</p>', unsafe_allow_html=True)
    # latest_comment_display = st.text_area("", latest_comment, height=150, key='latest_comment_display', disabled=True)
    st.write(f"<div class='box'>{latest_comment}</div>", unsafe_allow_html=True)

    if st.button('Generate Reply', key='generate_reply_button'):
        # comment = latest_comment_display
        comment = latest_comment
        transcript_data=[]
        if transcript_data not in st.session_state:
            ID=st.session_state.ID
            # Extracting YouTube transcript
            transcript_data = get_transcript(ID)
            st.session_state.transcript_data = transcript_data
        transcript_data = st.session_state.transcript_data
        video_summary = " ".join(transcript_data)
       #comment="If I play a cross block defense shot. Should I rush to cross court too?"
        reply = generate_reply(comment, video_summary)
        # st.header("Reply:")
        st.markdown('<p class="label">Reply:</p>', unsafe_allow_html=True)
        # st.text_area("", reply if reply else "No reply generated.", height=150, disabled=True)
        st.write(f"<div class='box'>{reply if reply else 'No reply generated.'}</div>", unsafe_allow_html=True)

