# Video Transcript & Question-Answering System

This project is a **video transcript extraction and question-answering system** that allows users to upload videos or provide YouTube URLs. It processes the video to extract the transcript and then answers questions based on the transcript using OpenRouter AI.

The system can transcribe audio using OpenAI's Whisper model or fetch a YouTube transcript directly. It also leverages the OpenRouter API to generate AI-based responses to user queries based on the extracted transcript.
### Web App Screenshot
![front page](exmaple_images/Screenshot%202025-03-12%20150528.png)
<p align="center">
    figure.1. User interface.
</p>

![front_page_1](exmaple_images/Screenshot%202025-03-12%20150541.png)
<p align="center">
    figure.2. can take youtube link or normal video.
</p>

![front_page_2](exmaple_images/Screenshot%202025-03-12%20151714.png)
 
<p align="center">
    figure.3. get the answer to the query using llm model.
</p>

## Features

- **Video Upload or YouTube URL Input**: Users can either upload a local video file or provide a YouTube URL for processing.
- **Transcript Extraction**: Transcribes the audio of the uploaded video or YouTube video.
- **Question-Answering**: Ask questions based on the extracted transcript, and get AI-generated answers using OpenRouter.
- **Supports Multiple Video Formats**: MP4, AVI, MOV, MKV, WebM, etc.

## Prerequisites

- Python 3.x
- FFmpeg (for video-to-audio conversion)
- Environment variables for Google API and OpenRouter API

## How It Works

1. **Video Processing**:
    - If a local video is uploaded, the video is converted into an audio file (WAV format) using **FFmpeg**.
    - If a YouTube URL is provided, the transcript is fetched directly using the **YouTube Transcript API**.

2. **Transcription**:
    - For local videos, the audio is transcribed using **OpenAI Whisper**.
    - For YouTube videos, the transcript is fetched if available.

3. **Question-Answering**:
    - The extracted transcript is then used to generate answers to user queries using the **OpenRouter AI** API.

## Environment Variables

The following environment variables must be set for the project to function properly:

- `GOOGLE_API_KEY`: Your Google API key.
- `API_KEY`: Your OpenRouter API key.

## Troubleshooting

- **FFmpeg Error**: If you encounter an error related to FFmpeg, ensure that FFmpeg is correctly installed and added to your system's PATH.
- **No Transcript Available**: For YouTube videos, if no transcript is available, the system will return an error message.



