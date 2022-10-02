from aiohttp import ClientSession
from core.shemas.client import Client
from core.shemas.msg import Msg
from datetime import datetime
from dataclasses import dataclass

from settings import TOKEN, URL_MSG_SEND

import asyncio

@dataclass(slots=True)
class ParamPost:
    json: dict
    session: ClientSession
    url: str
    headers: dict
    msg_id: int | None = None
    dispath_id: int | None = None
    client_id: int | None = None
    created_in: datetime | None = None    

async def func(**settings):
    client_list = await _search_client(param=settings['filter'], task_number=settings['id'])
    if client_list:
        session = ClientSession()
        async with session:
            headers = {'Authorization': f"Bearer {TOKEN}"}
            param = _create_param_post(settings['text'],session=session,headers=headers)
            sending = _create_sending(settings['id'], client_list, param)
            all_answer = await asyncio.gather(*sending)
            await _save_or_update(all_answer)

def _create_param_post(text: str, session: ClientSession, headers: dict) -> ParamPost:
    return ParamPost(
                json={'text': text},
                session=session,
                url=URL_MSG_SEND,
                headers=headers,
                                )

def _create_sending(task_id: int, client_list: list, param: ParamPost) -> list:
    sending = []
    for client in client_list:
        msg_id = int(f"{client.number}{task_id}")
        param = _update_param_post(param, msg_id, client.phone, task_id, client.number)
        sending.append(asyncio.create_task(_post_req(param=param)))
    return sending

async def _post_req(param: ParamPost) -> Msg:
    async with param.session.post(url=param.url+(str(param.msg_id)), headers=param.headers, json=param.json) as resp:
            answer = Msg(number=param.msg_id, sending_status=resp.status, num_dispath=param.dispath_id, num_client=param.client_id)
            return answer

async def _save_or_update(all_answer: list) -> None:
    for answer in all_answer:
        msg = await Msg.by_number(answer.number)
        answer.created_in = datetime.now()
        if not msg:
            await answer.create()
        else:
            req = {k: v for k, v in answer.dict().items() if v is not None}
            update_query = {"$set": {
            field: value for field, value in req.items()}}
            await msg.update(update_query)

async def _search_client(param: dict, task_number: int) -> list:
    client_list = await Client.find(param).to_list()
    result = []
    for client in client_list:
        msg = await _search_msg(param={'sending_status': 200, 'num_client': client.number, 'num_dispath': task_number})
        if not msg:
            result.append(client)
    return result

async def _search_msg(param: dict) -> list:
    msg = await Msg.find(param).to_list()
    return msg

def _update_param_post(param: ParamPost, msg_id: int, phone: int, 
                        dispath_id: int, client_id: int) -> ParamPost:
    param.msg_id = msg_id
    param.json['id'] = param.msg_id
    param.json['phone'] = phone
    param.dispath_id = dispath_id
    param.client_id = client_id
    return param