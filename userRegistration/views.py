from django.shortcuts import render
from userRegistration.models import UserInfo, BusPass


from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.db import models

from django.utils.crypto import get_random_string


@api_view(["POST"])
@permission_classes((AllowAny,))
def registerBusPass(request):
    if(not request.user.is_authenticated):
        return Response({'response':"Login to register bus pass" }, status=HTTP_401_UNAUTHORIZED)
    userData = request.data
    print(userData)
    user = UserInfo()
    user.firstName = userData['firstName']
    user.lastName = userData['lastName']
    user.isStudent = userData['isStudent']
    user.email = request.user
    user.phoneNo = userData['phoneNo']
    user.save()
    busPass = BusPass()
    busPass.userID=request.user
    busPass.passCode = get_random_string(20)
    busPass.save()
    print(request.user, "has been registered.")

    serializedUserData = UserInfo.objects.filter(email=request.user).values()
    return Response({"response":"User has been successfully created","userData":serializedUserData, "busPassID":busPass.passCode})


@api_view(["POST"])
@permission_classes((AllowAny,))
def verifyBusPass(request):
    if(not request.user.is_authenticated):
        return Response({'response': "Login to register bus pass"}, status=HTTP_401_UNAUTHORIZED)
    reqData = request.data
    busPassData=BusPass.objects.filter(userID=request.user)[0]
    if reqData['email']==busPassData.userID and reqData['passCode'] == busPassData.passCode:
        return Response({'response': "Pass Verified"}, status=HTTP_200_OK)
    return Response({'response': "Invalid Details"}, status=HTTP_404_NOT_FOUND)
