from qdrant_client import models, QdrantClient
import openai
from typing import List
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

# Qdrant API keys and endpoint
qdrant_client = QdrantClient(
    api_key=QDRANT_API_KEY,
    url=QDRANT_URL,
    timeout=100,
)


openai.api_key = OPENAI_API_KEY


# Embedding Model
embedding_model = "text-embedding-ada-002"


# Create Qdrant collection
collection_info = qdrant_client.collection_exists(collection_name="test_1")

if not collection_info:
    qdrant_client.recreate_collection(
        collection_name="test_1",
        vectors_config=models.VectorParams(
            size=1536,
            distance=models.Distance.COSINE,
        ),
    )


# Creating Embedding
def create_embeddings(texts):
    res = openai.Embedding.create(
        input=texts, engine=embedding_model, api_key=OPENAI_API_KEY
    )
    for record in res["data"]:
        embeds = record["embedding"]
    return embeds


# Qdrant Collection creation
async def create_collection(final_chunks: List[str]):
    try:
        qdrant_client.upload_records(
            collection_name="test_1",
            records=[
                models.Record(id=key["id"], vector=key["embeds"], payload=key)
                for id, key in enumerate(final_chunks)
            ],
        )
        return True
    except Exception as e:
        print(e)
        error_message = str(e)
        raise HTTPException(status_code=400, detail=error_message)
