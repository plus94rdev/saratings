from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
import base64,requests
from saratings.settings import IS_DEV,IS_PROD

"""

On file changes, run:
sudo systemctl restart gunicorn
sudo systemctl daemon-reload
sudo supervisorctl restart all
"""
        

@shared_task
def rsvp_confirmation_email(guest,email_address):
    
    """
    Send a welcom email after a new registration
    """

    subject = 'BuildRSA: Welcome'
        
    html_message = (
        f"Dear " + str(guest) +","+ "\n \n"
        f"Thank you for...\n \n"
        f"You have registered with username: " + str(guest) + "\n \n"
        
        f"Yours sincerely, \n"
        f"Sovereign Africa Ratings\n"
        f"www.saratings.com"
        )

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email_address]
    bcc_recipient_list = ['jasonm@plus94.co.za','jasemudau@gmail.com']
    
    email = EmailMessage(
    subject,
    html_message,
    from_email,
    recipient_list,
    bcc_recipient_list,
    )  
            
    email.send(fail_silently=True)

    return "RSVP confirmation email sent."

   
@shared_task
def article_commentary_email(first_name,document_title,email_address):
    
    """
    Send a thank you email after commentary submission
    """

    subject = 'SARatings: Public Commentary'
        
    html_message = (
        f"Dear " + str(first_name) +","+ "\n \n"
        f"Thank you for the commentary submitted for document: " + str(document_title) + "\n \n"
        
        f"Yours sincerely, \n"
        f"Sovereign Africa Ratings\n"
        f"www.saratings.com"
        )

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email_address]
    bcc_recipient_list = ['jasonm@plus94.co.za','jason@saratings.com']
    
    email = EmailMessage(
    subject,
    html_message,
    from_email,
    recipient_list,
    bcc_recipient_list,
    )  
            
    email.send(fail_silently=False) 
    
    return "Commentary confirmation email sent."