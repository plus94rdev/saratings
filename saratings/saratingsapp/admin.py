from django.contrib import admin
from .models import *

class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('file_name','uploaded_by','upload_date')
    search_fields = ('file_name', 'uploaded_by','upload_date')
    list_filter = ('file_name','upload_date', 'uploaded_by')
    date_hierarchy = 'upload_date'
    ordering = ('-upload_date',)
    fields = ('file_name', 'upload_file', 'uploaded_by')
    list_per_page = 10


class SAREventAdmin(admin.ModelAdmin):
    list_display = ('event_title','event_date','event_venue','event_image')

    
class EventRSVPAdmin(admin.ModelAdmin):
    list_display = ['event','title','first_name', 'last_name', 'email_address', 'contact_number','company','confirm_attendance','rsvp_date','rsvp_updated']

admin.site.register(FileUpload, FileUploadAdmin)
admin.site.register(SAREvent, SAREventAdmin)
admin.site.register(EventRSVP, EventRSVPAdmin)

