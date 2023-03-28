import logging
import datetime
import re

from bitrix24 import tokens, requests


logger_change_deadline = logging.getLogger('change_deadline_for_overdue_tasks')
logger_change_deadline.setLevel(logging.INFO)
fh_change_deadline = logging.handlers.TimedRotatingFileHandler('./logs/change_deadline_for_overdue_tasks.log', when='D', interval=1, backupCount=10)
formatter_change_deadline = logging.Formatter('[%(asctime)s] %(levelname).1s %(message)s')
fh_change_deadline.setFormatter(formatter_change_deadline)
logger_change_deadline.addHandler(fh_change_deadline)


BATCH_SIZE = 25


def run(deadline):
    bx24 = requests.Bitrix24()
    deadline_str = deadline.strftime("%Y-%m-%d")
    tasks = bx24.request_list("tasks.task.list", ["ID"], {"STATUS": -1})

    length = len(tasks)
    for i in range(0, length, BATCH_SIZE):
        cmd = {}
        for j in range(i, i + BATCH_SIZE):
            if j >= length:
                break
            task_id = tasks[j].get("id")
            cmd[task_id] = f"tasks.task.update?taskId={task_id}&fields[DEADLINE]={deadline_str}&fields[status]=2"
            logger_change_deadline.info({
                "task_id": task_id,
                "deadline": deadline_str
            })

        # response = bx24.call("batch", {"halt": 0, "cmd": cmd})



# def run(deadline):
#     bx24 = requests.Bitrix24()
#     # deadline_str = deadline.strftime("%Y-%m-%d")
#     # start = 0
#     while True:
#         response = bx24.call(
#             "tasks.task.list",
#             {
#                 "filter": {
#                     "STATUS": -1
#                 },
#                 "select": ["ID"],
#                 "order": {"ID": "asc"},
#                 # "start": start
#             },
#         )
#         logger_change_deadline.info({
#             "position": "1",
#             "response": response
#         })
#         if not response or "result" not in response or "tasks" not in response.get("result", {}):
#             return
#
#         if not response.get("result", {}).get("tasks", []):
#             break
#
#         # Изменение первых 25 задач из 50
#         cmd = {}
#         for task_ in response.get("result", {}).get("tasks", [])[:25]:
#             task_id = task_["id"]
#             cmd[task_id] = f"tasks.task.update?taskId={task_id}&fields[DEADLINE]={deadline}&fields[status]=2"
#
#         if cmd:
#             res_1 = bx24.call("batch", {"halt": 0, "cmd": cmd})
#             logger_change_deadline.info({
#                 "position": "2",
#                 "res_1": res_1
#             })
#
#         # Изменение последних 25 задач из 50
#         cmd = {}
#         for task_ in response.get("result", {}).get("tasks", [])[25:]:
#             task_id = task_["id"]
#             cmd[task_id] = f"tasks.task.update?taskId={task_id}&fields[DEADLINE]={deadline}&fields[status]=2"
#
#         if cmd:
#             res_2 = bx24.call("batch", {"halt": 0, "cmd": cmd})
#             logger_change_deadline.info({
#                 "position": "3",
#                 "res_2": res_2
#             })


