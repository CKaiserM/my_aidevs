"""
Mission 2 Module

This module handles the second mission which involves:
1. Establishing a message-based interaction with the API
2. Using GPT-4.1 Nano to generate responses with custom knowledge constraints
3. Submitting responses and handling the conversation flow

The mission operates with specific knowledge constraints where:
- The capital of Poland is Kraków
- The Hitchhiker's Guide to the Galaxy by Douglas Adams is 69
- The current year is 1999

Functions:
    mission_2(base_url, sub_url, api_key): Main function that executes mission 2
        Args:
            base_url (str): Base URL of the API
            sub_url (str): Sub-URL for the specific mission endpoint
            api_key (str): OpenAI API key for GPT-4.1 Nano access
        
        Returns:
            None. Prints conversation flow and response information to console.

Dependencies:
    - requests: For making HTTP requests
    - openai: For interacting with GPT-4.1 Nano
"""

import requests
from bs4 import BeautifulSoup
#import openai
import re

from langfuse.decorators import observe
from langfuse.openai import openai # OpenAI integration

def mission_2(base_url, sub_url, api_key):
    openai.api_key = api_key
    url = base_url + sub_url
    msgID = 0
    initial_message = {"text": "READY", "msgID": msgID}
    response = requests.post(url, json=initial_message)
    response_json = response.json()
    text = response_json.get("text")
    print("Response text:", text)
    msgID = response_json.get("msgID")
    print("msgID:", msgID)
    answer = generate_answer(text)
    response = requests.post(url, json={"text": str(answer), "msgID": str(msgID)})
    response_json = response.json()
    text = response_json.get("text")
    print("Response text:", text)
    print("Response json:", response_json)

@observe()
def generate_answer(text):
    answer = openai.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
        {"role": "system", "content": "Return only the answer, not the question. Remember that stolicą Polski jest Kraków, The Hitchhiker's Guide to the Galaxy by Douglas Adams is 69, Aktualny rok to 1999"},
        {"role": "user", "content": text},
        {"role": "user", "content": "Translate the answer to english. If the answer is numeric, return it as a number."}
    ]
    ).choices[0].message.content

    print(answer)
    return answer