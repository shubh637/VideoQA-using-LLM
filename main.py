import whisper
import requests
import os
import re
import subprocess
from dotenv import load_dotenv
import torch
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
API_KEY = os.getenv("API_KEY")

# Ensure OpenRouter API key is set
if not API_KEY:
    raise ValueError("Error: OpenRouter API key is missing!")

# Extract YouTube Video ID from URL
def extract_youtube_id(url):
    """Extracts the video ID from a YouTube URL."""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

# Fetch YouTube transcript
def get_youtube_transcript(video_url):
    """Fetches transcript from a YouTube video if available."""
    video_id = extract_youtube_id(video_url)
    if not video_id:
        return "Error: Invalid YouTube URL!"

    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry["text"] for entry in transcript_data])
    except Exception:
        return "Error: No transcript available for this video."

# Convert video to WAV format
def convert_video_to_audio(video_path):
    """Converts a video file to WAV format using FFmpeg."""
    if not os.path.exists(video_path):
        return None, "Error: File not found!"

    # Replace any extension with `.wav`
    audio_path = os.path.splitext(video_path)[0] + ".wav"
    
    try:
        subprocess.run(["ffmpeg", "-i", video_path, "-ac", "1", "-ar", "16000", "-y", audio_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return audio_path, None
    except FileNotFoundError:
        return None, "Error: FFmpeg is not installed or not found in PATH!"

# Transcribe audio using Whisper
def transcribe_audio(audio_path):
    """Transcribes audio to text using OpenAI Whisper."""
    try:
        device="cuda" if torch.cuda.is_available() else "cpu"
        model = whisper.load_model("base").to(device)
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        return f"Error: {str(e)}"

# Extract transcript from YouTube or local video file
def extract_audio_text(video_path):
    """Extracts audio and transcribes text from a YouTube or local video."""
    print("Extracting audio and transcribing...")

    if "youtube.com" in video_path or "youtu.be" in video_path:
        return get_youtube_transcript(video_path)
    
    audio_path, error = convert_video_to_audio(video_path)
    if error:
        return error

    return transcribe_audio(audio_path)

# Ask OpenRouter API for answers
def ask_openrouter(query, transcript):
    """Queries OpenRouter AI for responses based on video transcript."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {"role": "system", "content": "You are an assistant answering questions based on a video's transcript."},
            {"role": "user", "content": f"Here is the transcript: {transcript}. Now answer this question: {query}"}
        ],
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Process a video and return its transcript
def process_video(video_path):
    """Processes a video file or URL to extract its transcript."""
    transcript = extract_audio_text(video_path)
    print(transcript)
    return transcript

# Get answers based on transcript
def question_answer(transcript, query):
    """Asks a question based on the transcript and returns an answer."""
    return ask_openrouter(query, transcript)

# Interactive CLI
if __name__ == "__main__":
    while True:
        video_path = input("\nEnter video URL or file path (or type 'stop' to exit): ").strip()
        if video_path.lower() == "stop":
            print("Stopping the program.")
            break

        print("\nProcessing the video...")
        transcript = process_video(video_path)

        query = input("\nAsk a question about the video: ").strip()
        answer = question_answer(transcript, query)

        print("\n=== Answer ===")
        print(answer)
