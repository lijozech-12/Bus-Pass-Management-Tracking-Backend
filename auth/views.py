# from django.shortcuts import render

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.db import models

from django.contrib.auth.models import User

import requests

from userRegistration.models import UserInfo


# @csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    userData = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo?access_token="+request.POST["accessToken"]).json()
    # print(userData)
    username = userData["email"]
    password = "topsecretkey"
    if username is None:
        return Response({'error': 'Operation failed'}, status=HTTP_400_BAD_REQUEST)
    user = None
    if User.objects.filter(username=username).exists():
        user = authenticate(username=username, password=password)
        print("Logged in")
    else:
        user = User.objects.create_user(
            username=username, email=username, password=password)
        print("Created new user")
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    res=UserInfo.objects.filter(email=username).values()
    userRegistered = True
    userDetails=None
    if(len(res)==0) :
        userRegistered = False
    else:
        userDetails = res[0]
    return Response({'token': token.key, 'registered':userRegistered, 'userDetails':userDetails}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    print(request.user)
    data = {'response': "Authentication Success"}
    return Response(data, status=HTTP_200_OK)
