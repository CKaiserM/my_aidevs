"""
Mission 6 Module

This module processes a map image to identify city locations. It analyzes multiple map fragments
to determine street names, landmarks, and urban layouts to identify which city the map represents.

The module looks specifically for:
- Street names and layouts
- Notable landmarks like churches, cemeteries, schools, stores
- Urban features like granaries and fortresses
- Consistency between map fragments to verify city identification

Functions:
    mission_6(api_key): Processes a map image and returns the identified city name

Dependencies:
    - requests: For making HTTP requests
    - re: For regular expressions
    - os: For file operations
    - dotenv: For loading environment variables
    - get_answer: For image processing using AI
"""

import requests
import re
import os
from dotenv import load_dotenv
from core.openai_functions import process_image

load_dotenv()

def mission_6(api_key):
    
    prompt = """Obraz zawiera cztery fragmenty mapy. W trzech wierszach zawiera 4 fragmenty mapy,
pierwszy wiersz od góry zawiera dwa fragmenty mapy (po lewej i prawej stronie), drugi (środek obrazu) jeden fragment mapy, trzeci wiersz (dół obrazu) zawiera jeden fragment mapy.
Pamiętaj, aby w analizie pominąć symbol w lewym dolnym rogu. Pamiętaj, że jeden z czterech fragmentów mapy może z innego miasta niż pozostałe.
Dla każdego fragmentu zidentyfikuj nazwy ulic, charakterystyczne obiekty na przykład: cmentarze, kościoły, szkoły, sklepy i układ urbanistyczny.
Sprawdź, czy wykryte nazwy obiektów są poprawne. Pomiń numery dróg. Sprawdź czy nazwy sklepów są poprawne i istnieją, jeśli nie to zastąp istniejącą nazwą. Szukane miasto ma spichlerze i twierdze.
Rozpoznaj lokalizacje o takim samym układzie ulic i obiektów, z twierdzą i spichlerzami. Upewnij się, że lokalizacje, które rozpoznajesz na mapie, na pewno znajdują się w mieście, które zamierzasz zwrócić jako odpowiedź.
Jakie miasta znajdują się na obrazie? Które fragmenty mapy pochodzą z tego samego miasta? Zwróć tylko nazwę miasta."""
    
    answer = process_image("mapa/mapa.jpg", prompt, "gpt-4.1", "jpeg")
    print("--------------------------------")
    print("Answer:", answer)
    print("--------------------------------")

    

