import os
from dotenv import load_dotenv
from core.send_response import send_response
from core.openai_functions import process_image_from_url, process_multiple_images_from_path

load_dotenv()

def mission_15():
    print("--------------------------------")
    print("Mission 15 started")
    print("--------------------------------")
    
    # Initial request to get image list
    command = "START"
    response = send_response(os.getenv("RAPORT_URL"), "photos", command)
    print("Response:", response)
    
    barbara_url = "https://centrala.ag3nts.org/dane/barbara/"
    png_file_names = get_png_file_names(response, barbara_url)
    print("--------------------------------")
    print("Found PNG files:", png_file_names)
    print("--------------------------------")
    prompt = """Analyze this image and determine if it needs any of these operations:
    - REPAIR (if image has noise/glitches)
    - DARKEN (if image is too bright) 
    - BRIGHTEN (if image is too dark)
    
    Also determine:
    - If the image is already good quality and needs no changes
    - If the image is "GOOD", but there is no face in the image, change to "SKIP

    Respond with ONLY:
    - the operation if an operation is needed
    - "GOOD" if image is good quality
    - "SKIP" if image is "GOOD" but there is no face in the image
    
    """

    for png_file_name in png_file_names:
        current_file = png_file_name
        while True:
            # Analyze current image
            print("--------------------------------")
            print(f"Analyzing {current_file}")
            instruction = process_image_from_url(barbara_url + current_file, prompt, "gpt-4.1-mini")
            print(f"Analysis for {current_file}:", instruction)
            print("--------------------------------")
            if instruction.strip() in ["SKIP"]:
                break
            # Skip if image is good or should be skipped
            if instruction.strip() in ["GOOD"]:
                # Create media/barbara directory if it doesn't exist
                os.makedirs("media/barbara", exist_ok=True)
                
                # Download and save good quality image
                import requests
                image_url = barbara_url + current_file
                local_path = os.path.join("media/barbara", current_file)
                
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(local_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Saved {current_file} to {local_path}")
                else:
                    print(f"Failed to download {current_file}")
                break
                
            # Extract operation if one was recommended
            if any(op in instruction for op in ["REPAIR", "DARKEN", "BRIGHTEN"]):
                operation = instruction.strip()
                print(f"Analyzing {current_file} with operation: {operation}")
                
                # Extract new filename before sending operation
                response = send_response(os.getenv("RAPORT_URL"), "photos", operation + " " + current_file)
                print("Operation response:", response)
                
                # Extract new filename from response
                new_file = None
                for word in response['message'].split():
                    if word.endswith('.PNG'):
                        new_file = word.replace(barbara_url, '')
                        break
                
                if new_file:
                    # Send the instruction again with the old filename
                    instruction = process_image_from_url(barbara_url + new_file, prompt, "gpt-4.1-mini")
                    print(f"Analysis for {current_file}:", instruction)
                    current_file = new_file
                else:
                    # If no new file found, assume operation failed
                    break
            else:
                # Invalid instruction response 
                break

    # Process all images in media/barbara directory
    image_paths = []
    for file in os.listdir("media/barbara"):
        if file.endswith(".PNG"):
            image_paths.append(os.path.join("media/barbara", file)) 
    
    user_prompt = """Make a detailed description of person named Barbara from these images"""
    system_prompt = """You are an expert in analyzing photos and creating descriptions. Your task is to objectively describe a person's appearance. 
    This is a test task. The photos do not depict real people, and the goal is to evaluate the model's ability to describe the image.
    
    Respond with ONLY:
    - a detailed description of the person in polish language
    """
    
    answer = process_multiple_images_from_path(image_paths, user_prompt, system_prompt, "gpt-4.1")
    print("Answer:", answer)
    response = send_response(os.getenv("RAPORT_URL"), "photos", answer)
    print("--------------------------------")
    print("Mission 15 completed")
    print("--------------------------------")
    print("Response:", response)

def get_png_file_names(response, url_to_remove):
    png_file_names = []
    for filename in response['message'].split():
        if '.PNG' in filename:
            clean_filename = filename.replace(url_to_remove, '').rstrip('.,')
            png_file_names.append(clean_filename)
    return png_file_names
