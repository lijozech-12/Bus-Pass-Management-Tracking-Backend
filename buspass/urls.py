"""buspass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from auth.views import login, conductor_login, sample_api
from userRegistration.views import register_bus_pass, register_conductor, home
from functions.views import verify_bus_pass, get_travel_log

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/login', login),
    path('api/test', sample_api),
    path('api/user_registration', register_bus_pass),
    path('api/travelLog', get_travel_log),
    path('api/conductor/verify_pass', verify_bus_pass),
    path('api/conductor/login', conductor_login),
    path('api/conductor/conductor_registration', register_conductor)
]
