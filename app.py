"""
AI Devs Course Project - Mission Runner

A script for executing various missions from the AI Devs course that interact with xyz.ag3nts.org API.

Each mission focuses on different aspects like:
- Working with OpenAI APIs and GPT models
- Image processing and analysis 
- API integrations
- Natural language processing tasks

Configuration:
    Required environment variables:
    - OPENAI_API_KEY: For GPT model access
    - USERNAME/PASSWORD: For API authentication
    - BASE_URL/SUB_URL: API endpoints

Usage:
    Run the script and enter the mission number (1-15) when prompted.
    The corresponding mission handler will be executed.

Dependencies:
    - requests: HTTP requests
    - beautifulsoup4: HTML parsing
    - openai: GPT model interaction
    - python-dotenv: Environment variables
"""

import os
from dotenv import load_dotenv
from missions import (
    mission_1, mission_2, mission_3, mission_4, mission_5,
    mission_6, mission_7, mission_8, mission_9, mission_10,
    mission_11, mission_12, mission_13, mission_14, mission_15, mission_16, mission_17, mission_18
)

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USERNAME = os.getenv("USERNAME") 
PASSWORD = os.getenv("PASSWORD")
BASE_URL = os.getenv("BASE_URL")
SUB_URL = os.getenv("SUB_URL")

def run_mission(mission_num):
    """Execute the specified mission with appropriate parameters"""
    
    # Missions that require API key only
    api_key_missions = {
        "3": mission_3.mission_3,
        "4": mission_4.mission_4,
        "5": mission_5.mission_5,
        "6": mission_6.mission_6,
        "7": mission_7.mission_7,
        "8": mission_8.mission_8,
        "9": mission_9.mission_9,
        "10": mission_10.mission_10
    }
    
    # Missions with no parameters
    simple_missions = {
        "11": mission_11.mission_11,
        "12": mission_12.mission_12,
        "13": mission_13.mission_13,
        "14": mission_14.mission_14,
        "15": mission_15.mission_15,
        "16": mission_16.mission_16,
        "17": mission_17.mission_17,
        "18": mission_18.mission_18
    }

    try:
        if mission_num == "1":
            mission_1.mission_1(BASE_URL, USERNAME, PASSWORD, OPENAI_API_KEY)
        elif mission_num == "2":
            mission_2.mission_2(BASE_URL, SUB_URL, OPENAI_API_KEY)
        elif mission_num in api_key_missions:
            api_key_missions[mission_num](OPENAI_API_KEY)
        elif mission_num in simple_missions:
            simple_missions[mission_num]()
        else:
            print("Invalid mission number. Please enter a number between 1-18.")
    except Exception as e:
        print(f"Error executing mission {mission_num}: {str(e)}")

if __name__ == "__main__":
    mission_number = input("Enter mission number (1-18): ")
    run_mission(mission_number)
    exit()
