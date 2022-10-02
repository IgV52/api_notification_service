from fastapi import APIRouter, HTTPException
from core.shemas.dispath import Dispath, DispathOut, DispathUpdate
from core.models.scheduler import Scheduler
from v1.utils.dispath import func

router = APIRouter()

@router.post("/", status_code=201, response_model=DispathOut)
async def post_dispath(dispath: Dispath):
    dispath_search = await Dispath.by_number(dispath.number)
    if dispath_search:
        raise HTTPException(status_code=409, 
                            detail="Рассылка с таким номером уже создана")
    Scheduler.add_task(func, dispath)
    Scheduler.reload_scheduler()
    await dispath.create()
    return dispath

@router.put("/{id}", status_code=201, response_model=DispathOut)
async def update_dispath(id: int, update: DispathUpdate):
    req = {k: v for k, v in update.dict().items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in req.items()
    }}
    dispath = await Dispath.by_number(id)
    if not dispath:
        raise HTTPException(status_code=404, 
                            detail="Такой рассылки нету")
    
    Scheduler.modify_task(func, id, update)
    Scheduler.reload_scheduler()

    await dispath.update(update_query)
    return dispath

@router.delete("/{id}", response_description="Рассылка удалена", status_code=200)
async def delete_dispath(id: int) -> dict:
    dispath = await Dispath.by_number(id)
    if not dispath:
        raise HTTPException(
            status_code=404,
            detail="Такой рассылки нету"
        )

    Scheduler.delete_task(str(id))
    Scheduler.reload_scheduler()

    await dispath.delete()
    return {"message": "Dispath deleted successfully"}