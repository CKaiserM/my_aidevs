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

def mission_9(api_key): 
    response = requests.get(os.getenv("DRAFT"))
    # Convert HTML to Markdown
    # Create directory for media files if it doesn't exist
    if not os.path.exists("media"):
        os.makedirs("media")
    if not os.path.exists("draft.md"):
        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Download and process images
        for img in soup.find_all("img"):
            img_url = img.get("src")
            if img_url:
                if not img_url.startswith("http"):
                    img_url = os.getenv("DRAFT").replace("arxiv-draft.html", "") + img_url
                
                img_name = os.path.basename(img_url)
                description_path = os.path.join("media", f"{img_name}.md")
                
                if not os.path.exists(description_path):
                    print("processing image: ", img_url)
                    # Get image description from OpenAI
                    img_description = process_image_from_url(img_url, "Describe Image in detail. Return only the description of the image, nothing else. Return text in polish language.", "gpt-4.1")
                    
                    # Save description to markdown file
                    with open(description_path, "w", encoding="utf-8") as f:
                        f.write(img_description)
                else:
                    # Read existing description
                    with open(description_path, "r", encoding="utf-8") as f:
                        img_description = f.read()
                
                # Replace image tag with description
                img.replace_with(f"[Opis obrazu: {img_description}]")

        # Download and process audio files
        for audio in soup.find_all("audio"):
            print("audio found")
            print("audio: ", audio)
            audio_url = audio.source.get("src")
            print("--------------------------------")
            print("audio url: ", audio_url)
            print("--------------------------------")
            if audio_url:
                audio_url = os.getenv("DRAFT").replace("arxiv-draft.html", "") + audio_url
                audio_name = os.path.basename(audio_url)
                audio_path = os.path.join("media", audio_name)
                transcription_path = os.path.join("media", f"{audio_name}.md")

                if not os.path.exists(transcription_path):
                    # Download audio file if not exists
                    if not os.path.exists(audio_path):
                        audio_response = requests.get(audio_url)
                        with open(audio_path, "wb") as f:
                            print("downloading audio: ", audio_url)
                            f.write(audio_response.content)
                    
                    # Get audio transcription from local file
                    audio_transcription = process_recordings(audio_path)
                    
                    # Save transcription to markdown file
                    with open(transcription_path, "w", encoding="utf-8") as f:
                        f.write(audio_transcription)
                else:
                    # Read existing transcription
                    with open(transcription_path, "r", encoding="utf-8") as f:
                        audio_transcription = f.read()

                # Replace audio tag with transcription
            audio.replace_with(f"[Opis dźwięku: {audio_transcription}]")

        response._content = str(soup).encode()


        h = html2text.HTML2Text()
        
        h.ignore_links = False
        h.body_width = 0
        markdown_text = h.handle(response.text)

        with open("draft.md", "w", encoding="utf-8") as f:
            f.write(markdown_text)

    with open("draft.md", "r", encoding="utf-8") as f:
        draft = f.read()

    questions_response = requests.get(os.getenv("QUESTIONS"))  
    questions = questions_response.text
    print("--------------------------------")
    print("Questions:", questions)
    print("--------------------------------")
    prompt = """    
    You are a helpful assistant that can answer questions and help with tasks.
    You are given a markdown of a paper.
    Read and transform the markdown to answer only the following questions with short answers in 1 sentence.
    
    <Questions>
    01=jakiego owocu użyto podczas pierwszej próby transmisji materii w czasie?
    02=Na rynku którego miasta wykonano testową fotografię użytą podczas testu przesyłania multimediów?
    03=Co Bomba chciał znaleźć w Grudziądzu?
    04=Resztki jakiego dania zostały pozostawione przez Rafała?
    05=Od czego pochodzą litery BNW w nazwie nowego modelu językowego?
    </Questions>
    
    Do not change the questions and their numbers, just answer them.
    
    return exactly same number of answers as questions in json format with numbers as keys, answer only those questions which are in the <Questions> tag

    <sample_answer>
    {
        "01": "krótka odpowiedź w 1 zdaniu",
        "02": "krótka odpowiedź w 1 zdaniu",
        "03": "krótka odpowiedź w 1 zdaniu",
        "04": "krótka odpowiedź w 1 zdaniu",
        "05": "krótka odpowiedź w 1 zdaniu"
    }
    </sample_answer>
    """
    aiMessage = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": draft}
    ]

    answer = generate_answer("gpt-4.1", aiMessage)
    with open("answer.json", "w", encoding="utf-8") as f:
        f.write(answer)
    answer = json.loads(answer)
    response = send_response(os.getenv("RAPORT_URL"), "arxiv", answer)
    print("--------------------------------")
    print("Mission 9 completed")
    print("--------------------------------")
    print("Response:", response)
