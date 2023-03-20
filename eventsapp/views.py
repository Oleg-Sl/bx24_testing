from rest_framework import views, status
from rest_framework.response import Response
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
import logging


from .services import tokens


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
            "query_params": request.data,
            "query_params": request.q
        })
