from datetime import datetime
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from v1.helpers.qdrant_client import create_embeddings
from fastapi.exceptions import HTTPException
import uuid
from uuid import uuid4
import os
import PyPDF2
from langchain.text_splitter import TokenTextSplitter


async def text_splitter(text: str):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5, chunk_overlap=0)
        input_chunks = text_splitter.split_text(text)
        print(input_chunks)
        final_chunks = []
        # for i, item in enumerate(input_chunks):
        # print(f"\nChunk {i + 1}:\n")
        # print(item)
        final_chunks.extend(
            [
                {
                    "id": str(uuid4()),
                    "text": input_chunks[i],
                    "chunk": i,
                    "embeds": create_embeddings(input_chunks[i]),
                }
                for i in range(len(input_chunks))
            ]
        )
        print(final_chunks)
        return final_chunks
    except Exception as e:
        print(e)
        error_message = str(e)
        raise HTTPException(status_code=400, detail=error_message)


async def pdf_text_splitter(text: str):
    try:
        text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=0)
        input_chunks = text_splitter.split_text(text)
        final_chunks = []
        final_chunks.extend(
            [
                {
                    "id": str(uuid4()),
                    "text": input_chunks[i],
                    "chunk": i,
                    "embeds": create_embeddings(input_chunks[i]),
                }
                for i in range(len(input_chunks))
            ]
        )
        return final_chunks
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"{str(e)}")


async def text_loader(text: str):
    try:
        if not text:
            raise HTTPException(status_code=400, detail="Text should not be empty.")
        ROOT_DIR = os.path.abspath(os.curdir)
        temp_folder = os.path.join(ROOT_DIR, "text_vector")
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        if os.path.exists(temp_folder) and os.path.isdir(temp_folder):
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{str(uuid.uuid4())}__{current_time}.txt"
            file_path = f"{temp_folder}\{file_name}"

            if not os.path.exists(file_path) and not os.path.isfile(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text)
            loader = TextLoader(file_path, autodetect_encoding=True)
            documents = loader.load()

            # removing file path
            if os.path.exists(file_path) and os.path.isfile(file_path):
                os.remove(file_path)

            final_chunks = await text_splitter(documents)
            return final_chunks

        else:
            return []
    except Exception as e:
        print(e)
        return []


async def pdf_loader(file):
    try:
        print(file.filename)
        ROOT_DIR = os.path.abspath(os.curdir)
        temp_folder = os.path.join(ROOT_DIR, "pdf_vector")
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        file_path = os.path.join(temp_folder, file.filename)
        if not os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(await file.read())

        # pdf read
        reader = PyPDF2.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        print(text)

        # removing file path
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)

        # Text Chunking
        final_chunks = await pdf_text_splitter(text=text)
        return final_chunks
    except Exception as e:
        print(e)
        return []
