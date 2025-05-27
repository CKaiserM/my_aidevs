

"""
Mission 3 Module

This module handles the third mission which involves:
1. Fetching and processing JSON data from a centralized file
2. Validating and correcting mathematical calculations in test data
3. Generating answers using GPT-4.1 Nano
4. Submitting processed data back to the report endpoint

Dependencies:
    - requests: For making HTTP requests to fetch JSON and submit reports
"""

import requests
import re

from langfuse.decorators import observe
from langfuse.openai import openai # OpenAI integration
from bs4 import BeautifulSoup

import os
from dotenv import load_dotenv
from core.send_response import send_response
from core.openai_functions import generate_answer

load_dotenv()

def mission_4(api_key):
    txt_file = requests.get(os.getenv("CENTRALA_FILE_2"))
    print(txt_file.text)

    aiModel = "gpt-4.1-nano"
    aiMessage = [{"role": "system", "content": "Return only the answer, not the question. Change full name and surname to single word CENZURA, change the only the city name to CENZURA, change only the Street name and street number to single word CENZURA, finally find age and change only the number to CENZURA."},
                 {"role": "user", "content": txt_file.text}]
    answer = generate_answer(aiModel, aiMessage)
    print(answer)
    response = send_response(os.getenv("RAPORT_URL"), "CENZURA", answer)
    print("Response:", response)


