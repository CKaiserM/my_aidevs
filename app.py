"""
    A script for interacting with the xyz.ag3nts.org API to complete various missions.

    This script provides functionality to:
    - Execute Mission 1: Solves mathematical questions using GPT-4.1 Nano and submits answers
    - Execute Mission 2: Engages in a message-based interaction with custom knowledge constraints

    Configuration:
        - OpenAI API key for GPT-4.1 Nano access
        - Login credentials (username/password) for API authentication
        - Base URL and sub-URL for API endpoints

    Usage:
        Run the script and select mission 1 or 2 when prompted.
        The appropriate mission handler will be called with required parameters.

    Dependencies:
        - requests: For making HTTP requests
        - beautifulsoup4: For parsing HTML responses
        - openai: For interacting with GPT-4.1 Nano
        - re: For extracting numeric answers from responses
"""

import requests
from bs4 import BeautifulSoup
import openai
import re
from missions.mission_1 import mission_1
from missions.mission_2 import mission_2

import os
from dotenv import load_dotenv

load_dotenv()
# OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
# Dane logowania i odpowiedź
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Adres docelowy
base_url = "https://xyz.ag3nts.org/"
sub_url = "verify"

if __name__ == "__main__":
    mission_number = input("Enter mission number (1 or 2): ")
    
    match mission_number:
        case "1":
            mission_1(base_url, username, password, api_key)
        case "2":
            mission_2(base_url, sub_url, api_key)
        case _:
            print("Invalid mission number. Please enter 1 or 2.")
    exit()


