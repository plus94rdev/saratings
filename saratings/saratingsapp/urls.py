from django.urls import path
from django.conf.urls.static import static
from saratingsapp.views import *
from django.conf import settings


urlpatterns = [
    
    path("", sar_home, name="sar_home"),
    path('events/',event_homepage, name="eventsHomepage"),
    path('event-rsvp/<str:event_id>',event_rsvp, name="eventRSVP"),
    path('media-page/',media_homepage, name="mediaHomepage"),
    
]

#Append 'MEDIA_URL' and 'MEDIA_ROOT' to urlpatterns for PROD
if IS_PROD:
    urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
