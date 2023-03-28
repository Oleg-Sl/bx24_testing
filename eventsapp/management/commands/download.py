import pprint
from django.core.management.base import BaseCommand
from django.utils import timezone

from bitrix24 import tokens, requests


BATCH_SIZE = 25


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        bx24 = requests.Bitrix24()
        deadline = "2022-03-09"
        # tasks = bx24.request_list("tasks.task.list", ["ID"], {"STATUS": -1})
        tasks = bx24.request_list("tasks.task.list", ["ID"])
        length = len(tasks)
        for i in range(0, length, BATCH_SIZE):
            cmd = {}
            for j in range(i, i + BATCH_SIZE):
                if j >= length:
                    break
                task_id = tasks[j].get("id")
                cmd[task_id] = f"tasks.task.update?taskId={task_id}&fields[DEADLINE]={deadline}&fields[status]=2"

            pprint.pprint(cmd)


