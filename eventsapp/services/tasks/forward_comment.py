import logging
from bitrix24 import tokens, requests


logger_ = logging.getLogger('forward_comment')
logger_.setLevel(logging.INFO)
fh_ = logging.handlers.TimedRotatingFileHandler('./logs/forward_comment.log', when='D', interval=1, backupCount=10)
formatter_ = logging.Formatter('[%(asctime)s] %(levelname).1s %(message)s')
fh_.setFormatter(formatter_)
logger_.addHandler(fh_)


EMOJI_FORWARD_COMMENT = "⏩"


def run(task_id, comment_id):
    if task_id not in [1329, "1329"]:
        return

    bx24 = requests.Bitrix24()
    logger_.info({
        "pos": 0
    })
    # Получение задачи и комментария
    response = bx24.call("batch", {
        "halt": 0,
        "cmd": {
            "task": f"tasks.task.get?taskId={task_id}&select[]=UF_CRM_TASK",
            "comment": f"task.commentitem.get?taskId={task_id}&itemId={comment_id}"
        }
    })
    logger_.info({
        "pos": 1,
        "response": response
    })
    if not response or "result" not in response or "result" not in response["result"]:
        return

    task = response.get("result", {}).get("result", {}).get("task", {})
    comment = response.get("result", {}).get("result", {}).get("comment", {})

    # Проверка, что комментарий нужно переслать
    comment_msg = comment.get("POST_MESSAGE").strip()
    logger_.info({
        "pos": 2,
        "comment_msg": comment_msg
    })
    if not comment_msg.startswith(EMOJI_FORWARD_COMMENT):
        return

    # # Получение ID связанной с задачей сделки
    # id_deal = get_id_from_binding(task["ufCrmTask"], "D")
    # if not id_deal:
    #     return
    #
    # # Получение данных сделки
    # deal = bx24.call("crm.deal.get", {"id": id_deal}).get("result")
    # id_task_montage = deal["UF_CRM_1661089762"]     # монтаж
    # id_task_print = deal["UF_CRM_1661089736"]       # поспечать
    # id_task_order = deal["UF_CRM_1661089895"]       # передача заказа
    #
    # # если комментарий добавлен не в задачу на монтаж
    # if task_id != id_task_montage:
    #     return

    id_task_print = 1335
    id_task_order = 1337
    logger_.info({
        "pos": 3
    })
    # Добавление комментария в задачу поспечать и передача заказа
    response = bx24.call("batch", {
        "halt": 0,
        "cmd": {
            "1": f"task.commentitem.add?taskId={id_task_print}&fields[POST_MESSAGE]={comment_msg}",
            "2": f"task.commentitem.add?taskId={id_task_order}&fields[POST_MESSAGE]={comment_msg}"
        }
    })
    logger_.info({
        "pos": 4,
        "response": response
    })


def get_id_from_binding(arr_binding, prefix):
    if not isinstance(arr_binding, list) or not arr_binding:
        return

    for binding in arr_binding:
        arr_entity_data_ = binding.split("_")
        if len(arr_entity_data_) == 2 and arr_entity_data_[0] == prefix:
            return arr_entity_data_[1]


