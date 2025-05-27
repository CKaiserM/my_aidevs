"""
This module provides functions to generate answers from GPT-4.1 Nano and process audio files.

Functions:
    generate_answer(aiModel, aiMessage): Generates an answer from GPT-4.1 Nano.
    process_recordings(recording): Processes audio files and returns their transcriptions.  
    process_image(image_path, prompt): Processes images and returns their answers.

"""
from langfuse.decorators import observe
from langfuse.openai import openai # OpenAI integration
import os
import base64
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


def process_image_from_url(image_url, prompt, model):
    response = openai.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                },
            ],
        }],
    )

    return response.choices[0].message.content

@observe()
# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def process_image(image_path, prompt, model, extension):

    # Getting the Base64 string
    base64_image = encode_image(image_path)


    response = openai.responses.create(
        model=model,
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": prompt },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/{extension};base64,{base64_image}",
                    },
                ],
            }
        ],
    )

    return response.output_text

@observe()
def generate_image(prompt):
    result = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024"
    )

    return result.data[0].url

@observe()
def generate_embeddings(text, model):
    result = openai.embeddings.create(
        input=text,
        model=model
    )

    return result