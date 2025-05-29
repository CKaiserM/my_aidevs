import os
from dotenv import load_dotenv
from core.send_response import send_response_to_api_db, send_response, send_response_to_centrala
from core.openai_functions import generate_answer
import requests
import json
load_dotenv()

def mission_13():
    """
    Mission 13 processes text data to find connections between people and places.
    
    The function:
    1. Retrieves text data from an API endpoint
    2. Uses GPT to extract people and place names from the text
    3. Queries databases to find connections between people and places
    4. Tracks potential locations where "BARBARA" appears
    5. Sends reports for relevant locations
    
    The function maintains lists of people and places, expanding them by following 
    connections in the data. It specifically tracks places associated with "BARBARA"
    and sends reports for those locations (except KRAKOW).
    """
    print("--------------------------------")
    print("Mission 13 started") 
    print("--------------------------------")

    # Get initial text data
    text = requests.get(os.getenv("CENTRALA_DANE_BARBARA")).text
    user_prompt = str(text)

    # Configure GPT prompt to extract names and places
    system_prompt = """    
        You are a helpful assistant that can answer questions and help with tasks.
        You are given a text with few informations.
        Retrieve all places and people names from the text.
        Return the list of cities and polish names (without surnames), check if names are correct, correct misspellings. 
        Return names in nominative form (e.g. Aleksander, Krakow, etc.) without polish diacritics.
        Return only cities and names without surnames mentioned in the text.
        Remove duplicates from the list.

        <sample_output>
            {
                "places": ["KRAKOW", "WARSZAWA"],
                "people": ["ALEKSANDER", "RAFAL"]
            }
        </sample_output>
    """
    
    # Get initial lists from GPT
    aiMessage = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    answer = json.loads(generate_answer("gpt-4.1-mini", aiMessage))
    print(answer)
    people_list = answer.get("people")
    places_list = answer.get("places")
    potential_places = []

    def remove_polish_diacritics(text):
        """Helper function to remove Polish diacritical marks from text"""
        replacements = {
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z',
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z'
        }
        for polish, latin in replacements.items():
            text = text.replace(polish, latin)
        return text

    def check_person_locations(person):
        """Query database for places associated with a person and update places list"""
        print("--------------------------------")
        people_db = send_response_to_centrala(os.getenv("CENTRALA_PEOPLE"), str(person))
        print("--------------------------------")
        print(people_db)
        print("--------------------------------")
        
        if people_db.get("message") != "[**RESTRICTED DATA**]":
            people_places = people_db.get("message")
            print(people_places)
            cities = remove_polish_diacritics(people_places).split()
            for city in cities:
                if city not in places_list:
                    places_list.append(city)
                    return True
        return False

    def check_place_connections(place, check_new_only=False):
        """Query database for people associated with a place and update lists"""
        if check_new_only and place not in new_places:
            return False

        print("--------------------------------")
        city_db = send_response_to_centrala(os.getenv("CENTRALA_PLACES"), str(place))
        print("--------------------------------")
        print(city_db)
        print("--------------------------------")
        
        if city_db.get("code") != 0:
            print("************************************************")
            print("--------------------------------")
            print("potential_places", potential_places)
            print("--------------------------------")
            print("************************************************")
            return True

        if city_db.get("message") != "[**RESTRICTED DATA**]":
            peoples = city_db.get("message")
            ppl = remove_polish_diacritics(peoples).split()
            found_new = False
            
            for p in ppl:
                if p == "BARBARA":
                    if place not in potential_places:
                        if place != "KRAKOW":
                            response = send_response(os.getenv("RAPORT_URL"), "loop", place)
                            print("--------------------------------")
                            print(response)
                            if response.get("code") == 0:
                                return True
                            print("--------------------------------")
                        potential_places.append(place)
                elif p not in people_list:
                    people_list.append(p)
                    if not check_new_only:
                        found_new = True
                    else:
                        new_people.append(p)
            return found_new
        return False

    # First check initial lists
    for person in people_list:
        check_person_locations(person)

    for place in places_list:
        check_place_connections(place)

    # Then check only newly added items
    while True:
        new_people = []
        new_places = []
        
        # Check new people for places
        for person in people_list:
            if check_person_locations(person):
                new_places.append(places_list[-1])
        
        # Check new places for people
        for place in places_list:
            check_place_connections(place, True)

        # Check all places for BARBARA
        for place in places_list:
            if check_place_connections(place):
                break

        if not new_people and not new_places:
            break

        print("people_list", people_list)
        print("--------------------------------")
        print("potential_places", potential_places)

    print("--------------------------------")
    print("Mission 12 completed")
    print("--------------------------------")
