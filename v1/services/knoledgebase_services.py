from fastapi.exceptions import HTTPException
from v1.schema.pydentic_models import collection_req_text
from v1.helpers.text_loader import text_loader, pdf_loader
from v1.helpers.qdrant_client import create_collection


async def knowledgebase_text_processor(request: collection_req_text):
    try:
        final_chunks = await text_loader(request.content)
        result = await create_collection(final_chunks=final_chunks)
        if result:
            return True

    except Exception as e:
        error_message = f"{str(e)}"
        print(f"{str(e)}")
        raise HTTPException(status_code=400, detail=error_message)


async def knowledgebase_pdf_processor(file):
    try:
        final_chunks = await pdf_loader(file=file)
        result = await create_collection(final_chunks=final_chunks)
        if result:
            return True
    except Exception as e:
        error_message = f"{str(e)}"
        print(f"{str(e)}")
        raise HTTPException(status_code=400, detail=error_message)
