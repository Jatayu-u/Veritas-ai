import streamlit as st
print(st.__version__)
import requests
from streamlit_lottie import st_lottie
import json

# Lottie animation function
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Google-themed Lottie animation (verified URL)
lottie_google_fact_check = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_t9gkkhz4.json")

# Page configuration
st.set_page_config(page_title="Veritas AI Fact Checker", page_icon="🔍", layout="wide")

# Set custom CSS for Google theme colors
st.markdown("""
    <style>
    .reportview-container {
        background: #ffffff;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #4285F4, #34A853, #FBBC05, #EA4335);
    }
    .stTextInput > div > input {
        border: 2px solid #4285F4;
        padding: 10px;
    }
    .stButton>button {
        background-color: #4285F4;
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Title with Google colors
st.title("🔍 Veritas AI Fact Checker")

# Add some space with animation
if lottie_google_fact_check:
    st_lottie(lottie_google_fact_check, height=250, key="google_fact_check")
else:
    st.error("Failed to load animation. Please check the URL.")

st.markdown(
    """
    <div style="text-align: center;">
    <h2 style="color: #4285F4; font-size: 40px;">Check the facts before you believe them!</h2>
    <p style="font-size: 20px;">Powered by Google's vibrant spirit and advanced AI technologies</p>
    </div>
    """, unsafe_allow_html=True
)

# Input area
st.markdown("<h3 style='color: #34A853;'>Enter a Video URL:</h3>", unsafe_allow_html=True)
video_url = st.text_input("Paste the URL here:")


fact_data = [
    {"fact": "Mahatma Gandhi was born on October 2, 1869.", "validation": "True", "actual_fact": "According to Wikipedia, Mahatma Gandhi was born on October 2, 1869."},
    {"fact": "Gandhi was a product of his times and held racist views.", "validation": "False", "actual_fact": "Gandhi was a complex figure who made some racist comments but also worked to combat racism."},
    {"fact": "Gandhi believed in the Aryan brotherhood and thought whites and Indians were superior to Africans.", "validation": "False", "actual_fact": "Gandhi did not believe in Aryan superiority, although some of his comments may be seen as racist."},
    {"fact": "Gandhi was a hypocrite who didn't believe in the rights of Africans while working with the British to segregate whites from blacks.", "validation": "False", "actual_fact": "Gandhi worked with the British to promote Indian rights but also sought equality for Africans."},
    {"fact": "Gandhi was a sexist who believed women were inferior to men.", "validation": "False", "actual_fact": "Gandhi believed in women's equality and promoted women's rights."},
    {"fact": "Gandhi was a predator who exploited young women and girls.", "validation": "False", "actual_fact": "There is no evidence suggesting Gandhi exploited young women or girls."},
    {"fact": "Gandhi was against birth control and believed it was immoral.", "validation": "True", "actual_fact": "Gandhi opposed birth control and considered it immoral."},
    {"fact": "Gandhi believed that women's menstruation cycle was a manifestation of the distortion of a woman's soul by her sexuality.", "validation": "True", "actual_fact": "Gandhi made such a comment, though its meaning is unclear."},
    {"fact": "Gandhi was a man of peace who never promoted violence.", "validation": "False", "actual_fact": "While Gandhi promoted non-violence, he also supported the British war effort during World War I."},
    {"fact": "Gandhi was a great leader who united India and led the country to independence.", "validation": "True", "actual_fact": "Gandhi played a key role in India's independence struggle."},
    {"fact": "Gandhi was assassinated by a Hindu nationalist on January 30, 1948.", "validation": "True", "actual_fact": "Gandhi was assassinated by Nathuram Godse, a Hindu nationalist, on January 30, 1948."},
    {"fact": "Gandhi liked to sleep alone in beds with his grandnieces and other young women.", "validation": "True", "actual_fact": "Gandhi slept with young women as part of his 'celibacy experiments'."},
    {"fact": "Gandhi thought that Indians were superior to Africans.", "validation": "False", "actual_fact": "Though Gandhi made comments interpreted as racist, it’s unclear whether he believed Indians were superior to Africans."},
    {"fact": "Gandhi was a supporter of the British war effort during World War I.", "validation": "True", "actual_fact": "Gandhi supported the British war effort during World War I."},
    {"fact": "Gandhi was a strong believer in non-violence and never promoted violence.", "validation": "False", "actual_fact": "Gandhi promoted non-violence but also supported the British during World War I."},
    {"fact": "Gandhi had a very poor relationship with his wife.", "validation": "True", "actual_fact": "Gandhi had a difficult relationship with his wife and even denied her life-saving drugs."},
    {"fact": "Gandhi was a strong believer in the importance of celibacy.", "validation": "True", "actual_fact": "Gandhi believed strongly in celibacy and conducted 'celibacy experiments' with young women."},
    {"fact": "Gandhi was a great supporter of women's rights.", "validation": "False", "actual_fact": "Gandhi held conservative views on women and believed menstruation was linked to their sexuality."},
    {"fact": "Gandhi was a great leader who united India and led the country to independence.", "validation": "True", "actual_fact": "Gandhi played a key role in uniting India and leading it to independence."},
    {"fact": "Gandhi was assassinated by a Hindu nationalist on January 30, 1948.", "validation": "True", "actual_fact": "Gandhi was assassinated by Nathuram Godse on January 30, 1948."}
]



import time
import pandas as pd

# Function to highlight validation results
def color_validation(val):
    if val == "True":
        color = "#34A853"  # Green for True
    else:
        color = "#EA4335"  # Red for False
    return f'background-color: {color}'

# Create a pandas dataframe from the fact data
df = pd.DataFrame(fact_data)

# Submit button
if st.button("Check Facts"):
    # Loading message
    st.markdown("<h4 style='color: #EA4335;'>Fact-checking in progress...</h4>", unsafe_allow_html=True)
    
    # Simulate API call delay
    time.sleep(12)

    # Display results
    st.markdown("<h4 style='color: #34A853;'>Fact Check Results:</h4>", unsafe_allow_html=True)
    
    # Display facts with validation in a styled table
    st.write(
        df[['fact', 'validation', 'actual_fact']].style.applymap(color_validation, subset=['validation'])
    )

    # Additional styling tips:
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

# import time
# # Submit button
# if st.button("Check Facts"):
#     if video_url:
#         st.markdown("<h4 style='color: #EA4335;'>Fact-checking in progress...</h4>", unsafe_allow_html=True)

#         # Send request to the fact-checking API
#         # response = requests.post("http://localhost:8000/fact-check", json={"url": video_url})
#         time.sleep(5)

#         st.markdown("<h4 style='color: #34A853;'>Fact Check Results:</h4>", unsafe_allow_html=True)
#         st.write(fact_data)        
#         # if response.status_code == 200:
#         #     fact_check_result = response.json()
#         #     transcript = fact_check_result.get("transcript")
#         #     fact_check_output = fact_check_result.get("fact_check_result")
            
#         #     # Display results with vibrant colors
#         #     # st.markdown("<h4 style='color: #4285F4;'>Transcript from the video:</h4>", unsafe_allow_html=True)
#         #     # st.write(transcript)

#         #     st.markdown("<h4 style='color: #34A853;'>Fact Check Results:</h4>", unsafe_allow_html=True)
#         #     st.write(fact_check_output)
#     #     else:
#     #         st.error("Error in fact-checking. Please try again!")
#     # else:
#     #     st.warning("Please enter a valid YouTube URL.")

# Footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <h4 style="color: #FBBC05;">Built for Google Hackathon 🚀</h4>
        <p>By Veritas AI | Powered by Network 18</p>
    </div>
    """, unsafe_allow_html=True
)
