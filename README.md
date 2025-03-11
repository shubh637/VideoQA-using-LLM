# VideoQA Bot

## Overview
VideoQA Bot is an interactive system that allows you to ask questions based on the content of a video. The system extracts audio from the video, transcribes it into text, and then uses an AI model (via OpenRouter API) to answer any queries you have related to the video's content. It leverages the Whisper model for speech-to-text conversion and the DeepSeek model for answering questions based on the transcript.

---

## Features
- **Speech-to-Text Transcription**: Extracts audio from the video and converts it to text using the Whisper model.
- **Question-Answering**: Allows users to ask questions based on the video transcript, providing relevant answers using the DeepSeek model via the OpenRouter API.
- **Interactive**: Continuously runs in a loop, processing new videos and queries until the user opts to stop.

---

## Requirements
1. **Python 3.x**  
   Ensure you have Python 3.x installed.
   
2. **Libraries**:  
   Install the following libraries using `pip`:
   ```bash
   pip install whisper requests
