# !pip install openai-whisper requests
import whisper
import requests
import os
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

# Get API keys from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
API_KEY = os.getenv("API_KEY")



genai.configure(api_key=os.getenv(GOOGLE_API_KEY))

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

# Function to extract audio from video and convert to text
def extract_audio_text(video_path):
    print("Extracting audio and transcribing...")
    if "https://www.youtube.com" in video_path:
        transcript=extract_transcript_details(video_path)
        return transcript
    else:
        model = whisper.load_model("base")  # Use the Whisper model
        result = model.transcribe(video_path)
        return result["text"]  

# Function to query OpenRouter for answers based on the transcribed text
def ask_openrouter(query, transcript):
    """Get responses from OpenRouter API using DeepSeek model."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }
    data = {
        "model": "deepseek/deepseek-r1:free",  # Use the DeepSeek model
        "messages": [
            {"role": "system", "content": "You are an assistant that answers questions based on the transcript of a video."},
            {"role": "user", "content": f"Here is the transcript: {transcript}. Now answer this question: {query}"}
        ],
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        answer = response_data["choices"][0]["message"]["content"]
        return answer
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't fetch a response from OpenRouter."

# Main function to process the video and get answers
def process_video(video_path):
    # Extract text from the video
    transcript = extract_audio_text(video_path)
    print(transcript)
    return transcript


def question_answer(transcript,query):
    # Ask a question based on the transcript
    answer = ask_openrouter(query, transcript)
    return answer



if __name__ == "__main__":
    while True:
        # Ask the user for the video file path
        video_path = input("Enter the path to the video file (or type 'stop' to exit): ").strip()

        # Stop if the user types 'stop'
        if video_path.lower() == "stop":
            print("Stopping the program.")
            break
        # Process the video and provide an answer
        print("\n Processing the video...")
        transcript=process_video(video_path)
        # Ask for the query
        query = input("Ask a question based on the video: ").strip()

        #taking response
        answer = question_answer(transcript,query)
        print("\n=== Answer ===")
        print(answer)
