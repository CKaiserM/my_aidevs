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
from missions.mission_3 import mission_3
from missions.mission_4 import mission_4
from missions.mission_5 import mission_5
from missions.mission_6 import mission_6
from missions.mission_7 import mission_7
from missions.mission_8 import mission_8
import os
from dotenv import load_dotenv

load_dotenv()
# OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
# Dane logowania i odpowiedź
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Adres docelowy
base_url = os.getenv("BASE_URL")
sub_url = os.getenv("SUB_URL")

if __name__ == "__main__":
    mission_number = input("Enter mission number (1 or 2 or 3 or 4 or 5 or 6 or 7 or 8): ")
    
    match mission_number:
        case "1":
            mission_1(base_url, username, password, api_key)
        case "2":
            mission_2(base_url, sub_url, api_key)
        case "3":
            mission_3(api_key)
        case "4":
            mission_4(api_key)
        case "5":
            mission_5(api_key)
        case "6":
            mission_6(api_key)
        case "7":
            mission_7(api_key)
        case "8":
            mission_8(api_key)
        case _:
            print("Invalid mission number. Please enter 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8.")
    exit()


