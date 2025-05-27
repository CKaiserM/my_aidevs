"""
    This script performs semantic search using vector embeddings and Qdrant vector database.
    
    The process involves:
    1. Creating text embeddings using OpenAI's embedding model
    2. Storing embeddings in a Qdrant collection with metadata
    3. Performing semantic search on the collection
    
    Key components:
    - OpenAI embeddings API for converting text to vectors
    - Qdrant vector database for storing and searching embeddings
    - Collection configuration with cosine distance metric
    - Search functionality to find semantically similar content
    
    The script specifically searches for mentions of weapon prototype theft
    in dated reports and returns the relevant report date.
    
    Returns:
        str: Filename of the report containing weapon theft information
        
    Environment variables required:
        - RAPORT_URL: URL endpoint for submitting the answer
"""
import openai
import os
import qdrant_client
from dotenv import load_dotenv
from qdrant_client.models import VectorParams, Distance, PointStruct
from send_response import send_response
load_dotenv()

def mission_11():   
    openai_client = openai.Client(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    client = qdrant_client.QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API")
    )   

    collection_name = "weapons_tests_collection"
    embedding_model = "text-embedding-3-small"
    # Check if collection exists
    collections = client.get_collections()
    if collection_name not in [collection.name for collection in collections.collections]:
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

        result = openai_client.embeddings.create(
            input=texts,
            model=embedding_model
        )

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
        client.create_collection(
            collection_name,
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE,
            ),
        )

        # Insert points into collection
        client.upsert(collection_name, points)
    else:
        print("Collection already exists")
    
    question = "W raporcie, z którego dnia znajduje się wzmianka o kradzieży prototypu broni?"
    response = client.search(
    collection_name=collection_name,
    query_vector=openai_client.embeddings.create(
        input=[question],
        model=embedding_model,
        )
        .data[0]
        .embedding,
    )
    answer = response[0].payload["filename"]
    print(answer)
    raport = send_response(os.getenv("RAPORT_URL"), "wektory", str(answer))
    print("--------------------------------")
    print("Mission 10 completed")
    print("--------------------------------")
    print("Response:", raport)     

