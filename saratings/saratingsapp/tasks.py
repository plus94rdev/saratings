from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
# from saratingsapp.models import UserProfile
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
import base64,requests

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
        f"Welcome to BuildRSA. Enjoy participating in realtime discussions about our country. Feel free to express yourself on any topic. \n \n"
        f"You have registered with username: " + str(guest) + "\n \n"
        
        f"Yours sincerely, \n"
        f"BuildRSA\n"
        f"www.buildrsa.co.za"
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