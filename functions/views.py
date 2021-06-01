from functions.models import TravelInfo
from django.shortcuts import render

from userRegistration.models import UserInfo, BusPass, ConductorInfo, UserImage
from auth.views import getUserDetails, getConductorDetails
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.core.serializers import serialize
from django.http import JsonResponse
import datetime

@api_view(["POST"])
@permission_classes((AllowAny,))
def verify_bus_pass(request):
    if not request.user.is_authenticated:
        return Response({'response': "Login as a conductor to verify bus pass"}, status=HTTP_401_UNAUTHORIZED)
    username = request.data["email"]
    res = ConductorInfo.objects.filter(email=username).values()
    if len(res) == 0:
        return Response({'response': "Only conductors can verify pass"}, status=HTTP_401_UNAUTHORIZED)
    req_data = request.data
    bus_pass_data = BusPass.objects.filter(userID=request.user)[0]
    if req_data['email'] == bus_pass_data.userID and req_data['passCode'] == bus_pass_data.passCode:
        travel_log=TravelInfo()
        travel_log.email = req_data['email']
        travel_log.to_Location = req_data['to']
        travel_log.from_Location = req_data['from']
        travel_log.date = datetime.datetime.now()
        travel_log.busID = req_data['busID']
        travel_log.save()
        return Response({'response': "Pass Verified"}, status=HTTP_200_OK)
    return Response({'response': "Invalid Details"}, status=HTTP_404_NOT_FOUND)

@api_view(["GET"])
@permission_classes((AllowAny,))
def get_travel_log(request):
    if not request.user.is_authenticated:
        return Response({'response': "Login to get travel history"}, status=HTTP_401_UNAUTHORIZED)
    username = request.user
    res = UserInfo.objects.filter(email=username).values()
    if len(res) == 0:
        return Response({'response': "Invalid user"}, status=HTTP_401_UNAUTHORIZED)
    req_data = request.data
    travel_log_data = TravelInfo.objects.filter(email=request.user)
    travel_log_data=serialize("json", travel_log_data)
    return HttpResponse(travel_log_data)