from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import path, include
from django_otp.admin import OTPAdminSite
import os

admin.site.site_header = "SA Ratings Administration"

#Enfore 2FA in all environments
# if 'aws' in os.uname()[2]:
#     admin.site.__class__ = OTPAdminSite


urlpatterns = [
    path('sar-adm/', admin.site.urls),
    path("", include("saratingsapp.urls")),
    path('password-reset/',auth_views.PasswordResetView.as_view(
                          template_name='registration/password_reset_submit.html'),
                            name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_submitted.html'),
	    name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
                    template_name='registration/password_reset_confirmation.html'),
	                name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_completed.html'),
	name='password_reset_complete'),
]

#Append 'MEDIA_URL' and 'MEDIA_ROOT' to urlpatterns
if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)