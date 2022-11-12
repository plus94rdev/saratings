from typing import Optional, Sequence
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

class MediaPageFileAdmin(admin.ModelAdmin):
    list_display = ('file_name','added_by','added_on_date','file_type','upload_file','file_link','file_description','interview_date','interview_platform')
    search_fields = ('file_name', 'added_by','added_on_date','interview_date')
    list_filter = ('file_name','added_on_date', 'added_by')
    date_hierarchy = 'added_on_date'
    ordering = ('-added_on_date',)
    # fields = ('file_name','file_description', 'upload_file', 'uploaded_by','file_type')    
    list_per_page = 10
class RegulatoryArticleAdmin(admin.ModelAdmin):
    
    list_display = ('title','added_by','added_on_date','file_type','upload_file','file_link','file_description','publication_date','submission_deadline')
    search_fields: Sequence[str] = ('title', 'added_by','added_on_date','review_date')
    list_filter: Sequence[str] = ('title','added_on_date', 'added_by')
    ordering: Optional[Sequence[str]] = ('-added_on_date',)
    list_per_page: int = 10
 
class RegulatoryArticleCommentAdmin(admin.ModelAdmin):
     
     list_display: Sequence[str] = ('title','first_name','last_name','email_address','company','submission_date')
    
    
class RatingsPublicationAdmin(admin.ModelAdmin):
    
    list_display = ('title','added_by','added_on_date','file_type','upload_file','file_link','file_description','publication_date')
    search_fields: Sequence[str] = ('title', 'added_by','added_on_date','review_date')
    list_filter: Sequence[str] = ('title','added_on_date', 'added_by')
    ordering: Optional[Sequence[str]] = ('-added_on_date',)
    list_per_page: int = 10
 

class RatingsMethodologyAdmin(admin.ModelAdmin):
    
    list_display = ('title','added_by','added_on_date','file_type','upload_file','file_link','file_description','publication_date')
    search_fields: Sequence[str] = ('title', 'added_by','added_on_date','review_date')
    list_filter: Sequence[str] = ('title','added_on_date', 'added_by')
    ordering: Optional[Sequence[str]] = ('-added_on_date',)
    list_per_page: int = 10


class ResearchPublicationAdmin(admin.ModelAdmin):
    
    list_display = ('title','added_by','added_on_date','file_type','upload_file','file_link','file_description','publication_date')
    search_fields: Sequence[str] = ('title', 'added_by','added_on_date','review_date')
    list_filter: Sequence[str] = ('title','added_on_date', 'added_by')
    ordering: Optional[Sequence[str]] = ('-added_on_date',)
    list_per_page: int = 10

class NuggetPublicationAdmin(admin.ModelAdmin):
    
    list_display = ('title','added_by','added_on_date','file_type','upload_file','file_link','file_description','publication_date')
    search_fields: Sequence[str] = ('title', 'added_by','added_on_date','review_date')
    list_filter: Sequence[str] = ('title','added_on_date', 'added_by')
    ordering: Optional[Sequence[str]] = ('-added_on_date',)
    list_per_page: int = 10
    
admin.site.register(FileUpload, FileUploadAdmin)
admin.site.register(SAREvent, SAREventAdmin)
admin.site.register(EventRSVP, EventRSVPAdmin)
admin.site.register(MediaPage, MediaPageFileAdmin)
admin.site.register(RegulatoryArticle, RegulatoryArticleAdmin)
admin.site.register(RegulatoryArticleComment, RegulatoryArticleCommentAdmin)
admin.site.register(RatingsPublication, RatingsPublicationAdmin)
admin.site.register(RatingsMethodology, RatingsMethodologyAdmin)
admin.site.register(ResearchPublication, ResearchPublicationAdmin)
admin.site.register(NuggetPublication, NuggetPublicationAdmin)
