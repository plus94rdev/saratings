from django.urls import path, include
from saratingsapp.views import *

urlpatterns = [
    
    path("", sar_home, name="sar_home"),
    path('events/',event_homepage, name="eventsHomepage"),
    path('event-rsvp/<str:event_id>',event_rsvp, name="eventRSVP"),
    
]

