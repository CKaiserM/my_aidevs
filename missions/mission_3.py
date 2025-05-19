

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

import os
from dotenv import load_dotenv
from send_response import send_response
load_dotenv()

def mission_3(api_key):
    openai.api_key = api_key
    json_txt_file = requests.get(os.getenv("CENTRALA_FILE"))
    json_txt_file = json_txt_file.json()
    json_txt_file["apikey"] = os.getenv("MY_API")
    
    test_data = json_txt_file.get("test-data")
    for data in test_data:
        question = data.get("question")
        answer = data.get("answer")
        # Check if question matches answer and calculate if needed
        try:
            clean_question = re.sub(r'[^0-9+\-*/().\s]', '', question)
            calculated_answer = eval(clean_question)
            if int(answer) != int(calculated_answer):  # If answer differs
                data["answer"] = calculated_answer  # Update with correct calculation
        except:
            pass  # Skip if we can't evaluate the expression
        
        test = data.get("test")
        #print(answer)
        if test:
            q = test.get("q")
            #print(q)
            test["a"] = generate_answer(q)
            #print(test)
    #print(json_txt_file)

    response = send_response(os.getenv("RAPORT_URL"), "JSON", json_txt_file)
    print("Response:", response)

@observe()
def generate_answer(question):
    answer = openai.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
        {"role": "system", "content": "Return only the answer, not the question. "},
        {"role": "user", "content": question},
        
    ]
    ).choices[0].message.content

    #print(answer)
    return answer