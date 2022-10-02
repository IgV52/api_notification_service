from fastapi import APIRouter, HTTPException
from core.shemas.client import Client, ClientOut, ClientUpdate

router = APIRouter()

@router.post("/", status_code=201, response_model=ClientOut)
async def post_client(client: Client):
    client_search = await Client.by_number(client.number)
    if client_search:
        raise HTTPException(status_code=409, 
                            detail="Клиент с таким номером уже создан")
    await client.create()
    return client

@router.put("/{id}", status_code=201, response_model=ClientOut)
async def update_client(id: int, update: ClientUpdate):
    req = {k: v for k, v in update.dict().items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in req.items()
    }}
    client = await Client.by_number(id)
    if not client:
        raise HTTPException(status_code=404, 
                            detail="Такого клиента нету")
    await client.update(update_query)
    return client

@router.delete("/{id}", response_description="Клиент удален", status_code=200)
async def delete_client(id: int) -> dict:
    client = await Client.by_number(id)
    if not client:
        raise HTTPException(
            status_code=404,
            detail="Такого клиента нету"
        )

    await client.delete()
    return {"message": "Client deleted successfully"}