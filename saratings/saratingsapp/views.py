from re import template
from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import EmailMessage,send_mail
from django.contrib import messages
from django.conf import settings
import random, string
from saratings.settings import IS_DEV,IS_PROD
from .models import *
from .forms import *

# if 'F16' in os.uname()[1]:
if IS_DEV:
    url_home = "http://localhost:8000/"
    
# if 'aws' in os.uname()[2]:
if IS_PROD:
    url_home = "http://saratings.com/"

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


def sar_home(request):
    
    """
    APP_DIRS = True, so template loader will search for templates inside saratingsapp/templates
    Sections are hidden using style attribute in html
    """
   #current homepage
    template = "sar_home.html"
    
    #inheritance homepage
    #template = "home/sar_home.html"
    return render(request, template)

def event_homepage(request):
    
    get_all_events = SAREvent.objects.all()
    
    for event in get_all_events:
        print("event_id",event.event_id)
    
    template = "events/events_homepage.html"
    
    context = {"get_all_events":get_all_events}
    
    return render(request, template,context)

def event_rsvp(request,event_id):
    
    event_instance = get_object_or_404(SAREvent, event_id=event_id)
        
    rsvp_form = EventRSVPForm(request.POST or None, instance=event_instance)
    
    is_DEV = False
    
    if request.method == 'POST':
        rsvp_form = EventRSVPForm(request.POST)
        if rsvp_form.is_valid():
            
            user_title = rsvp_form.cleaned_data['title']
            user_last_name = rsvp_form.cleaned_data.get('last_name')
            user_email_address = rsvp_form.cleaned_data.get('email_address')
            
            rsvp_instance = rsvp_form.save(commit=False)
            rsvp_instance.event = event_instance
            rsvp_instance.save()
            
            subject = 'RSVP Notification: Sovereign Africa Ratings Launch'
            
            html_message = (
                f"Dear " + str(user_title) +" "+ str(user_last_name)+","+ "\n \n"
                
                f"Thank you for confirming your attendance for the upcoming event.\n \n" 
                f"Event Details: \n \n"
                f""+str(event_instance)+"\n \n"
                f"Date: "+str(event_instance.event_date)+"\n \n"
                f"Time: "+str(event_instance.event_time)+"\n \n"
                f"Venue: "+str(event_instance.event_venue)+"\n \n"
                f"To view our events, please click on the link below: \n \n"
                f"https://saratings.com/events/" + "\n \n"
                f"For any queries regarding this event, kindly contact info@saratings.com \n \n"
                
                f"Yours sincerely, \n"
                f"Sovereign Africa Ratings \n"
                )

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user_email_address]
            
            if IS_DEV:
                bcc_recipient_list = ['info@saratings.com','jasonm@plus94.co.za','jasemudau@gmail.com']
                print("Sent an email Dev")
            if IS_PROD:
                bcc_recipient_list = ['info@saratings.com','jasonm@plus94.co.za','jason@saratings.com','nqobilez@papashamedia.co.za'] 
                print("Sent an email Prod")
            
            email = EmailMessage(
            subject,
            html_message,
            from_email,
            recipient_list,
            bcc_recipient_list,
            )
            
            messages.success(request,"Confirmation Received!")
            
            email.send(fail_silently=False)
            
            return redirect('eventsHomepage')

        else:
            # Return the form with POST data
            print("RSVP form is not valid")
            rsvp_form = EventRSVPForm(request.POST)
            print("rsvp_form_errors:",rsvp_form.errors)
            for field in rsvp_form.errors:
                rsvp_form[field].field.widget.attrs['class'] += 'form-group textinput textInput form-control form-control is-invalid'
            

    template = "events/event_rsvp.html"
    
    context = {"event_instance":event_instance,"event_id":event_id,"rsvp_form":rsvp_form}
    
    return render(request, template,context)

def media_homepage(request):
    
    radio_interviews = MediaPage.objects.filter(interview_platform="radio").order_by('-interview_date')
    tv_interviews = MediaPage.objects.filter(interview_platform="tv").order_by('-interview_date') 
        
    template = "media_page/media_homepage.html"
    
    context = {"radio_interviews":radio_interviews,"tv_interviews":tv_interviews}
    
    return render(request, template,context)
    