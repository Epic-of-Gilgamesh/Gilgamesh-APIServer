from django.urls import path

from task.views import *

urlpatterns = [
    path("create-task/<uuid:user_id>", TaskCreationAPI.as_view()),
    path("task/<int:task_id>", TaskAPI.as_view()),
    # path("register/", RegisterAPI.as_view()),
]