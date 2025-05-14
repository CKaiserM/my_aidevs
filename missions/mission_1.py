"""
Mission 1 Module

This module handles the first mission which involves:
1. Fetching a mathematical question from a webpage
2. Using GPT-4.1 Nano to calculate the answer
3. Submitting the answer via a POST request

Functions:
    mission_1(url, username, password, api_key): Main function that executes mission 1

Dependencies:
    - requests: For making HTTP requests
    - beautifulsoup4: For parsing HTML responses
    - openai: For interacting with GPT-4.1 Nano
    - re: For extracting numeric answers from responses

Returns:
    None. Prints status and response information to console.
"""

import requests
from bs4 import BeautifulSoup
import openai
import re

def mission_1(url, username, password, api_key):
    
    openai.api_key = api_key
    # Step 1: Fetch question from webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    question_tag = soup.find("p", id="human-question")

    # Adres docelowy
    url = "https://xyz.ag3nts.org/"

    # Nagłówki
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    if not question_tag:
        raise ValueError("Could not find <p id='human-question'> on the page.")

    question = question_tag.get_text().strip()

    # Step 2: Send to ChatGPT using GPT-4.1 Nano
    completion = openai.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "Return only a numeric answer."},
            {"role": "user", "content": question}
        ]
    )

    # Step 3: Extract numeric answer
    answer = completion.choices[0].message.content.strip()
    numeric_match = re.search(r"[-+]?\d*\.\d+|\d+", answer)

    if numeric_match:
        numeric_answer = numeric_match.group()
        print("Numeric answer:", numeric_answer)
    else:
        print("No numeric answer found. Response was:", answer)

    # Ciało żądania (formularz)
    data = {
        "username": username,
        "password": password,
        "answer": answer
    }

    # Wykonanie żądania POST
    response = requests.post(url, data=data, headers=headers)

    # Wyświetlenie odpowiedzi
    print("Status kod:", response.status_code)
    print("Treść odpowiedzi:")
    print(response.text)
