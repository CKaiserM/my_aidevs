"""
Mission 5 Module

This module handles the fifth mission which involves:
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
import zipfile

from langfuse.decorators import observe
from langfuse.openai import openai # OpenAI integration
from bs4 import BeautifulSoup

import os
from dotenv import load_dotenv
from core.send_response import send_response 
from core.openai_functions import generate_answer, process_recordings
load_dotenv()

def mission_5(api_key):
    openai.api_key = api_key
    text_contents = []  
    if not os.path.exists("transcriptions.txt"):
    # Get the zip file from the RECORDINGS URL and process each audio file
        zip_response = requests.get(os.getenv("RECORDINGS"))
        with open("temp.zip", "wb") as f:
            f.write(zip_response.content)
        
        # Create temporary directory for audio files
        temp_dir = "temp_audio"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        # Extract and process each audio file
        with zipfile.ZipFile("temp.zip", "r") as zip_ref:
            zip_ref.extractall(temp_dir)
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                text_contents.append(process_recordings(file_path))
                
            # Combine all text contents
        txt_file = "\n".join(text_contents)
        #print("--------------------------------")
        #print("Text file:", txt_file)
        #print("--------------------------------")
        # Write the combined text to a file
        with open("transcriptions.txt", "w", encoding="utf-8") as f:
            f.write(txt_file)
    # Remove temporary directory and its contents
    #for file in os.listdir(temp_dir):
    #    os.remove(os.path.join(temp_dir, file))
    #os.rmdir(temp_dir)
    
    # Clean up temp file
    #os.remove("temp.zip")
        
    else:
        with open("transcriptions.txt", "r", encoding="utf-8") as f:
            txt_file = f.read()

    aiModel = "gpt-4.1"
    aiMessage = [{"role": "system", "content": "Return only the answer, not the question. In the text extract the information about name of the institute where proffesor Andrzej Maj was teaching. W internecie znajdz adres instytutu. Zwróc tylko nazwe ulicy bez słowa ulica i bez numeru."},
                 {"role": "user", "content": txt_file}]

    answer = generate_answer(aiModel, aiMessage)
    print("--------------------------------")
    print("Answer:", answer)
    print("--------------------------------")
    
    response = send_response(os.getenv("RAPORT_URL"), "mp3", answer)
    print("Response:", response)

    # Clean up temp file
    #os.remove("temp.zip")  


