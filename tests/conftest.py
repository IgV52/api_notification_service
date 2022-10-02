from beanie import init_beanie
from core.models.scheduler import Scheduler
from core.shemas.client import Client
from core.shemas.dispath import Dispath
from core.shemas.msg import Msg
from dataclasses import dataclass
from httpx import AsyncClient
from main import create_app
from typing import Iterator

import motor.motor_asyncio
import pytest
import settings

@dataclass(slots=True, frozen=True)
class EndPoints:
    client: str
    dispath: str
    stats: str

@pytest.fixture()
def routes() -> EndPoints:
    return EndPoints(
                    client="/client/", 
                    dispath="/dispath/",  
                    stats="/stats/",
                    )

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

async def clear_database() -> None:
    await Client.delete_all()
    await Dispath.delete_all()
    await Msg.delete_all()

@pytest.fixture(scope="session")
async def db() -> None:
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)
    await init_beanie(database=client.TEST_DB, document_models=[Client, Dispath, Msg])

@pytest.fixture(scope="session")
async def client() -> Iterator[AsyncClient]:
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as _client:
        try:
            Scheduler.init_scheduler_test()
            yield _client
        except Exception as exc:  # pylint: disable=broad-except
            print(exc)
        finally:
            await clear_database()
       