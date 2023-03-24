from django.urls import include, path
from rest_framework import routers


from .views import (
    IndexApiView,
    InstallApiView,
    TaskCommentCreateApiView,
    ChangeDeadlineForOverdueTasksApiView,
)

app_name = 'eventsapp'
router = routers.DefaultRouter()


urlpatterns = [
    # path('', include(router.urls)),

    path('index/', IndexApiView.as_view()),
    path('install/', InstallApiView.as_view()),

    path('task-comment-create/', TaskCommentCreateApiView.as_view()),  # добавление комментария к задаче
    path('change-deadline-all-overdue_tasks/', ChangeDeadlineForOverdueTasksApiView.as_view()),  # изменение крайнего срока в просроченных задачах

    # path('task-change-deadline/', TaskChangeDeadlineApiView.as_view()), # изменение дедлайна задачи
]

urlpatterns += router.urls


