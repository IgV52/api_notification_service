from httpx import AsyncClient
from tests.conftest import EndPoints

import pytest

@pytest.mark.anyio
async def test_client(client: AsyncClient, routes: EndPoints, db: None) -> None:

    data = {
            "number": 0,
            "phone": 79300488976,
            "code_mobile": 200,
            "tag": "gold",
            "tzone": "UTC",
            }

    resp = await client.post(routes.client, json=data)
    assert resp.status_code == 201
    assert resp.json() == data
    
    resp = await client.post(routes.client, json=data)
    assert resp.status_code == 409
    assert (resp.json())['detail'] == "Клиент с таким номером уже создан"
    
    data["phone"] = 79444488986
    resp = await client.put(f"{routes.client}{0}", json=data)
    assert resp.status_code == 201
    assert resp.json()["phone"] == 79444488986

    resp = await client.delete(f"{routes.client}{0}")
    assert resp.status_code == 200

    resp = await client.delete(f"{routes.client}{0}")
    assert resp.status_code == 404
    assert (resp.json())['detail'] == "Такого клиента нету"

    
@pytest.mark.anyio
async def test_dispath(client: AsyncClient, routes: EndPoints, db: None):

    data = {
        "number": 0,
        "start_sending": "2022-09-23T19:55:44.580000",
        "text": "Первая рассылка",
        "filter": {"tag": "gold", "code_mobile": 200},
        "end_sending": "2022-11-12T19:55:44.580000",
        }

    resp = await client.post(routes.dispath, json=data)
    assert resp.status_code == 201
    assert resp.json() == data

    resp = await client.post(routes.dispath, json=data)
    assert resp.status_code == 409
    assert (resp.json())['detail'] == "Рассылка с таким номером уже создана"
    
    data["text"] = "Вторая рассылка"
    resp = await client.put(f"{routes.dispath}{0}", json=data)
    assert resp.status_code == 201
    assert resp.json()["text"] == "Вторая рассылка"

    resp = await client.delete(f"{routes.dispath}{0}")
    assert resp.status_code == 200

    resp = await client.delete(f"{routes.dispath}{0}")
    assert resp.status_code == 404
    assert (resp.json())['detail'] == "Такой рассылки нету"

@pytest.mark.anyio
async def test_stats(client: AsyncClient, routes: EndPoints, db: None):
    resp = await client.get(routes.stats)
    assert resp.status_code == 404
    assert resp.json()['detail'] == "Данных нету"

    resp = await client.get(f"{routes.stats}{0}")
    assert resp.status_code == 404
    assert resp.json()['detail'] == "Данных нету"


