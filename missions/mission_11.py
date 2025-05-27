"""
Mission 11 Module

This module searches through dated weapon test reports to identify potential theft incidents.
It uses semantic search powered by vector embeddings to analyze report contents.

The module:
1. Processes text files from weapons_tests/do-not-share directory
2. Converts report dates from DDMMYYYY to YYYY-MM-DD format
3. Creates vector embeddings of report contents using OpenAI's API
4. Stores embeddings and metadata in Qdrant vector database
5. Performs semantic search to find mentions of weapon prototype theft

Dependencies:
    - openai: For generating text embeddings
    - qdrant_client: For vector database operations
    - os: For file operations
    - dotenv: For loading environment variables
    - core.send_response: For submitting results
    - core.openai_functions: For embedding generation
    - core.qdrant_functions: For Qdrant database operations

Returns:
    str: Date of the report containing weapon theft information in YYYY-MM-DD format

Environment variables:
    - RAPORT_URL: Endpoint for submitting the identified report date
    - OPENAI_API_KEY: For OpenAI API access
    - QDRANT_URL: Qdrant server URL
    - QDRANT_API: Qdrant API key
"""
import openai
import os
import qdrant_client
from dotenv import load_dotenv
from qdrant_client.models import VectorParams, Distance, PointStruct
from core.send_response import send_response
from core.openai_functions import generate_embeddings
from core.qdrant_functions import check_if_collection_exists, create_collection, insert_points_into_collection, search_collection    

load_dotenv()

def mission_11():   

    collection_name = "weapons_tests_collection"
    # Map models to their vector sizes

    embedding_model = "text-embedding-3-small"
    # Check if collection exists
    if not check_if_collection_exists(collection_name):
        # Read files from directory
        texts = []
        filenames = []
        base_path = "pliki_z_fabryki/weapons_tests/do-not-share"
        
        for filename in os.listdir(base_path):
            if filename.endswith(".txt"):
                with open(os.path.join(base_path, filename), "r", encoding="utf-8") as f:
                    text = f.read()
                    texts.append(text)
                    # Convert filename from DDMMYYYY to YYYY-MM-DD format
                    date = filename.split(".")[0]  # Get filename without extension
                    date = date.replace("_", "-")
                    filenames.append(date)

        # Create embeddings

        result = generate_embeddings(texts, embedding_model)

        # Convert to qdrant points with filename metadata
        points = [
            PointStruct(
                id=idx,
                vector=data.embedding,
                payload={
                    "text": text,
                    "filename": filename
                },
            )
            for idx, (data, text, filename) in enumerate(zip(result.data, texts, filenames))
        ]

        # Create and configure collection
        create_collection(collection_name, embedding_model)

        insert_points_into_collection(collection_name, points)
    else:
        print("Collection already exists")
    
    question = "W raporcie, z którego dnia znajduje się wzmianka o kradzieży prototypu broni?"
    response = search_collection(collection_name, embedding_model, question)
    answer = response[0].payload["filename"]
    print(answer)
    raport = send_response(os.getenv("RAPORT_URL"), "wektory", str(answer))
    print("--------------------------------")
    print("Mission 11 completed")
    print("--------------------------------")
    print("Response:", raport)     

