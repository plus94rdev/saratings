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