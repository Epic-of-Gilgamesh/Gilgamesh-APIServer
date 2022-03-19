"""
Views for APIs of Authorizations
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
from user.serializers import UserSerializer


class LoginAPI(APIView):
    """Login a user

    - api - `/api/user/login`
    """
    @transaction.atomic
    def post(self, request):
        request_body = request.data
        user_cache = authenticate(
            request, 
            username=request_body['username'], 
            password=request_body['password'])
        try:
            login(request, user_cache, backend='django.contrib.auth.backends.ModelBackend')
        except:
            return Response({}, status=403)
        if user_cache is None:
            return Response({}, status=403)
        query = User.objects.get(username = user_cache.username)
        response = UserSerializer(query).data
        return Response(response, status=200)


class RegisterAPI(APIView):
    """Register an user.
    
    - api - `/api/user/register`
    """

    @transaction.atomic
    def post(self, request):
        request_body = request.data
        response = {}
        user = None
        try:
            user = User(
                username = request_body['username'],
                email = request_body['email'],
                role = request_body['role'],
                first_name = request_body['first_name'],
                last_name = request_body['last_name']
            )
            user.set_password(request_body['password'])
            user.save()
        except KeyError as e:
            logging.error(f"KeyError = {e}")
            response['msg'] = "The request doesn't contain required fields"
            return Response(response, status=400)
        except Exception as e:
            logging.error(f"Error = {e}")
            response['msg'] = "Unknown error"
            return Response(response, status=400)

        # build response
        response = UserSerializer(user).data
        return Response(response, status=200)
    

class LogoutAPI(APIView):
    """Logout request user.
    
    - api - `/api/user/logout`
    """
    def post(self, request):
        logout(request)
        response = {}
        return Response(response, status=200)