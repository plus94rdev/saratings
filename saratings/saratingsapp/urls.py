from django.urls import path, include
from saratingsapp.views import *

urlpatterns = [
    
    path("", sar_home, name="sar_home"),
    
]