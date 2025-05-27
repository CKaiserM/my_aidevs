"""
Qdrant Functions Module

This module provides functionality for interacting with the Qdrant vector database
and OpenAI embeddings. It handles collection management, vector storage, and similarity search.

Dependencies:
    - qdrant_client: For connecting to and managing Qdrant vector database
    - os: For environment variable access
    - dotenv: For loading environment variables
    - langfuse.openai: For OpenAI API integration
    - langfuse.decorators: For observability decorators

The module uses environment variables for configuration:
    - QDRANT_URL: URL of the Qdrant server
    - QDRANT_API: API key for Qdrant authentication
    - OPENAI_API_KEY: OpenAI API key for embeddings
"""

import qdrant_client
from qdrant_client.models import VectorParams, Distance, PointStruct
import os
from dotenv import load_dotenv
from langfuse.openai import openai
from langfuse.decorators import observe
load_dotenv()

@observe()
def openai_client():
    return openai.Client(
        api_key=os.getenv("OPENAI_API_KEY")
    )

client = qdrant_client.QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API")
    )  

model_dimensions = {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "text-embedding-ada-002": 1536
    }

def check_if_collection_exists(collection_name):
    # Check if collection exists
    collections = client.get_collections()
    if collection_name not in [collection.name for collection in collections.collections]:
        return False
    return True

def create_collection(collection_name, embedding_model):
    client.create_collection(
        collection_name,
        vectors_config=VectorParams(
            size=model_dimensions.get(embedding_model),
            distance=Distance.COSINE,
        ),
    )
    
def insert_points_into_collection(collection_name, points):
    client.upsert(
        collection_name=collection_name,
        points=points
    )

def search_collection(collection_name, embedding_model, question):
    response = client.search(
    collection_name=collection_name,
    query_vector=openai_client().embeddings.create(
        input=[question],
        model=embedding_model,
        )
        .data[0]
        .embedding,
    )
    return response