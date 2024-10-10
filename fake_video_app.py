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

genai.configure(api_key='')
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
Analyze the provided video for any indications of tampering, editing, or manipulation. Your analysis should include the following details:

1. **Tampering Detection**:
   - Identify specific timestamps where tampering or editing is suspected.
   - Describe the nature of the suspected alterations (e.g., visual edits, audio modifications, splicing).

2. **Detailed Insights**:
   - Provide logical reasoning for each identified tampering instance, including any inconsistencies in audio and visual elements.
   - Discuss any discrepancies in lighting, shadows, or other visual artifacts that suggest manipulation.

3. **Content Analysis**:
   - Evaluate the authenticity of the spoken or visual content, indicating if the video has been altered to convey a different message.
   - Highlight specific phrases or images that appear altered or out of context.

4. **Confidence Score**:
   - Assign a confidence score (0-100%) for each identified tampering instance, based on the evidence gathered during the analysis.

5. **Edited Parts**:
   - List any sections of the video that have been edited, providing timestamps and a brief description of the changes made.

6. **Summarization**:
   - Conclude with a summary of your findings, highlighting the overall authenticity of the video and any significant areas of concern.

Ensure your analysis is thorough and well-structured, supporting each claim with logical reasoning and evidence drawn from the video.

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
