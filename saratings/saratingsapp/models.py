from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
import random, string



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
    first_name = models.CharField(max_length=100, null=True, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=False)
    email_address = models.EmailField(max_length=100, null=True, blank=False)
    contact_number = models.CharField(max_length=100, null=True, blank=False)
    confirm_attendance = models.CharField(max_length=5, null=True, blank=False)
    
    def __str__(self):
        return str(self.event)
    
    class Meta:
        db_table = "event_rsvp"
        verbose_name_plural = "Events RSVP"
    