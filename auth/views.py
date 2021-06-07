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
from django.contrib.auth.models import User
import requests
from userRegistration.models import UserInfo, BusPass, ConductorInfo, UserImage


def getUserDetails(user: User):
    password = "topsecretkey"
    print(user, "is the user")
    user = authenticate(username=user.email, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    res = UserInfo.objects.filter(email=user.email).values()
    user_registered = True
    user_details = None
    bus_pass_id = None
    if len(res) == 0:
        user_registered = False
    else:
        user_details = res[0]
        bus_pass_id = BusPass.objects.filter(
            userID=user.email).values()[0]['passCode']
    return Response({'token': token.key, 'registered': user_registered, 'picture': UserImage.objects.filter(userID=user.email).values()[0]['pic'],
                     'userDetails': user_details, 'busPassID': bus_pass_id}, status=HTTP_200_OK)


def getConductorDetails(user: User):
    password = "topsecretkey"
    print(user, "is the user")
    user = authenticate(username=user.email, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    res = ConductorInfo.objects.filter(email=user.email).values()
    conductor_registered = True
    conductor_details = None
    if len(res) == 0:
        conductor_registered = False
    else:
        conductor_details = res[0]
    return Response({'token': token.key, 'registered': conductor_registered, 'picture': UserImage.objects.filter(userID=user.email).values()[0]['pic'],
                     'conductorDetails': conductor_details}, status=HTTP_200_OK)

# @csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    user_data = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo?access_token="+request.POST["accessToken"]).json()
    print(user_data) 
    username = user_data["email"]
    picture=user_data["picture"]
    password = "topsecretkey"
    if username is None or username == '':
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
    userImg = UserImage()
    userImg.userID = username
    userImg.pic = picture
    userImg.save()
    return getUserDetails(user)


@api_view(["POST"])
@permission_classes((AllowAny,))
def conductor_login(request):
    user_data = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo?access_token="+request.POST["accessToken"]).json()
    # print(user_data)
    username = user_data["email"]
    picture=user_data["picture"]
    password = "topsecretkey"
    if username is None or username == '':
        return Response({'error': 'Operation failed'}, status=HTTP_400_BAD_REQUEST)
    conductor = None
    if User.objects.filter(username=username).exists():
        conductor = authenticate(username=username, password=password)
        print("Logged in")
    else:
        conductor = User.objects.create_user(
            username=username, email=username, password=password)
        print("Created new user")
    if not conductor:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
    userImg = UserImage()
    userImg.userID = username
    userImg.pic = picture
    userImg.save()
    return getConductorDetails(conductor)
    # token, _ = Token.objects.get_or_create(user=conductor)
    # res = ConductorInfo.objects.filter(email=username).values()
    # conductor_registered = True
    # conductor_details = None
    # if len(res) == 0:
    #     conductor_registered = False
    # else:
    #     conductor_details = res[0]
    # return Response({'token': token.key, 'registered': conductor_registered, 'picture': UserImage.objects.filter(userID=username).values()[0]['pic'],
    #                  'conductorDetails': conductor_details}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    print(request.user)
    data = {'response': "Authentication Success. Logged in as " + str(request.user)}
    return Response(data, status=HTTP_200_OK)
