import json
import os
import csv  
def save_data_to_file(data, filename, directory, extension):
    """
    Saves data to a JSON file in a specified directory.
    
    Args:
        data: Data to save (must be JSON-serializable)
        filename: Name of file to save to
        directory: Directory to save file in
        extension: File extension to use
    """
    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    # Check if file exists
    filepath = os.path.join(directory, filename + extension)
    if os.path.exists(filepath):
        response = input(f"File {filepath} already exists. Override? (y/n): ")
        if response.lower() != 'y':
            print("File not saved")
            return
            
    # Save data to file 
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filepath}")

def save_json_as_csv(json, csv_file):
    """
    Converts a JSON string to CSV format and saves it.
    
    Args:
        json_str: JSON string to convert
        csv_file: Path to output CSV file
    """
    # Parse JSON string
    data = json
    
    # Extract data - assumes JSON contains a list of dictionaries
    if isinstance(data, dict):
        # If data is wrapped in a dict (like {"reply": [...]}), get the first list
        for value in data.values():
            if isinstance(value, list):
                records = value
                break
    elif isinstance(data, list):
        records = data
    else:
        raise ValueError("JSON must contain a list of records")
        
    if not records:
        raise ValueError("No records found in JSON")
        
    # Get field names from first record
    fieldnames = records[0].keys()
    
    # Write to CSV with UTF-8 encoding
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    
    print(f"Converted JSON string to CSV format at {csv_file}")

def save_data_to_csv(data, directory, filename, extension):
    """
    Saves data to a CSV file.

    Args:
        data: Data to save (must be JSON-serializable)
        directory: Directory to save file in
        filename: Name of file to save to
        extension: File extension to use
    """
    # Create directory if it doesn't exist  
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    # Check if file exists
    filepath = os.path.join(directory, filename + extension)
    if os.path.exists(filepath):    
        response = input(f"File {filepath} already exists. Override? (y/n): ")
        if response.lower() != 'y':
            print("File not saved")
            return
            
    # Save data to file 
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data.keys())
        writer.writerows(data.values())
        
    print(f"Data saved to {filepath}")  


