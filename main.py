from core.models.database import init_db
from core.models.scheduler import Scheduler
from fastapi import APIRouter, FastAPI
from v1.api import api_router

import uvicorn

def create_app():

    root_router = APIRouter()
    app = FastAPI(title="Сервис уведомлений")

    @app.on_event("startup")
    async def start_db():
        await init_db()

    @app.on_event("startup")
    def start_schelduler():
       Scheduler.init_scheduler()

    @root_router.get("/", status_code=200)
    async def index():
        return {"msg": "Hello world"}
    
    app.include_router(root_router)
    app.include_router(api_router)

    return app

if __name__=="__main__":
    uvicorn.run("main:create_app", host="0.0.0.0", port=8888, reload=True)
