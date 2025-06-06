from dotenv import load_dotenv
#from langfuse.decorators import observe
from langfuse.openai import openai # OpenAI integration
import os
load_dotenv()

#@observe()
def process_instruction(instruction):
    openai.api_key = os.getenv("OPENAI_API_KEY")



    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You are a drone navigation system interpreting movement instructions on a 4x4 grid map.

Input: You will receive natural language instructions describing drone movement in Polish or English.
Output: Return a single word or two-word description of the final location in Polish.

Map Layout (4x4 grid):
[Start][Grass][Tree][House]
[Grass][Windmill][Grass][Grass] 
[Grass][Grass][Rocks][Two trees]
[Mountains][Mountains][Car][Cave]

Rules:
1. Drone always starts at [Start] position (top-left corner)
2. Movement is grid-based (up/down/left/right)
3. Cannot move outside the 4x4 grid boundaries
4. Return only the name of the final location in Polish
5. If you reach a field, you must move to an adjacent field

Example:
Input: "Lecimy kolego teraz na sam dół mapy, a później ile tylko możemy polecimy w prawo. Teraz mała korekta o jedno pole do góry."
Output: "Dwa drzewa"

Location Names in Polish:
- Start -> Start
- Grass -> Trawa
- Tree -> Drzewo
- House -> Dom
- Windmill -> Wiatrak
- Rocks -> Skały
- Two trees -> Dwa drzewa
- Mountains -> Góry
- Car -> Samochód
- Cave -> Jaskinia

Return format: Single word or two words in Polish, no additional text or punctuation."""},
            {"role": "user", "content": f"Instrukcja: {instruction}"}
        ]
    )
    
    return response.choices[0].message.content.strip() 