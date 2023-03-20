from django.urls import include, path
from rest_framework import routers


from .views import (
    InstallApiView,
    TaskCommentCreateApiView,
)

app_name = 'eventsapp'
router = routers.DefaultRouter()


urlpatterns = [
    # path('', include(router.urls)),

    path('install/', InstallApiView.as_view()),                         # установка приложения

    path('task-comment-create/', TaskCommentCreateApiView.as_view()),  # добавление комментария к задаче
    # path('task-change-deadline/', TaskChangeDeadlineApiView.as_view()), # изменение дедлайна задачи
]

urlpatterns += router.urls


