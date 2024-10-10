import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables and configure API key for Generative AI
genai.configure(api_key=os.getenv('GOOGLE_GENAI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_pdf_text(pdf_docs):
    """Extract text from a list of uploaded PDF documents."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def fetch_video_transcript(youtube_url):
    """Extract transcript from a YouTube video using its URL."""
    video_id = youtube_url.split("v=")[-1].split("&")[0]  # Extract video ID
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = " ".join([t['text'] for t in transcript])
    return transcript_text

def split_text_into_chunks(text):
    """Split text into smaller chunks for processing."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def create_vector_store(text_chunks):
    """Create a vector store from text chunks using Google Generative AI embeddings."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def build_qa_chain():
    """Build a question-answering chain using a conversational model."""
    prompt_template = """
    Answer the question as accurately as possible using the provided context.
    If the answer is not in the context, respond with "Answer is not available in the context."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    chain = load_qa_chain(model, chain_type="stuff", prompt=PromptTemplate(template=prompt_template, input_variables=["context", "question"]))
    return chain

def validate_transcript_facts(transcript, pdf_chunks):
    """Validate facts from a video transcript against the content of uploaded PDFs."""
    chain = build_qa_chain()
    validation_results = []

    for sentence in transcript.split('.'):
        if sentence.strip():  # Skip empty sentences
            response = chain({"input_documents": pdf_chunks, "question": sentence}, return_only_outputs=True)
            validation_results.append((sentence, response["output_text"]))

    return validation_results

def main():
    st.set_page_config("YouTube Fact Validator", layout="centered")
    st.title("Validate YouTube Video Facts Against PDF Content 📄🔍")

    # User inputs: YouTube video URL and PDF files
    youtube_url = st.text_input("Enter YouTube Video URL")
    pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True)

    if st.button("Validate"):
        if youtube_url and pdf_docs:
            with st.spinner("Processing..."):
                # Step 1: Extract transcript from YouTube
                transcript = fetch_video_transcript(youtube_url)

                # Step 2: Extract text from uploaded PDFs
                pdf_text = extract_pdf_text(pdf_docs)
                pdf_chunks = split_text_into_chunks(pdf_text)

                # Step 3: Validate facts from the transcript against the PDF content
                validation_results = validate_transcript_facts(transcript, pdf_chunks)

                st.success("Validation Complete!")

                # Display validation results
                for original_fact, validation_response in validation_results:
                    st.write(f"**Fact:** {original_fact.strip()}")
                    st.write(f"**Validation Response:** {validation_response.strip()}")
                    st.write("---")
        else:
            st.warning("Please provide both a YouTube URL and at least one PDF document.")

if __name__ == "__main__":
    main()
