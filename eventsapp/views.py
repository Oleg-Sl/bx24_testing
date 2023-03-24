from rest_framework import views, status
from rest_framework.response import Response
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
import logging
import datetime
from threading import Thread


from bitrix24 import tokens, requests
from .services.tasks import forward_comment, change_deadline_for_overdue_tasks


# логгер входные данные событий
logger_access = logging.getLogger('eventsapp_access')
logger_access.setLevel(logging.INFO)
fh_access = logging.handlers.TimedRotatingFileHandler('./logs/access.log', when='D', interval=1, backupCount=10)
formatter_access = logging.Formatter('[%(asctime)s] %(levelname).1s %(message)s')
fh_access.setFormatter(formatter_access)
logger_access.addHandler(fh_access)


class InstallApiView(views.APIView):
    @xframe_options_exempt
    def post(self, request):
        data = {
            "domain": request.query_params.get("DOMAIN", "bits24.bitrix24.ru"),
            "auth_token": request.data.get("AUTH_ID", ""),
            "expires_in": request.data.get("AUTH_EXPIRES", 3600),
            "refresh_token": request.data.get("REFRESH_ID", ""),
            # используется для проверки достоверности событий Битрикс24
            "application_token": request.query_params.get("APP_SID", ""),
            'client_endpoint': f'https://{request.query_params.get("DOMAIN", "bits24.bitrix24.ru")}/rest/',
        }

        tokens.save_secrets(data)
        return render(request, 'eventsapp/install.html')


# Обработчик установленного приложения
class IndexApiView(views.APIView):

    @xframe_options_exempt
    def post(self, request):
        return render(request, 'eventsapp/index.html', context={
            "DOMAIN": "https://"
        })


class TaskCommentCreateApiView(views.APIView):
    def post(self, request):
        logger_access.info({
            "handler": "TaskCommentCreateApiView",
            "data": request.data,
            "query_params": request.query_params
        })
        task_id = request.data.get("data[FIELDS_AFTER][TASK_ID]", None)
        comment_id = request.data.get("data[FIELDS_AFTER][ID]", None)
        application_token = request.data.get("auth[application_token]", None)

        if not task_id:
            return Response("Not transferred ID task", status=status.HTTP_400_BAD_REQUEST)

        if not comment_id:
            return Response("Not transferred ID comment", status=status.HTTP_400_BAD_REQUEST)

        # forward_comment.run(task_id, comment_id)
        thr = Thread(target=forward_comment.run, args=(task_id, comment_id,))
        thr.start()

        return Response("Обновление списка сотрудников началось", status=status.HTTP_200_OK)


class ChangeDeadlineForOverdueTasksApiView(views.APIView):
    def post(self, request):
        logger_access.info({
            "handler": "ChangeDeadlineForOverdueTaskApiView",
            "data": request.data,
            "query_params": request.query_params
        })
        deadline = request.query_params.get("deadline", datetime.datetime.now()) or datetime.datetime.now()

        thr = Thread(target=change_deadline_for_overdue_tasks.run, args=(deadline,))
        thr.start()

        return Response("Обновление крайнего срока задач началось", status=status.HTTP_200_OK)
