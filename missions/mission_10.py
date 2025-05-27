"""
    Mission 7 Module

This module handles the seventh mission which involves:
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
import json
import os
import html2text
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from core.send_response import send_response 
from core.openai_functions import process_image, process_recordings, generate_answer, process_image_from_url

load_dotenv()

def mission_10(api_key):
    facts_file = "<facts>\n"
    facts = []
    for file in os.listdir("pliki_z_fabryki/facts"):
        
        if file.endswith(".txt"):
            with open(os.path.join("pliki_z_fabryki/facts", file), "r", encoding="utf-8") as f:
                filename = file.split(".")[0]
                content = f.read()
                facts.append(f"<fact {filename}>{content}</fact>")
    
    facts_string = "\n".join(facts)
    facts_string += "\n</facts>"

    #print(facts_string)

    chunks = []
    for file in os.listdir("pliki_z_fabryki"):
        if file.endswith(".txt"):
            with open(os.path.join("pliki_z_fabryki", file), "r", encoding="utf-8") as f:
                filename = file.split(".")[0]
                content = f.read()
                chunks.append(f"<chunk>{filename}.txt: {content}</chunk>")

    chunks_string = "\n".join(chunks)

    #print(chunks_string)
    user_prompt = f"{facts_string}\n{chunks_string}"

    user_prompt_1 = facts_string
    user_prompt_2 = chunks_string 

    system_prompt_1 = """    
   You are a helpful assistant that can answer questions and help with tasks.
You are given a set of <facts> and <chunks> (report files in plain text format).
Your task is to analyze each of them according to the following steps:

For each of the 9 facts <fact f0x>:
Extract and identify key information:

- What happened?
- Where did it happen?
- Who was involved?
- What items or technologies appeared?
- Include names of people, roles, places, technologies, and items.

Generate list of keywords for each fact

For each of the 10 report files <chunk>:
Analyze the content of the report. Extract and identify:

- What happened?
- Where did it happen?
- Who was involved?
- What items or technologies appeared?
- Include names of people, roles, places, technologies, and items.

Generate list of keywords for each chunk

Check the related <facts>. Use names of people or references in the report to identify linked facts. Include their keywords if relevant.

Use file name information to detect additional context — particularly the sector name (e.g. “sektor C1”).
Sector names are composed of a capital letter and a number, e.g., "sektor A3".

Generate a list of keywords that:

- Accurately describe the report.
- Are based on report content, related facts, and the file name.
- Are in Polish.
- Are in the nominative case (e.g. "nauczyciel", "algorytm", not "nauczyciela", "algorytmu").
- Include names of people, places, technologies, and items.
- Remove all duplicates.

If a person appears in the report, and they are mentioned in the facts, include related fact keywords.
Ensure sector name is returned only if it follows the capital-letter-and-number format (e.g. "sektor C1"). Otherwise, ignore.
Be aware that some reports or facts may contain typos or variations of names. Use best judgment to identify connections.

Output:
Return only a dictionary-style output in JSON format.

Each key should be the filename (e.g. "raport_03.txt") and its value a single string of comma-separated keywords in Polish.

Format example:

    <sample_answer>
    {
        "filename 1": "keyword 1, keyword 2, ...",
        "filename 2": "keyword 1, keyword 2, ...",
        "filename 3": "keyword 1, keyword 2, ...",
        "filename x": "keyword 1, keyword 2, ...",
        
    }
    </sample_answer>
    """
    aiMessage = [
        {"role": "system", "content": system_prompt_1},
        {"role": "user", "content": user_prompt}
    ]

    answer = generate_answer("gpt-4.1-mini", aiMessage)
    with open("answer.json", "w", encoding="utf-8") as f:
        f.write(answer)
    answer = json.loads(answer)
    print(answer)
    response = send_response(os.getenv("RAPORT_URL"), "dokumenty", answer)
    print("--------------------------------")
    print("Mission 10 completed")
    print("--------------------------------")
    print("Response:", response)
