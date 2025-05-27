"""
    Mission 7 Module

This module handles the seventh mission which involves:
1. Downloading and extracting audio recordings from a zip file
2. Processing and transcribing audio files
3. Combining transcriptions into a single text file
4. Storing results for later analysis

Dependencies:
    - requests: For downloading zip file of recordings
    - zipfile: For extracting audio files
    - os: For file and directory operations
    - dotenv: For loading environment variables
"""

import requests
import re

import os
from dotenv import load_dotenv
from core.send_response import send_response 
from core.openai_functions import generate_image, generate_answer

load_dotenv()

def mission_7(api_key):
    description = requests.get(os.getenv("DESCRIPTION"))
    
    raw_prompt = description.json().get("description")
    aiModel = "gpt-4.1-nano"
    aiMessage = [{"role": "system", "content": "Return only the answer, not the question. Generate prompt for DALL-E from description"},
                 {"role": "user", "content": raw_prompt}]
    prompt = generate_answer(aiModel, aiMessage)
    print(prompt)
    answer = generate_image(prompt)
    print(answer)
    response = send_response(os.getenv("RAPORT_URL"), "robotid", answer)
    print("Response:", response)


