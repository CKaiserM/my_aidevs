import os
from dotenv import load_dotenv
from core.send_response import send_response
from core.openai_functions import generate_answer

load_dotenv()

def mission_18():
    response = send_response(os.getenv("RAPORT_URL"), "webhook", "https://aidevs.mcichockikaiser.com/api/process")
    print("Response:", response)