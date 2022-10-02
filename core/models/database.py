from beanie import init_beanie
from core.shemas.client import Client
from core.shemas.dispath import Dispath
from core.shemas.msg import Msg

import motor.motor_asyncio
import settings

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)
    await init_beanie(database=client.SERVICE_MSG, document_models=[Client, Dispath, Msg])