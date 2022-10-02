from fastapi import APIRouter
from v1.endpoints import client, dispath, stats

api_router = APIRouter()

api_router.include_router(client.router, prefix="/client", tags=["client"])
api_router.include_router(dispath.router, prefix="/dispath", tags=["dispath"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])