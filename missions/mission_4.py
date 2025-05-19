

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

load_dotenv()

def mission_4(api_key):
    openai.api_key = api_key
    txt_file = requests.get(os.getenv("CENTRALA_FILE_2"))
    print(txt_file.text)
    answer = generate_answer(txt_file.text)
    print(answer)

    response = requests.post(os.getenv("RAPORT_URL"), json={"task": "CENZURA", "apikey": os.getenv("MY_API"), "answer": answer})
    response_json = response.json()

    print("Response json:", response_json)

@observe()
def generate_answer(text):
    answer = openai.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
        {"role": "system", "content": "Return only the answer, not the question. Change full name and surname to single word CENZURA, change the only the city name to CENZURA, change only the Street name and street number to single word CENZURA, finally find age and change only the number to CENZURA."},
        {"role": "user", "content": text}
    ]
    ).choices[0].message.content
    return answer