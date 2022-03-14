"""
Views for APIs of Tasks
@author: Yizhou Zhao
@last-update: 2022/03/12
"""
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from django.db import transaction

from user.models import User
from task.models import Task, TaskLog
from task.serializers import TaskSerializer

def is_self(user, user_id):
    return str(user.id) == str(user_id)

def is_tester(user):
    return user.role == 'tester'

def is_manager(user):
    return user.role == 'manager'

class TaskCreationAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """Create a task of given user

        Args:
            request: The request object
        """
        user_id = kwargs['user_id']
        if is_self(request.user, user_id) \
           or is_tester(request.user) \
           or is_manager(request.user):
            # Parse the request payload
            request_body = request.data
            request_body['user'] = user_id
            serializer = TaskSerializer(data=request_body)
            if (serializer.is_valid()):
                serializer.save()
                return Response(serializer.data, status=201)
            return Response({'msg': 'Invalid payload'}, status=400)
        else:
            return Response({'msg': 'Unauthorized'}, status=403)


class TaskAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # ensure requst user is logged in
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """Get the task information of the given task_id

        Args:
            request: The request object
        """
        task_id = int(kwargs['task_id'])
        try:
            query = Task.objects.get(id=task_id)
            data = TaskSerializer(query).data
            return Response(data, status=200)
        except Exception as e:
            logging.error(e)
            return Response({'msg': 'Invalid request'}, status=400)
    
    def put(self, request, *args, **kwargs):
        """Update the task with given task_id
        """
        task_id = int(kwargs['task_id'])
        try:
            query = Task.objects.get(id=task_id)
            serializer = TaskSerializer(query, data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return Response(serializer.data, status=201)
            return Response({'msg': 'Invalid request'}, status=400)
        except Exception as e:
            logging.error(e)
            return Response({'msg': 'Invalid request'}, status=400)
        