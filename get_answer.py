from langfuse.decorators import observe
from langfuse.openai import openai # OpenAI integration
import os

# Get answer from GPT-4.1 Nano

@observe()
def generate_answer(aiModel, aiMessage):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    answer = openai.chat.completions.create(
        model=aiModel,
        messages=aiMessage
    ).choices[0].message.content
    return answer

# Process audio files and return transcription
@observe()
def process_recordings(recording):
    
    audio_file= open(recording, "rb")

    transcription = openai.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

    return transcription.text