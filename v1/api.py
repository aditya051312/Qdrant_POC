from v1.routers.knoledgebase import knowledgebase_router
from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(knowledgebase_router, tags=["Collection Router"])
