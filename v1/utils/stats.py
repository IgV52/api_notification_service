from core.shemas.msg import MsgOut

def format_response(data: list) -> dict:
    new_data = []
    for msg in data:
        msg = MsgOut(number=msg.number, sending_status=msg.sending_status, num_dispath=msg.num_dispath, num_client=msg.num_client, created_in=msg.created_in)
        new_data.append(msg)
    response = _response_body(new_data)
    return response

def group_msg(all_dispath: list, all_msg: list) -> dict:
    result = list()
    for dispath in all_dispath:
        task_dict = {'id_task': dispath.number, 'msg': list()}
        for msg in all_msg:
            if msg.num_dispath == dispath.number:
                msg_dict = {'id_msg': msg.number, 'sending_status': msg.sending_status}
                task_dict['msg'].append(msg_dict)
        task_dict['quantity_msg'] = len(task_dict['msg'])
        task_dict['msg'] = _sorted_list(task_dict['msg'])
        result.append(task_dict)
    result = _response_body(result)
    return result

def _response_body(data: list) -> dict:
    return {
        "data": data,
        "code": 200,
    }

def _sorted_list(data: list) -> list:
    sorted_tuple = sorted(data, key=lambda x: x['sending_status'])
    return list(sorted_tuple)
