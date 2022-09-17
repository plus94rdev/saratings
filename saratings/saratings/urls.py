from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path, include


admin.site.site_header = "SA Ratings Administration"


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("saratingsapp.urls")),
]

#Append 'MEDIA_URL' and 'MEDIA_ROOT' to urlpatterns
if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)