from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
import asyncio,os,shutil, random, string
from pathlib import Path

if settings.IS_PROD:
    print("Running mails in PROD")
    base_url = 'https://saratings.com/read-weekly-economic-nugget/'
    year_in_review_base_url = 'https://saratings.com/read-year-in-review/'
    mailing_list = ["jason@saratings.com","jasonm@plus94.co.za","tumi@saratings.com","zweli@saratings.com","wayne@bettersa.co.za","liza@socialhat.co.za"]

else:
    print("Running mails in DEV")
    base_url = 'http://127.0.0.1:8001/read-weekly-economic-nugget/'
    year_in_review_base_url = 'http://127.0.0.1:8001/read-year-in-review/'
    mailing_list = ["jason@saratings.com","jasonm@plus94.co.za"]

from_email_address = settings.EMAIL_HOST_USER
BASE_DIR = Path(__file__).resolve().parent.parent
    

"""
For asyncio PROD
https://python.readthedocs.io/en/stable/library/asyncio-task.html
""" 
async def send_email(subject, message):   
    
    bcc_recipient_list = mailing_list
    """
    empty_recipient_list is for the 'to' field
    bcc_recipient_list is for the 'bcc' feld
    """
    empty_recipient_list = []
    email = EmailMessage(
    subject,
    message,
    from_email_address,
    empty_recipient_list,
    bcc_recipient_list,
    )  
            
    email.send(fail_silently=False)



def send_email_async(subject, message):
    
    bcc_recipient_list = mailing_list
    empty_recipient_list = []
    
    email = EmailMessage(
    subject,
    message,
    from_email_address,
    empty_recipient_list,
    bcc_recipient_list
    )  
         
    return email.send(fail_silently=False)
    

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
    is_report_historical = models.BooleanField(default=False)
   
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
    upload_file = models.FileField(upload_to='research_publication/', blank=True,null=True)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    added_on_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    unique_id = models.CharField(max_length=20, null=True, blank=True)
   
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        
        if not self.unique_id:
            self.unique_id = get_string(10,10)
            
        super(ResearchPublication,self).save(*args,**kwargs)
    class Meta:
        db_table = "research_publication"
        verbose_name_plural = "Research Publication"
class ResearchReport(models.Model):
    
    title = models.CharField(max_length=1000, null=True, blank=False)
    report_price = models.CharField(max_length=1000, null=True, blank=False)
    overview = models.TextField(null=True, blank=True)
    file_description = models.TextField(null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_link = models.TextField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=False)
    upload_file = models.FileField(upload_to='report_publication/research_reports/', blank=True,null=True)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    added_on_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    unique_id = models.CharField(max_length=20, null=True, blank=True)
    is_report_historical = models.BooleanField(default=False)
   
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        
        if not self.unique_id:
            self.unique_id = get_string(10,10)
            
        super(ResearchReport,self).save(*args,**kwargs)
    class Meta:
        db_table = "research_report"
        verbose_name_plural = "Research Reports"
    
#Nugget publications
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
        
        subject = "SAR: Economic Nuggets(" + str(self.title) + ")"
        message = "Good day, \n\n" + "Please find the link below for the weekly economic nugget published on " + str(self.publication_date) + "\n\n" + article_link + "\n\n" + "Regards, \n" + "SAR Team"
     
        if settings.IS_PROD: 
            """
            Apache running python 3.6.8
            asyncio.sleep(1) to prevent 'not awaited error'
            """
            asyncio.sleep(1)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(send_email(str(subject),str(message)))
            loop.run_until_complete(confirm_sent_notification())
            loop.close()
            
            
        if settings.IS_DEV:
            """
            Development server running python 3.7.3
            """
            asyncio.run((send_email(str(subject),str(message))))
            print("Email sent")
        
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
        
        
   
#Year In Review publications
class YearInReview(models.Model):
    
    title = models.CharField(max_length=1000, null=True, blank=False)
    reviewed_country = models.CharField(max_length=100,null=True,blank=False)
    reviewed_year = models.CharField(max_length=5,null=True,blank=False)
    overview = models.TextField(null=True, blank=True)
    article_body = models.TextField(null=True, blank=True)
    file_description = models.TextField(null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_link = models.TextField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=False)
    upload_file = models.FileField(upload_to='year_in_review/', blank=True,null=True)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    added_on_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    unique_id = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        
        
        """
        Move files from Media to Assets to allow PDF viewing
        """
        get_year_in_reviews = YearInReview.objects.all().order_by('-publication_date')
        
        if settings.IS_DEV: 
            
            source = '/Users/jasonm/SEng/CompanyProjects/SAR/saratings/saratings/media/year_in_review/'
            destination = '/Users/jasonm/Desktop/TestCopy/'
            
            for publication in get_year_in_reviews:
                    
                self.file_link = "http://127.0.0.1:8001"+publication.upload_file.url

        if settings.IS_PROD:
            
            source = os.path.join(BASE_DIR,'media/year_in_review/') 
            destination = os.path.join(BASE_DIR,'static/assets/file/year_in_review/')
            
            for publication in get_year_in_reviews:
                    
                file_url = publication.upload_file.url      
                
                self.file_link = "https://saratings.com"+file_url.replace("media","static/assets/file")
                
            print("Prod:Moved files from media to static")

        # gather all files
        allfiles = os.listdir(source)
        
        # iterate on all files to move them to destination folder
        for fname in allfiles:
            shutil.copy2(os.path.join(source,fname), destination)    
        
        
        if not self.unique_id:
            self.unique_id = get_string(10,10)
         
        super(YearInReview,self).save(*args,**kwargs)
        
        article_link = year_in_review_base_url +  str(self.unique_id)
        
        subject = "SAR: Year In Review(" + str(self.title) + ")"
        message = "Good day, \n\n" + "Please find the link below for the Year In Review publication" + "\n\n" + self.file_link + "\n\n" + "Regards, \n" + "SAR Team"
     
        if settings.IS_PROD: 
            """
            Apache running python 3.6.8
            asyncio.sleep(1) to prevent 'not awaited error'
            """
            asyncio.sleep(1)
            #new_event_loop() to prevent 'RuntimeError: There is no current event loop in thread'
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # Blocking call which returns when the hello_world() coroutine is done
            # loop.run_until_complete(send_email(str(subject),str(message)))
            # loop.run_until_complete(confirm_sent_notification())
            loop.close()
            print("Prod: Year In Review Email sent")
            
            
            
        if settings.IS_DEV:
            """
            Development server running python 3.7.3
            """
            #Working asyncio
            asyncio.run((send_email(str(subject),str(message))))
            
            
    class Meta:
        db_table = "year_in_review"
        verbose_name_plural = "Year In Review"

#Not added to Prod yet
class ResearchPurchase(models.Model):
    
    research = models.ForeignKey(ResearchPublication,on_delete=models.CASCADE,null=True,blank=True)
    research_unique_id = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='user')
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    added_on_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    purchase_date = models.DateField(auto_now_add=True,null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    purchase_unique_id = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.research.title
    
    def save(self,*args,**kwargs):
        
        if not self.purchase_unique_id:
            self.purchase_unique_id = get_string(10,10)
            
        super(ResearchPurchase,self).save(*args,**kwargs)
    class Meta:
        db_table = "research_purchase"
        verbose_name_plural = "Research Purchase"
        
#Not added to Prod yet    
class SARSubscription(models.Model):
    
    SUBSCRIPTION_TYPE_OPTIONS = [('unsubscribed','Unsubscribed'),('6_month','6-Month Subscription'),('annual','Annual Subscription')]
    SUBSCRIPTION_FEE_OPTIONS = [('0','Free'),('30000','30000'),('50000','50000')]
    SUBSCRIPTION_OFFERS_OPTIONS = [('free','Free'),('3000','3000'),('5000','5000'),('free_+_vip_access_to_sar_team','Free + VIP Access to SAR Team'),('full_access','Full Access')]
    SUBSCRIPTION_ITEMS = [('weekly_economic_nuggets','Weekly Economic Nuggets'),
                          ('month_in_the_mirror','Month in the Mirror'),
                          ('SAR_Events','SAR Events'),
                          ('rating_announcements','Rating Announcements'),
                          ('current_credit_rating_reports','Current Credit Rating Reports'),
                          ('current_research_reports','Current Research Reports'),
                          ('historical_credit_rating_reports','Historical Credit Rating Reports'),
                          ('historical_research_reports','Historical Research Reports')]

    subscription_type = models.CharField(max_length=100,choices=SUBSCRIPTION_TYPE_OPTIONS,null=True, blank=False)
    subscription_fee = models.CharField(max_length=100,choices=SUBSCRIPTION_FEE_OPTIONS,null=True, blank=False)
    item_1 =    models.CharField(max_length=100,choices=SUBSCRIPTION_ITEMS,null=True, blank=True)
    item_1_fee = models.CharField(max_length=100,choices=SUBSCRIPTION_OFFERS_OPTIONS,null=True, blank=False)
    item_2 =    models.CharField(max_length=100,choices=SUBSCRIPTION_ITEMS,null=True, blank=True)
    item_2_fee = models.CharField(max_length=100,choices=SUBSCRIPTION_OFFERS_OPTIONS,null=True, blank=False)
    item_3 =    models.CharField(max_length=100,choices=SUBSCRIPTION_ITEMS,null=True, blank=True)
    item_3_fee = models.CharField(max_length=100,choices=SUBSCRIPTION_OFFERS_OPTIONS,null=True, blank=False)
    item_4 =    models.CharField(max_length=100,choices=SUBSCRIPTION_ITEMS,null=True, blank=True)
    item_4_fee = models.CharField(max_length=100,choices=SUBSCRIPTION_OFFERS_OPTIONS,null=True, blank=False)
    item_5 =    models.CharField(max_length=100,choices=SUBSCRIPTION_ITEMS,null=True, blank=True)
    item_5_fee = models.CharField(max_length=100,choices=SUBSCRIPTION_OFFERS_OPTIONS,null=True, blank=False)
    item_6 =    models.CharField(max_length=100,choices=SUBSCRIPTION_ITEMS,null=True, blank=True)
    item_6_fee = models.CharField(max_length=100,choices=SUBSCRIPTION_OFFERS_OPTIONS,null=True, blank=False)
    item_7 =    models.CharField(max_length=100,choices=SUBSCRIPTION_ITEMS,null=True, blank=True)
    item_7_fee = models.CharField(max_length=100,choices=SUBSCRIPTION_OFFERS_OPTIONS,null=True, blank=False)
    item_8 =    models.CharField(max_length=100,choices=SUBSCRIPTION_ITEMS,null=True, blank=True)
    item_8_fee = models.CharField(max_length=100,choices=SUBSCRIPTION_OFFERS_OPTIONS,null=True, blank=False)
    
    
    
    subscription_code = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.subscription_type
    
    def save(self,*args,**kwargs):
        
        if not self.subscription_code:
            self.subscription_code = get_string(5,5)
            
        super(SARSubscription,self).save(*args,**kwargs)
           
    class Meta:
        db_table = "sar_subscription"
        verbose_name_plural = "SAR Subscriptions"
    
   
#Added to Prod
class SARPolicy(models.Model):
    
    title = models.CharField(max_length=1000, null=True, blank=False)
    file_description = models.TextField(null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_link = models.TextField(null=True, blank=True)
    upload_file = models.FileField(upload_to='policy/', blank=True,null=True)
    effective_date = models.DateField(null=True,blank=False)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    added_on_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    unique_id = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        
        if not self.unique_id:
            self.unique_id = get_string(10,10)
            
        super(SARPolicy,self).save(*args,**kwargs)
    class Meta:
        db_table = "sar_policy"
        verbose_name_plural = "SAR Policies"
        
        

#Added to Prod
class SectorCommentary(models.Model):
    
    title = models.CharField(max_length=1000, null=True, blank=False)
    file_description = models.TextField(null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_link = models.TextField(null=True, blank=True)
    upload_file = models.FileField(upload_to='sector_commentary/', blank=True,null=True)
    effective_date = models.DateField(null=True,blank=False)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    added_on_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    unique_id = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        
        if not self.unique_id:
            self.unique_id = get_string(10,10)
            
        super(SectorCommentary,self).save(*args,**kwargs)
    class Meta:
        db_table = "sector_commentary"
        verbose_name_plural = "Sector Commentaries"
        
        

#Added to Prod    
class IssuerCommentary(models.Model):
    
    title = models.CharField(max_length=1000, null=True, blank=False)
    file_description = models.TextField(null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_link = models.TextField(null=True, blank=True)
    upload_file = models.FileField(upload_to='issuer_commentary/', blank=True,null=True)
    effective_date = models.DateField(null=True,blank=False)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    added_on_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    unique_id = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        
        if not self.unique_id:
            self.unique_id = get_string(10,10)
            
        super(IssuerCommentary,self).save(*args,**kwargs)
    class Meta:
        db_table = "issuer_commentary"
        verbose_name_plural = "Issuer Commentaries"