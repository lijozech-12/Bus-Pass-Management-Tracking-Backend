from userRegistration.models import UserInfo, BusPass, ConductorInfo
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


def home(request):
    return HttpResponse("Smart bus pass is running")

@api_view(["POST"])
@permission_classes((AllowAny,))
def register_bus_pass(request):
    if not request.user.is_authenticated:
        return Response({'response': "Login to register bus pass"}, status=HTTP_401_UNAUTHORIZED)
    user_data = request.data
    print(user_data)
    user = UserInfo()
    user.firstName = user_data['firstName']
    user.lastName = user_data['lastName']
    user.isStudent = user_data['isStudent']
    user.email = request.user
    user.phoneNo = user_data['phoneNo']
    user.save()
    bus_pass = BusPass()
    bus_pass.userID = request.user
    bus_pass.passCode = get_random_string(20)
    bus_pass.user = user
    bus_pass.save()
    print(request.user, "has been registered.")

    serialized_user_data = UserInfo.objects.filter(email=request.user).values()
    return Response({"response": "User has been successfully created",
                     "userData": serialized_user_data, "busPassID": bus_pass.passCode})


@api_view(["POST"])
@permission_classes((AllowAny,))
def register_conductor(request):
    if not request.user.is_authenticated:
        return Response({'response': "Login to register as conductor"}, status=HTTP_401_UNAUTHORIZED)
    conductor_data = request.data
    print(conductor_data)
    conductor = ConductorInfo()
    conductor.firstName = conductor_data['firstName']
    conductor.lastName = conductor_data['lastName']
    conductor.email = request.user
    conductor.phoneNo = conductor_data['phoneNo']
    conductor.save()
    print(request.user, "has been registered as a conductor.")

    serialized_conductor_data = ConductorInfo.objects.filter(email=request.user).values()
    return Response({"response": "Conductor has been successfully registered",
                     "conductorData": serialized_conductor_data})


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
        return Response({'response': "Pass Verified"}, status=HTTP_200_OK)
    return Response({'response': "Invalid Details"}, status=HTTP_404_NOT_FOUND)
