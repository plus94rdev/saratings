from django.contrib import admin
from .models import FileUpload

class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('file_name','uploaded_by','upload_date')
    search_fields = ('file_name', 'uploaded_by','upload_date')
    list_filter = ('file_name','upload_date', 'uploaded_by')
    date_hierarchy = 'upload_date'
    ordering = ('-upload_date',)
    fields = ('file_name', 'upload_file', 'uploaded_by')
    list_per_page = 10


admin.site.register(FileUpload, FileUploadAdmin)