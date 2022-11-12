from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
import random, string
from django.core.validators import MinLengthValidator
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
import asyncio,os

if settings.IS_PROD:
    base_url = 'https://saratings.com/read-daily-nugget/'
    daily_nuggets_mailing_list = ["jason@saratings.com","jasonm@plus94.co.za"]

else:
    base_url = 'http://127.0.0.1:8001/read-daily-nugget/'
    daily_nuggets_mailing_list = ["jason@saratings.com","jasonm@plus94.co.za"]

"""
For asyncio PROD
https://python.readthedocs.io/en/stable/library/asyncio-task.html
"""

async def send_email(subject, message):
    
    # send_mail(
    #     subject,
    #     message,
    #     settings.EMAIL_HOST_USER,
    #     daily_nuggets_mailing_list,
    #     fail_silently=False,
    # )
    
    bcc_recipient_list = daily_nuggets_mailing_list
    # bcc_recipient_list.extend(['systemadmin@ResearchExpress.co.za','jasemudau@gmail.com'])
    
    """
    empty_recipient_list is for the 'to' field
    bcc_recipient_list is for the 'bcc' field
    """
    empty_recipient_list = []
    email = EmailMessage(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    empty_recipient_list,
    bcc_recipient_list,
    )  
            
    email.send(fail_silently=False)
            

async def confirm_sent_notification():
    
    print("Email notification sent")

User._meta.get_field('email')._unique = True

#Generate a modal ref string
def get_string(letters_count, digits_count):
    
    letters = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
    
    digits = ''.join((random.choice(string.digits) for i in range(digits_count)))

    # Convert resultant string to list and shuffle it to mix letters and digits
    sample_list = list(letters + digits)
    random.shuffle(sample_list)
    # convert list to string
    final_string = ''.join(sample_list)

    return final_string
    
class UserProfile(models.Model):
	
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField(max_length=60, unique=True,null=True,blank=False)
    first_name = models.CharField(max_length=30,null=True,blank=False)
    last_name = models.CharField(max_length=30,null=True,blank=False)
    cell_number = models.CharField(validators=[MinLengthValidator(10)],max_length=11, null=True,blank=False,unique=True)
    profile_ref = models.CharField(max_length=90, unique=True,null=True,blank=True)
    
    #Users are activated via a link sent to their email or sms
    is_user_activated = models.BooleanField(default=False,null=True,blank=True)
    has_subscribed = models.BooleanField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        
        get_first_name = self.first_name
        get_last_name = self.last_name
        
        get_full_name = ""
        if get_first_name == None or get_last_name == None or get_first_name == "" or get_last_name == "":
            get_full_name = self.user.username
        if get_first_name != None and get_last_name != None:
            get_full_name = get_first_name + " " + get_last_name

        return get_full_name


    class Meta:
        db_table = "user_profile"
        ordering = ('user',)
        verbose_name_plural = 'User Profiles'
        
# Generate a modal ref string
def get_string(letters_count, digits_count):
    
    letters = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
    
    digits = ''.join((random.choice(string.digits) for i in range(digits_count)))

    # Convert resultant string to list and shuffle it to mix letters and digits
    sample_list = list(letters + digits)
    random.shuffle(sample_list)
    # convert list to string
    final_string = ''.join(sample_list)

    return final_string

def doc_upload_location(instance, filename):
    
    return '{0}/{1}'.format(get_string(6,6), filename)


class FileUpload(models.Model):
    file_name = models.CharField(max_length=100, null=True, blank=True,unique=True)
    upload_file = models.FileField(upload_to=doc_upload_location, blank=True,null=True)
    uploaded_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    upload_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self):
        return self.file_name
    
    class Meta:
        db_table = "file_upload"
        
        
class SAREvent(models.Model):
    
    event_title = models.CharField(max_length=100, null=True, blank=True)
    event_id = models.CharField(max_length=100, null=True, blank=True,unique=True)
    event_date = models.DateField(null=True, blank=False)
    event_time = models.TimeField(null=True, blank=False)
    event_venue = models.CharField(max_length=100, null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    event_image =  models.ImageField(upload_to='events/', null=True, blank=True)
    agenda_item_1 = models.CharField(max_length=255, null=True, blank=True)
    agenda_item_2 = models.CharField(max_length=255, null=True, blank=True)
    agenda_item_3 = models.CharField(max_length=255, null=True, blank=True)
    agenda_item_4 = models.CharField(max_length=255, null=True, blank=True)
    agenda_item_5 = models.CharField(max_length=255, null=True, blank=True)
    agenda_item_6 = models.CharField(max_length=255, null=True, blank=True)
    agenda_item_7 = models.CharField(max_length=255, null=True, blank=True)
    agenda_item_8 = models.CharField(max_length=255, null=True, blank=True)
    agenda_item_9 = models.CharField(max_length=255, null=True, blank=True)
    agenda_item_10 = models.CharField(max_length=255, null=True, blank=True)
    agenda_item_11 = models.CharField(max_length=255, null=True, blank=True)
    agenda_item_12 = models.CharField(max_length=255, null=True, blank=True)
    agenda_item_13 = models.CharField(max_length=255, null=True, blank=True)
    agenda_item_14 = models.CharField(max_length=255, null=True, blank=True)
    agenda_item_15 = models.CharField(max_length=255, null=True, blank=True) 
    
    def __str__(self):
        return str(self.event_title)
    
    def save(self, *args,**kwards):
        if not self.event_id:
            self.event_id =str(get_string(20,20))
        super(SAREvent, self).save(*args,**kwards)
    
    class Meta:
        db_table = "sar_event"
        verbose_name_plural = "SAR Events"
        
     
class EventRSVP(models.Model):
    event = models.ForeignKey(SAREvent, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=False)
    first_name = models.CharField(max_length=100, null=True, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=False)
    company =  models.CharField(max_length=100, null=True, blank=False)
    email_address = models.EmailField(max_length=100, null=True, blank=False)
    contact_number = models.CharField(max_length=100, null=True, blank=False)
    rsvp_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    rsvp_updated = models.DateTimeField(auto_now=True,null=True,blank=True)
    confirm_attendance = models.CharField(max_length=20, null=True, blank=False)
    
    
    def __str__(self):
        return str(self.event)
    
    class Meta:
        db_table = "event_rsvp"
        verbose_name_plural = "Events RSVP"

class MediaPage(models.Model):
    
    file_name = models.CharField(max_length=100, null=True, blank=True,unique=True)
    file_description = models.TextField(null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_link = models.TextField(null=True, blank=True)
    
    #Youtube, audio streaming
    file_source = models.CharField(max_length=100, null=True, blank=True)
    #Youtube,TV, Radio, Newspaper, Magazine, Social Media, Website, Other
    interview_platform = models.CharField(max_length=100, null=True, blank=True)
    
    interview_date = models.DateField(null=True, blank=False)
    
    upload_file = models.FileField(upload_to='media_page/', blank=True,null=True)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    added_on_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    
    def __str__(self):
        return self.file_name
    
    class Meta:
        db_table = "media_page"
        verbose_name_plural = "Media Page Files"


class RegulatoryArticle(models.Model):
    
    title = models.CharField(max_length=1000, null=True, blank=False)
    overview = models.TextField(null=True, blank=False)
    file_description = models.TextField(null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_link = models.TextField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=False)
    submission_deadline = models.DateField(null=True, blank=False)
    is_submission_overdue = models.BooleanField(default=False)
    upload_file = models.FileField(upload_to='regulatory_articles/', blank=True,null=True)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    added_on_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    unique_id = models.CharField(max_length=20, null=True, blank=True)
   
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        
        if not self.unique_id:
            self.unique_id = get_string(10,10)
            
        super(RegulatoryArticle,self).save(*args,**kwargs)
    class Meta:
        db_table = "regulatory_article"
        verbose_name_plural = "Regulatory Articles"  
        
        
class RegulatoryArticleComment(models.Model):
    title = models.ForeignKey(RegulatoryArticle, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=False)
    email_address = models.EmailField(max_length=100, null=True, blank=False)
    company = models.CharField(max_length=100, null=True, blank=False)
    file_upload = models.FileField(upload_to='regulatory_articles_comment/', blank=False,null=True)
    submission_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        db_table = "regulatory_article_comment"
        verbose_name_plural = "Regulatory Article Comments"




class RatingsPublication(models.Model):
    
    title = models.CharField(max_length=1000, null=True, blank=False)
    overview = models.TextField(null=True, blank=True)
    file_description = models.TextField(null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_link = models.TextField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=False)
    upload_file = models.FileField(upload_to='ratings_publication/', blank=True,null=True)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    added_on_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    unique_id = models.CharField(max_length=20, null=True, blank=True)
   
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        
        if not self.unique_id:
            self.unique_id = get_string(10,10)
            
        super(RatingsPublication,self).save(*args,**kwargs)
    class Meta:
        db_table = "ratings_publication"
        verbose_name_plural = "Ratings Publication"  
          

class RatingsMethodology(models.Model):
    
    title = models.CharField(max_length=1000, null=True, blank=False)
    overview = models.TextField(null=True, blank=True)
    file_description = models.TextField(null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_link = models.TextField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=False)
    upload_file = models.FileField(upload_to='ratings_methodology/', blank=True,null=True)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    added_on_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    unique_id = models.CharField(max_length=20, null=True, blank=True)
   
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        
        if not self.unique_id:
            self.unique_id = get_string(10,10)
            
        super(RatingsMethodology,self).save(*args,**kwargs)
    class Meta:
        db_table = "ratings_methodology"
        verbose_name_plural = "Ratings Methodologies" 
        
        


class ResearchPublication(models.Model):
    
    title = models.CharField(max_length=1000, null=True, blank=False)
    overview = models.TextField(null=True, blank=True)
    file_description = models.TextField(null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_link = models.TextField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=False)
    upload_file = models.FileField(upload_to='ratings_publication/', blank=True,null=True)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    added_on_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    unique_id = models.CharField(max_length=20, null=True, blank=True)
   
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        
        if not self.unique_id:
            self.unique_id = get_string(10,10)
            
        super(RatingsPublication,self).save(*args,**kwargs)
    class Meta:
        db_table = "research_publication"
        verbose_name_plural = "Research Publication"   

#Daily nugget publications
class NuggetPublication(models.Model):
    
    title = models.CharField(max_length=1000, null=True, blank=False)
    overview = models.TextField(null=True, blank=True)
    article_body = models.TextField(null=True, blank=True)
    file_description = models.TextField(null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_link = models.TextField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=False)
    upload_file = models.FileField(upload_to='nuggets_publication/', blank=True,null=True)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    added_on_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    unique_id = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        
        if not self.unique_id:
            self.unique_id = get_string(10,10)
         
        super(NuggetPublication,self).save(*args,**kwargs)
        
        article_link = base_url +  str(self.unique_id)
        
        subject = "SAR Daily Nuggets:" + " " + str(self.title)
        message = "Good day, \n\n" + "Please find the link below for the daily nugget publication for " + str(self.publication_date) + "\n\n" + article_link + "\n\n" + "Regards, \n" + "SAR Team"
    
       
        
        if settings.IS_PROD: 
            """
            Apache running python 3.6.8
            """
            loop = asyncio.get_event_loop()
            # Blocking call which returns when the hello_world() coroutine is done
            loop.run_until_complete(send_email(str(subject),str(message)))
            loop.run_until_complete(confirm_sent_notification())
            loop.close()
            
            
        if settings.IS_DEV:
            """
            Development server running python 3.7.3
            """
            asyncio.run((send_email(str(subject),str(message))))
            

        
        
    class Meta:
        db_table = "nugget_publication"
        verbose_name_plural = "Nuggets Publication"
        

class NuggetComment(models.Model):
    
    nugget = models.ForeignKey(NuggetPublication,on_delete=models.CASCADE,null=True,blank=True)
    comment = models.TextField(null=True, blank=False)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    added_on_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    comment_unique_id = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.comment
    
    def save(self,*args,**kwargs):
        
        if not self.comment_unique_id:
            self.comment_unique_id = get_string(10,10)
            
        super(NuggetComment,self).save(*args,**kwargs)
    class Meta:
        db_table = "nugget_comment"
        verbose_name_plural = "Nuggets Comment"