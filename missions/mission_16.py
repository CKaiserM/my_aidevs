import os
from dotenv import load_dotenv
from core.send_response import send_response
from core.openai_functions import generate_answer

load_dotenv()

def mission_16():
    print("--------------------------------")
    print("Mission 16 started")
    print("--------------------------------")

    # Read the correct.txt file and create JSON format
    # Process correct.txt
    correct_file_path = os.path.join("fine_tune", "correct.txt")
    output_path = os.path.join("fine_tune", "file-data.jsonl")
    verify_file_path = os.path.join("fine_tune", "verify.txt")
    try:

            
        with open(output_path, 'w') as jsonl_file:
            # Process correct.txt
            with open(correct_file_path, 'r') as file:
                for line in file:
                    json_entry = {
                        "messages": [
                            {
                                "role": "system",
                                "content": "validate data"
                            },
                            {
                                "role": "user", 
                                "content": line.strip()
                            },
                            {
                                "role": "assistant",
                                "content": "1"
                            }
                        ]
                    }
                    import json
                    jsonl_file.write(json.dumps(json_entry) + '\n')

            # Process incorrect.txt
            incorrect_file_path = os.path.join("fine_tune", "incorect.txt")
            with open(incorrect_file_path, 'r') as file:
                for line in file:
                    json_entry = {
                        "messages": [
                            {
                                "role": "system",
                                "content": "validate data"
                            },
                            {
                                "role": "user", 
                                "content": line.strip()
                            },
                            {
                                "role": "assistant",
                                "content": "0"
                            }
                        ]
                    }
                    jsonl_file.write(json.dumps(json_entry) + '\n')
                    
        print(f"Created JSONL file at: {output_path}")
        
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error processing files: {str(e)}")

    answer_list = []

    with open(verify_file_path, 'r') as verify_file:
        for line in verify_file:
            json_entry = [
                        {
                            "role": "system",
                            "content": "validate data"
                        },
                        {
                            "role": "user",
                            "content": line.strip()
                        },
                        
                    ]
                
            aiModel = "ft:gpt-4.1-mini-2025-04-14:personal:ai-devs:BeDwUL6v"
            answer = generate_answer(aiModel, json_entry)
            print(answer)
            if answer == "1":
                answer_list.append(line.strip()[:2])
        print(answer_list)

    response = send_response(os.getenv("RAPORT_URL"), "research", answer_list)
    print("Response:", response)

    # Initial request to get image list
    #command = "START"
    #response = send_response(os.getenv("RAPORT_URL"), "photos", command)
    #print("Response:", response)
