from fastapi import APIRouter, HTTPException, UploadFile, File
from v1.schema.pydentic_models import collection_req_text, query_req
from v1.services.knoledgebase_services import (
    knowledgebase_text_processor,
    knowledgebase_pdf_processor,
)
from v1.helpers.qdrant_client import create_embeddings
from v1.helpers.qdrant_client import qdrant_client
from qdrant_client import QdrantClient

knowledgebase_router = APIRouter(prefix="/knowledgebase")


@knowledgebase_router.post("/text")
async def create_text_collection(request: collection_req_text):
    try:
        result = await knowledgebase_text_processor(request=request)
        if result:
            return {
                "message": "collection created successfully.",
            }
        raise HTTPException(status_code=400, detail="somethimg wrong")
    except Exception as e:
        print(e)
        error_message = str(e)
        raise HTTPException(status_code=400, detail=error_message)


@knowledgebase_router.post("/pdf")
async def create_pdf_collection(file: UploadFile = File()):
    try:
        result = await knowledgebase_pdf_processor(file=file)
        if result:
            return {
                "message": "collection created successfully.",
            }
        raise HTTPException(status_code=400, detail="somethimg wrong")
    except Exception as e:
        print(e)
        error_message = str(e)
        raise HTTPException(status_code=400, detail=error_message)


@knowledgebase_router.post("/query")
async def question_answer(text: str):
    try:
        search_result = qdrant_client.search(
            collection_name="test_1", query_vector=create_embeddings(text), limit=3
        )
        answer = search_result[0].payload["text"]
        return {"query": text, "answer": answer}
    except Exception as e:
        print(e)
        error_message = str(e)
        raise HTTPException(status_code=400, detail=error_message)
