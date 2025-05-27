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
from dotenv import load_dotenv
from core.send_response import send_response 
from core.openai_functions import process_image, process_recordings, generate_answer

load_dotenv()

def mission_8(api_key): 
    if not os.path.exists("kategorie.txt"):
        file_list = []
        for filename in os.listdir("pliki_z_fabryki"):
            # Skip facts folder, zip files and files without extension
            if (filename != "facts" and 
                not filename.endswith(".zip") and 
                "." in filename):
                if filename.endswith(".txt"):
                    content = open(os.path.join("pliki_z_fabryki", filename), "r", encoding="utf-8").read()
                elif filename.endswith(".png"):
                    content = process_image(os.path.join("pliki_z_fabryki", filename), "extract text from image", "gpt-4o", "png")
                elif filename.endswith(".mp3"):
                    content = process_recordings(os.path.join("pliki_z_fabryki", filename))
                file_list.append({
                    "name": filename,
                    "content": content
                })
        #print(file_list)
        with open("kategorie.txt", "w", encoding="utf-8") as f:
            f.write(str(file_list))

    with open("kategorie.txt", "r", encoding="utf-8") as f:
        file_list = eval(f.read())
    #print(file_list)
    instructions = """Zwróć tylko odpowiedź, nie pytanie.
Jesteś pomocnym asystentem, który pomoże mi skategoryzować zawartość plików w podanym pliku json w następującym formacie:
{
"name": "plik1.txt",
"content": "zawartość pliku"
}
Otrzymasz listę plików z ich zawartością.
        
Kategoryzacja: Na podstawie tekstu w polu content zdecyduj, czy dany plik zawiera informacje o:
- ludziach: Uwzględniaj tylko notatki zawierające informacje o schwytanych ludziach lub o śladach ich obecności.
- sprzęcie: Usterki hardwarowe (nie software).
Jeśli plik nie pasuje do żadnej z powyższych kategorii, pomiń go. Nie twórz żadnych dodatkowych kategorii. 
Zwróć tylko nazwy plików w formacie JSON, sortując alfabetycznie nazwy plików w każdej kategorii.

pamiętaj o sortowaniu alfabetycznym, nie zmieniaj nazw plików, tylko dodawaj do odpowiedzi (nie zmieniaj nazw i kolejności pól people i hardware):
        {
        "people": ["plik1.txt", "plik2.mp3", "plikN.png"],
        "hardware": ["plik4.txt", "plik5.png", "plik6.mp3"]
        }

        """
    aiModel = "gpt-4.1"
    aiMessage = [{"role": "system", "content": instructions},
        {"role": "user", "content": str(file_list)}]
    answer = generate_answer(aiModel, aiMessage)
    print(answer)
    answer = json.loads(answer)

    response = send_response(os.getenv("RAPORT_URL"), "kategorie", answer)
    print("Response:", response)


