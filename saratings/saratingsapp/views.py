import datetime
from re import template
from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import EmailMessage,send_mail
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.conf import settings
import random, string
from saratings.settings import IS_DEV,IS_PROD
from .models import *
from .forms import *
from .tasks import *
import os
import shutil
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
    

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
    #template = "sar_home.html"
    
    #inheritance homepage
    template = "home/sar_home.html"
    return render(request, template)

def sar_about(request):
    
    """
    APP_DIRS = True, so template loader will search for templates inside saratingsapp/templates
    Sections are hidden using style attribute in html
    """
   #current homepage
    #template = "sar_home.html"
    
    #inheritance homepage
    template = "home/sar_about.html"
    return render(request, template)

@cache_page(60*15)
def sar_team(request):
    
    """
    APP_DIRS = True, so template loader will search for templates inside saratingsapp/templates
    Sections are hidden using style attribute in html
    """
   #current homepage
    #template = "sar_home.html"
    
    #inheritance homepage
    template = "home/sar_team.html"
    
    return render(request, template)


def sar_contact(request):
    
    """
    APP_DIRS = True, so template loader will search for templates inside saratingsapp/templates
    Sections are hidden using style attribute in html
    """
   #current homepage
    #template = "sar_home.html"
    
    #inheritance homepage
    template = "home/sar_contact.html"
    
    return render(request, template)

def event_homepage(request):
    
    #Only display current and future events
    get_all_events = SAREvent.objects.filter(event_date__gte=datetime.date.today()).order_by('event_date')
    
    template = "events/events_homepage.html"
    
    todays_date = datetime.date.today()
    
    context = {"get_all_events":get_all_events,"todays_date":todays_date}
    
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
            
            print("Comment submitted")
            
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
                bcc_recipient_list = ['info@saratings.com','jasonm@plus94.co.za','jasemudau@gmail.com','jason@saratings.com']
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
    
    can_rsvp = event_instance.event_date >= datetime.date.today()
    
    if can_rsvp:
        print("Event title:",event_instance.event_title)
        print("Event date:",event_instance.event_date)
        print("Today's date:",datetime.date.today())
        print("Can RSVP:",can_rsvp)
        template = "events/event_rsvp.html"
    else:
        print("Event title:",event_instance.event_title)
        print("Event date:",event_instance.event_date)
        print("Today's date:",datetime.date.today())
        print("Can RSVP:",can_rsvp)
        messages.error(request,"This event has passed")
        return redirect('eventsHomepage')
       
    
    context = {"event_instance":event_instance,"event_id":event_id,"rsvp_form":rsvp_form,"can_rsvp":can_rsvp}
    
    return render(request, template,context)

def media_homepage(request):
    
    radio_interviews = MediaPage.objects.filter(interview_platform="radio").order_by('-interview_date')
    tv_interviews = MediaPage.objects.filter(interview_platform="tv").order_by('-interview_date') 
        
    template = "media_page/media_homepage.html"
    
    context = {"radio_interviews":radio_interviews,"tv_interviews":tv_interviews}
    
    return render(request, template,context)
    
  
def public_commentary_article_list(request):

    """
    List regulatory articles on a table
    Using shutil to copy files from media to static to allow viewing of pdfs
    """
    
    get_regulatory_articles = RegulatoryArticle.objects.all().order_by('-publication_date')
    
    todays_date = datetime.date.today()
    
    for article in get_regulatory_articles:
        if todays_date <= article.submission_deadline:
            article.is_submission_overdue = False
            article.save()
        else:
            article.is_submission_overdue = True
            article.save()
    
    if IS_DEV: 
        source = '/Users/jasonm/SEng/CompanyProjects/SAR/saratings/saratings/media/regulatory_articles/'
        destination = '/Users/jasonm/Desktop/TestCopy/'
        
        for article in get_regulatory_articles:
            
            print("upload_url:","http://127.0.0.1:8001"+article.upload_file.url)
            
            article.file_link = "http://127.0.0.1:8001"+article.upload_file.url
            article.save()
        
    
    if IS_PROD:
        # source = '/home/ubuntu/saratings/saratings/media/regulatory_articles/'
        # destination = '/home/ubuntu/saratings/saratings/static/assets/file/regulatory_articles/'
        
        source = os.path.join(BASE_DIR,'media/regulatory_articles/') 
        destination = os.path.join(BASE_DIR,'static/assets/file/regulatory_articles/')
        
        for article in get_regulatory_articles:
            
            file_url = article.upload_file.url      
            article.file_link = "https://saratings.com"+file_url.replace("media","static/assets/file")
            article.save()
        
    print("BASE_DIR:",BASE_DIR)

    # gather all files
    allfiles = os.listdir(source)
    
    # iterate on all files to move them to destination folder
    for fname in allfiles:
        shutil.copy2(os.path.join(source,fname), destination)    
    
    template = "articles/regulatory/list_public_commentary_article.html"
    
    context = {"get_regulatory_articles":get_regulatory_articles} 
    
    return render(request, template, context)

def view_commentary_article(request,unique_id):

    """
    List regulatory articles on a table
    """
    regulatory_article = get_object_or_404(RegulatoryArticle, unique_id=unique_id)
    
    print("regulatory_article",regulatory_article)
    
    template = "articles/regulatory/view_public_commentary_article.html"
    
    context = {"regulatory_article":regulatory_article} 
    
    return render(request, template, context)


def comment_commentary_article(request,unique_id):
    
    

    """
    Submit a public commentary about a regulatory article
    """
    regulatory_article = get_object_or_404(RegulatoryArticle, unique_id=unique_id)
    
    #Prevent user from submitting after the deadline
    can_submit_commentary = datetime.date.today() <= regulatory_article.submission_deadline
    
    
    print("todays_date:",datetime.date.today())
    print("submission_deadline:",regulatory_article.submission_deadline)
    print("can_submit_commentary:",can_submit_commentary)
    
    print("regulatory_article",regulatory_article)
    
    recapcha_public_key = settings.RECAPTCHA_PUBLIC_KEY
    
    regulatory_article_comment_form = RegulatoryArticleCommentForm(request.POST or None)
        
    if request.method == 'POST':
        regulatory_article_comment_form = RegulatoryArticleCommentForm(request.POST or None, request.FILES)
        if regulatory_article_comment_form.is_valid():
            
            first_name = regulatory_article_comment_form.cleaned_data.get('first_name')
            last_name = regulatory_article_comment_form.cleaned_data.get('last_name')
            email_address = regulatory_article_comment_form.cleaned_data.get('email_address')
            
            #Save instance without commiting to db. Update fields and then save
            comment_instance = regulatory_article_comment_form.save(commit=False)
            comment_instance.title = regulatory_article
            comment_instance.save()
            
            messages.success(request,"Comment received!")
           
            # email.send(fail_silently=True)
            article_commentary_email.delay(first_name,regulatory_article.title,email_address)
            
            print("Email sent")
            
            return redirect('publicCommentaryArticleList')

        else:
            # Return the form with POST data
            print("RSVP form is not valid")
            regulatory_article_comment_form = RegulatoryArticleCommentForm(request.POST or None, request.FILES)
            print("regulatory_article_comment_form_errors:",regulatory_article_comment_form.errors)
            
            for field in regulatory_article_comment_form.errors:
                regulatory_article_comment_form[field].field.widget.attrs['class'] += 'form-group textinput textInput form-control form-control is-invalid'
    
    if can_submit_commentary:
        template = "articles/regulatory/comment_public_commentary_article.html"
    else:
        return redirect('publicCommentaryArticleList')
   
    context = {"regulatory_article":regulatory_article,
               "regulatory_article_comment_form":regulatory_article_comment_form,
               "recapcha_public_key":recapcha_public_key} 
    
    return render(request, template, context)


 
def ratings_publication_list(request):

    """
    List regulatory articles on a table
    Using shutil to copy files from media to static to allow viewing of pdfs
    """
    
    get_rating_publications = RatingsPublication.objects.all().order_by('-publication_date')
     
    todays_date = datetime.date.today()
    
    if IS_DEV: 
        source = '/Users/jasonm/SEng/CompanyProjects/SAR/saratings/saratings/media/ratings_publication/'
        destination = '/Users/jasonm/Desktop/TestCopy/'
        
        for publication in get_rating_publications:
            
            print("upload_url:","http://127.0.0.1:8001"+publication.upload_file.url)
            
            publication.file_link = "http://127.0.0.1:8001"+publication.upload_file.url
            publication.save()
        
    
    if IS_PROD:
        # source = '/home/ubuntu/saratings/saratings/media/regulatory_articles/'
        # destination = '/home/ubuntu/saratings/saratings/static/assets/file/regulatory_articles/'
        
        source = os.path.join(BASE_DIR,'media/ratings_publication/') 
        destination = os.path.join(BASE_DIR,'static/assets/file/ratings_publication/')
        
        for publication in get_rating_publications:
            
            file_url = publication.upload_file.url      
            publication.file_link = "https://saratings.com"+file_url.replace("media","static/assets/file")
            publication.save()
        
    print("BASE_DIR:",BASE_DIR)

    # gather all files
    allfiles = os.listdir(source)
    
    # iterate on all files to move them to destination folder
    for fname in allfiles:
        shutil.copy2(os.path.join(source,fname), destination)    
    
    template = "ratings/ratings_publication_list.html"
    
    context = {"get_rating_publications":get_rating_publications} 
    
    return render(request, template, context)



def ratings_methodology_list(request):

    """
    List regulatory articles on a table
    Using shutil to copy files from media to static to allow viewing of pdfs
    """
    
    get_rating_methodologies = RatingsMethodology.objects.all().order_by('-publication_date')
     
    todays_date = datetime.date.today()
    
    if IS_DEV: 
        source = '/Users/jasonm/SEng/CompanyProjects/SAR/saratings/saratings/media/ratings_methodology/'
        destination = '/Users/jasonm/Desktop/TestCopy/'
        
        for publication in get_rating_methodologies:
            
            print("upload_url:","http://127.0.0.1:8001"+publication.upload_file.url)
            
            publication.file_link = "http://127.0.0.1:8001"+publication.upload_file.url
            publication.save()
        
    
    if IS_PROD:
        # source = '/home/ubuntu/saratings/saratings/media/regulatory_articles/'
        # destination = '/home/ubuntu/saratings/saratings/static/assets/file/regulatory_articles/'
        
        source = os.path.join(BASE_DIR,'media/ratings_methodology/') 
        destination = os.path.join(BASE_DIR,'static/assets/file/ratings_methodology/')
        
        for publication in get_rating_methodologies:
            
            file_url = publication.upload_file.url      
            publication.file_link = "https://saratings.com"+file_url.replace("media","static/assets/file")
            publication.save()
        
    print("BASE_DIR:",BASE_DIR)

    # gather all files
    allfiles = os.listdir(source)
    
    # iterate on all files to move them to destination folder
    for fname in allfiles:
        shutil.copy2(os.path.join(source,fname), destination)    
    
    template = "ratings/ratings_methodology_list.html"
    
    context = {"get_rating_methodologies":get_rating_methodologies} 
    
    return render(request, template, context)