import time
import requests
import os
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
# from gemini_sdk import Gemini

import pandas as pd
import os
import textwrap
import google.generativeai as genai
from IPython.display import Markdown, Image as IPImage
from PIL import Image

genai.configure(api_key='AIzaSyAAF1cFQJy_zDZKIx8NhZuHKBExZ7mHYLM')
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()



class VideoAnalysisResponse(BaseModel):
    tampered_segments: dict
    insights: str

# Helper function to upload and process the video
def upload_and_process_video(video_path: str):
    print(f"Uploading file {video_path}...")
    video_file = genai.upload_file(path=video_path)
    print(f"Completed upload: {video_file.uri}")
    
    # Wait for the file to be processed and ready for inference
    while video_file.state.name == "PROCESSING":
        print('.', end='')
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError("Video upload failed")

    return video_file

# Analyze the video for tampering and generate insights
def analyze_video(video_file):
    prompt = """
    Analyze this video and check if any parts of it have been tampered with using AI or have been altered to say something different. 
    If tampered, identify the timestamps and provide detailed insights on why the tampering is suspected.
    """
    print("Making LLM inference request...")
    response = model.generate_content([video_file, prompt], request_options={"timeout": 600})
    
    return response.text

@app.post("/analyze_video/", response_model=VideoAnalysisResponse)
async def analyze_video_endpoint(file: UploadFile = File(...)):
    os.makedirs("./videos", exist_ok=True)

    file_location = f"./videos/{file.filename}"

    # Ensure the directory exists
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    # Upload and process the video using Gemini's API
    video_file = upload_and_process_video(file_location)

    # Analyze the video for tampering and get insights
    analysis_result = analyze_video(video_file)

    # Process the response to extract useful information
    tampered_segments = {}  # This should be parsed from the analysis_result based on detected tampering
    insights = analysis_result  # Full insights can be provided in this field

    # Cleanup uploaded file
    os.remove(file_location)

    return VideoAnalysisResponse(
        tampered_segments=tampered_segments,
        insights=insights
    )

# Start the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
