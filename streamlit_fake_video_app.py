import streamlit as st
import requests
from PIL import Image
from streamlit_lottie import st_lottie

# Lottie animation function
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animation
lottie_animation = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_t9gkkhz4.json")

# Set the page config
st.set_page_config(page_title="Fake Video Finder", page_icon="🎥", layout="wide")

# Add custom CSS for improved styling
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f4f8;
            color: #333;
        }
        
        .title-text {
            color: white; /* Light blue color */
            font-size: 42px; /* Larger font size for title */
            text-align: center; /* Centered title */
            margin-bottom: 2px; /* Closer spacing below title */
        }
        
        .header-text {
            color: #ADD8E6; /* Light blue color */
            font-size: 36px;
            text-align: center; /* Centered header */
            margin-bottom: 10px; /* Slightly reduced space below header */
        }
        
        .subheader-text {
            color: white; /* Light blue color */
            font-size: 18px;
            text-align: center; /* Centered subheader */
            margin-bottom: 10px; /* Space below subheader */
        }
        
        .result {
            background-color: black;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #ddd;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
            animation: slideIn 0.5s; /* Slide-in animation */
        }
        
        .button {
            background-color: #4285F4; /* Soft blue */
            color: white;
            border-radius: 5px;
            padding: 12px 24px;
            font-size: 16px;
            border: none; /* Remove default border */
            cursor: pointer; /* Pointer cursor for buttons */
            transition: background-color 0.3s, transform 0.3s;
            margin-top: 10px; /* Space above button */
        }
        
        .button:hover {
            background-color: #357ae8; /* Darker blue on hover */
            transform: translateY(-2px); /* Slightly lift the button */
        }
        
        @keyframes slideIn {
            from {
                transform: translateY(-20px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .fade-in {
            animation: fadeIn 1s; /* Fade-in effect */
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            font-size: 14px;
            color: #777;
        }
        
        .footer a {
            color: #4285F4;
            text-decoration: none; /* No underline for links */
        }
        
        .footer a:hover {
            text-decoration: underline; /* Underline on hover */
        }
    </style>
    """, unsafe_allow_html=True
)

# Add a title and description
st.markdown("""
    <h1 class="title-text">Fake Video Finder 🌟</h1>
    <h2 class="header-text">Analyze Your Videos for Tampering</h2>
    <p class="subheader-text">
        Upload a video to check if it has been altered or tampered with. 
        This application uses advanced AI to provide insights on any suspected modifications.
    </p>
""", unsafe_allow_html=True)

# Display Lottie animation
if lottie_animation:
    st_lottie(lottie_animation, height=200, key="animation")
else:
    st.error("Failed to load animation. Please check the URL.")

# File uploader for video files
st.markdown("<h3 style='text-align: center;'>Upload Video File</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "mov", "avi"], label_visibility="collapsed")

# Function to analyze the video
def analyze_video(file):
    """Function to send video to the FastAPI endpoint for analysis."""
    api_url = "http://localhost:8000/analyze_video/"
    files = {"file": file}

    try:
        response = requests.post(api_url, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        st.error(f"Error: {err}")
        return None

# Button to start analysis
if st.button("Analyze Video", help="Click to analyze your uploaded video", key="analyze_video"):
    if uploaded_file is not None:
        # Show loader while processing
        with st.spinner("Analyzing your video... This may take a few moments! ⏳"):
            result = analyze_video(uploaded_file)

        if result:
            st.success("Analysis Complete! 🎉")

            # Display results
            st.subheader("Analysis Results")

            # Display insights
            insights = result['insights']
            st.markdown(
                """
                <div class="result">
                {}
                </div>
                """.format(insights), unsafe_allow_html=True
            )

# Add a footer
st.markdown("""
    ---
    <div class="footer">
        Created for the Google Hackathon. Powered by FastAPI and Streamlit! 🚀 <br>
        <a href="https://github.com/" target="_blank">Visit our GitHub</a>
    </div>
""", unsafe_allow_html=True)
