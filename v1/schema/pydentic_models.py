from pydantic import BaseModel


class collection_req_text(BaseModel):
    content: str


class query_req(BaseModel):
    content: str
