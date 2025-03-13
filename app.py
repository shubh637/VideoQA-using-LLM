
import os
import streamlit as st
from main import *
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Create temp_video directory if it doesn't exist
if not os.path.exists("temp_video"):
    os.makedirs("temp_video")
background= f"""
    <style>
[data-testid="stApp"] {{
background: linear-gradient(325deg,#2C67F2 0%,#86fde8 68%,#9796f0 98%);
background-size: 180% 180%;
animation: gradient-animation 12s ease infinite;
}}
@keyframes gradient-animation {{
  0% {{
    background-position: 0% 50%;
  }}
  50% {{
    background-position: 100% 50%;
  }}
  100% {{
    background-position: 0% 50%;
  }}
}}
</style>"""
# st.markdown(background, unsafe_allow_html=True) uncomment it for css.
# Streamlit page config
st.title("Video Transcript & Question-Answering System")
st.write("Upload a video or provide a YouTube URL, and ask questions based on the transcript.")

# Video upload or URL input
video_option = st.selectbox("Select input method:", ["Upload Video", "Provide YouTube URL"])

# Display input options based on the user's choice
if video_option == "Upload Video":
    video_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv", "webm"])
    if video_file:
        # Save the uploaded file temporarily
        video_path = os.path.join("temp_video", video_file.name)
        with open(video_path, "wb") as f:
            f.write(video_file.getbuffer())
        st.video(video_path)
else:
    video_url = st.text_input("Enter YouTube Video URL")
    if video_url:
        st.video(video_url)

# Ask user to input a question based on the video
query = st.text_input("Ask a question based on the transcript of the video:")

if st.button("Get Answer"):
    if video_option == "Upload Video" and video_file:
        # Process uploaded video
        st.write("Processing video...")
        transcript = extract_audio_text(video_path)
    elif video_option == "Provide YouTube URL" and video_url:
        # Process YouTube video
        st.write("Processing YouTube video...")
        transcript = extract_audio_text(video_url)
    else:
        st.error("Please provide either a video file or a YouTube URL.")

    if transcript:
        st.write("Transcript extracted successfully!")
        # Get the answer for the query
        answer = ask_openrouter(query, transcript)
        st.write("### Answer:")
        st.write(answer)
    else:
        st.error("Failed to extract transcript. Please check the video format or URL.")
