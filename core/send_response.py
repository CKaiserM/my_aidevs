"""
This module provides a function to send responses to the report endpoint.

Functions:
    send_response(url, answer): Sends a response to the report endpoint.

Dependencies:
    - requests: For making HTTP requests to the report endpoint
    - os: For accessing environment variables
    - dotenv: For loading environment variables from a .env file
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()
def send_response(url, task, answer):
    print("Sending response to:", url)
    print("Task:", task)
    print("Answer:", answer)
    response = requests.post(url, json={"task": task, "apikey": os.getenv("MY_API"), "answer": answer}, headers={'Content-Type': 'application/json; charset=utf-8'})
    response_json = response.json()
    #print("Response json:", response_json)

    return response_json

