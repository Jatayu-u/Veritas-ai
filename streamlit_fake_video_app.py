import streamlit as st
import requests
import json
from PIL import Image

# Set the page config
st.set_page_config(page_title="Fake Video Finder", page_icon="🎥")

# Add a title and description
st.title("Fake Video Finder 🌟")
st.markdown("""
    ### Analyze Your Videos for Tampering
    Upload a video to check if it has been altered or tampered with. 
    This application uses advanced AI to provide insights on any suspected modifications.
""", unsafe_allow_html=True)

# Create a sidebar for navigation
st.sidebar.header("Upload Video")
st.sidebar.markdown("""
    This application is part of the Google Hackathon. 
    Let's detect any alterations in your videos!
""")

# Add a colorful Google-themed style
st.markdown(
    """
    <style>
        .title {
            color: #4285F4;
            font-weight: bold;
            font-size: 24px;
        }
        .description {
            color: #EA4335;
            font-size: 18px;
        }
        .result {
            background-color: "brown";
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #ccc;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }
        .loader {
            text-align: center;
            margin-top: 50px;
        }
        .success {
            color: #34A853;
            font-weight: bold;
            font-size: 18px;
        }
        .error {
            color: #EA4335;
            font-weight: bold;
            font-size: 18px;
        }
    </style>
    """, unsafe_allow_html=True
)

# File uploader for video files
uploaded_file = st.sidebar.file_uploader("Choose a video file...", type=["mp4", "mov", "avi"])

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
if st.sidebar.button("Analyze Video") and uploaded_file is not None:
    # Show loader while processing
    with st.spinner("Analyzing your video... This may take a few moments! ⏳"):
        result = analyze_video(uploaded_file)

    if result:
        st.sidebar.success("Analysis Complete! 🎉")

        # Display results
        st.subheader("Analysis Results")

        # # If tampered segments exist, display them
        # if result['tampered_segments']:
        #     st.markdown("**Tampered Segments:**")
        #     for timestamp, details in result['tampered_segments'].items():
        #         st.markdown(f"- **Timestamp:** {timestamp} - **Details:** {details}")
        # else:
        st.markdown("Tampering detected! ")

        # Display insights
        st.markdown("### Insights:")
        insights = result['insights']

        # Display insights with a colorful layout
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
    Created for the Google Hackathon. Powered by FastAPI and Streamlit! 🚀
""", unsafe_allow_html=True)
