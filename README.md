# **VideoQA Bot**

## Overview
VideoQA Bot is an interactive system that allows you to ask questions based on the content of a video.
Whisper Model (OpenAI): The model transcribes audio into text, which is a form of natural language processing (NLP). It's the first step in understanding the content of the video.
DeepSeek Model (OpenRouter): After transcribing the audio, you use an LLM to process and generate responses to user queries based on the content. DeepSeek here acts as the LLM that generates human-like answers.

---

## Features
- **Speech-to-Text Transcription**: Extracts audio from the video and converts it to text using the Whisper model.
- **Question-Answering**: Allows users to ask questions based on the video transcript, providing relevant answers using the DeepSeek model via the OpenRouter API.
- **Interactive**: Continuously runs in a loop, processing new videos and queries until the user opts to 
---

## Requirements
1. **Python 3.x**  
   Ensure you have Python 3.x installed.
   
2. **Libraries**:  
   Install the following libraries using `pip`:
   ```bash
   pip install whisper requests
