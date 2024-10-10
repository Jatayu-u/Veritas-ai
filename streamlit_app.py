import streamlit as st
import requests
import pandas as pd
import time
from streamlit_lottie import st_lottie

# Lottie animation function
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Google-themed Lottie animation
lottie_google_fact_check = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_t9gkkhz4.json")

# Page configuration
st.set_page_config(page_title="Veritas AI Fact Checker", page_icon="🔍", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .reportview-container {
        background: #FFFFFF; /* Clean white background */
        color: #333333; /* Dark text for contrast */
    }
    .stTextInput > div > input, .stTextArea > div > textarea {
        border: 1px solid #B0BEC5; /* Light grey border */
        padding: 10px;
        border-radius: 5px; /* Slightly rounded corners */
        transition: border-color 0.3s;
        width: 100%; /* Full width */
        margin-bottom: 20px; /* Add spacing between inputs */
    }
    .stTextInput > div > input:focus, .stTextArea > div > textarea:focus {
        border-color: #ADD8E6; /* Highlight border on focus */
    }
    .stFileUploader > div > div {
        width: 100% !important; /* Full width for file uploader */
        margin-bottom: 20px; /* Add spacing */
    }
    .stButton > button {
        background-color: #ADD8E6; /* Soft blue */
        color: black;
        border-radius: 5px;
        padding: 12px 24px;
        font-size: 16px;
        transition: background-color 0.3s, transform 0.3s;
        border: none; /* Remove default border */
        cursor: pointer; /* Pointer cursor for buttons */
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #357ae8; /* Darker blue on hover */
        transform: translateY(-2px); /* Slightly lift the button */
        color: black;
    }
    .header-text {
        color: #ADD8E6;
        font-size: 38px;
        text-align: center; /* Centered header */
        margin-bottom: 20px; /* Add space between title and content */
    }
    .subheader-text {
        color: white;
        font-size: 18px;
        text-align: center; /* Centered subheader */
        margin-bottom: 10px; /* Add space between subheader and content */
        margin-top: 20px; 
    }
    .footer-text {
        color: #FBBC05;
        margin-top: 40px;
        text-align: center; /* Centered footer */
    }
    .fade-in {
        animation: fadeIn 1s; /* Fade-in effect */
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)


# Custom CSS for styling
st.markdown("""
    <style>
    .reportview-container {
        background: #FFFFFF; /* Clean white background */
        color: #333333; /* Dark text for contrast */
    }
    .stButton > button {
        background-color: #ADD8E6; /* Soft blue */
        color: black;
        border-radius: 5px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold; /* Make the text bold */
        transition: background-color 0.3s, transform 0.3s;
        border: none; /* Remove default border */
        cursor: pointer; /* Pointer cursor for buttons */
    }
    .response-container {
        font-size: 20px;
        color:#f9f9f9;
        background-color: black; /* Light grey background for result box */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        border-left: 5px solid #34A853; /* Accent color to the left */
    }
    </style>
""", unsafe_allow_html=True)

# Centered title with custom spacing
st.markdown("<h1 class='header-text'>🔍 Veritas AI Fact Checker</h1>", unsafe_allow_html=True)

# Adjusted Lottie animation (smaller size)
if lottie_google_fact_check:
    st_lottie(lottie_google_fact_check, height=150, key="google_fact_check")
else:
    st.error("Failed to load animation. Please check the URL.")

# Centered introduction with increased spacing
st.markdown("""
    <div class="fade-in">
    <h2 class="header-text">Check the facts before you believe them!</h2>
    <p class="subheader-text">Powered by Google's vibrant spirit and advanced AI technologies</p>
    </div>
""", unsafe_allow_html=True)

# First two input fields side by side using st.columns, with spacing
st.markdown("<h3 class='subheader-text fade-in'>Select Category and Action:</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)  # Create two columns

# Updated category dropdown in the first column with the specified categories
with col1:
    category = st.selectbox("Choose a category:", 
                            ["criminal_cases", "sports_cases", "economic_cases", 
                             "historical_fake_news", "important_personalities", 
                             "political_social_cases", "science_facts"], 
                            key="category", index=0)

# Updated action dropdown in the second column with specified tasks
with col2:
    task = st.selectbox("Choose an action:", ["fact_check", "source_finding"], key="task", index=0)

# Full-width input area for URL and file upload with spacing
st.markdown("<h3 class='subheader-text fade-in'>Enter a Video URL or Upload a Video:</h3>", unsafe_allow_html=True)

# URL and video file uploader in full width with spacing
video_url = st.text_input("Paste the URL here:", "", key="video_url_fullscreen")
uploaded_file = st.file_uploader("Or upload a video file:", type=["mp4", "mov", "avi"], key="video_upload_fullscreen")


# import streamlit as st
import time


# Display the response after 10 seconds delay
# Submit button with added spacing
if st.button("Submit"):
    with st.spinner("Processing your request..."):
        time.sleep(2)
    


    # Example usage for each fact:

    
    # Simulate API call delay
    # time.sleep(2)  # Reduced delay for a smoother experience

    # Prepare the request payload
    payload = {
        "category": category,
        "task": task,
        "url": video_url if video_url else None,
        "file": uploaded_file if uploaded_file else None
    }


    

    # Send the request to the API
    response = requests.post("http://localhost:8000/process-video", data=payload)

    # Check the response from the server

    # Check the response from the server
    # Check the response from the server
    if response.status_code == 200:
        result_data = response.json()

        # Debugging: Check result_data structure
        print("Result Data:", result_data)

        # Display the full response without parsing
        if "result" in result_data:
            # Display the entire response in a styled container
            st.markdown(f"<div class='response-container'>{result_data['result']}</div>", unsafe_allow_html=True)
        else:
            st.error("No valid results returned from the server.")
    else:
        st.error(f"Error processing the request: {response.text}")    # Additional table styling
    st.markdown("""
    <style>
    table {
        font-size: 16px;
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    th {
        background-color: #f2f2f2;
    }
    </style>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer-text fade-in">
        <h4>Built for Google Hackathon 🚀</h4>
        <p>By Veritas AI | Powered by Network 18</p>
    </div>
""", unsafe_allow_html=True)
