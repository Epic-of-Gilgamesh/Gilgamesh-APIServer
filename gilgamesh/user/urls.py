from django.urls import path

from user.views import *

urlpatterns = [
    # Authorization
    path("login", LoginAPI.as_view()),
    path("logout", LogoutAPI.as_view()),
    path("register", RegisterAPI.as_view()),
]