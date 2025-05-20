"""
Mission 6 Module        

This module handles the sixth mission which involves:
1. Processing an image
2. Storing results for later analysis

Dependencies:
    - os: For file and directory operations
    - dotenv: For loading environment variables
    - get_answer: For processing the image
"""

import requests
import re
import os
from dotenv import load_dotenv
from get_answer import process_image

load_dotenv()

def mission_6(api_key):
    
    prompt = """Obraz zawiera cztery fragmenty mapy. W trzech wierszach zawiera 4 fragmenty mapy,
pierwszy wiersz od góry zawiera dwa fragmenty mapy (po lewej i prawej stronie), drugi (środek obrazu) jeden fragment mapy, trzeci wiersz (dół obrazu) zawiera jeden fragment mapy.
Pamiętaj, aby w analizie pominąć symbol w lewym dolnym rogu. Pamiętaj, że jeden z czterech fragmentów mapy może z innego miasta niż pozostałe.
Dla każdego fragmentu zidentyfikuj nazwy ulic, charakterystyczne obiekty na przykład: cmentarze, kościoły, szkoły, sklepy i układ urbanistyczny.
Sprawdź, czy wykryte nazwy obiektów są poprawne. Pomiń numery dróg. Sprawdź czy nazwy sklepów są poprawne i istnieją, jeśli nie to zastąp istniejącą nazwą. Szukane miasto ma spichlerze i twierdze.
Rozpoznaj lokalizacje o takim samym układzie ulic i obiektów, z twierdzą i spichlerzami. Upewnij się, że lokalizacje, które rozpoznajesz na mapie, na pewno znajdują się w mieście, które zamierzasz zwrócić jako odpowiedź.
Jakie miasta znajdują się na obrazie? Które fragmenty mapy pochodzą z tego samego miasta? Zwróć tylko nazwę miasta."""
    
    answer = process_image("mapa/mapa.jpg", prompt)
    print("--------------------------------")
    print("Answer:", answer)
    print("--------------------------------")

    

