from fastapi import APIRouter, HTTPException
from core.shemas.dispath import Dispath
from core.shemas.msg import Msg
from v1.utils.stats import group_msg, format_response

router = APIRouter()

@router.get("/", status_code=200)
async def get_all_task():
    dispath_all = await Dispath.find_all().to_list()
    msg_all = await Msg.find_all().to_list()
    if not dispath_all:
        raise HTTPException(
            status_code=404,
            detail="Данных нету"
        )
    result = group_msg(dispath_all, msg_all)
    return result

@router.get("/{id}", status_code=200)
async def get_task(id: int):
    search_msg = await Msg.find({'num_dispath': id}).to_list()
    if not search_msg:
        raise HTTPException(
            status_code=404,
            detail="Данных нету"
        )
    result = format_response(search_msg)
    return result
