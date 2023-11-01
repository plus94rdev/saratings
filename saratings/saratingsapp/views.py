import datetime
from re import template
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import EmailMessage,send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
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

def registration(request):
    
    template = "registration/registration.html"
    
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()
    
    if request.method == "POST":
        
        user_form = UserRegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user_profile = profile_form.save(commit=False)
            user_profile.user = user
            user_profile.profile_ref = get_string(20,20)
            user_profile.save()
            
            username = user_form.cleaned_data.get('username')
            email_address = user_form.cleaned_data.get('email')
            msg = messages.info(
                request, f"{username} successsfully registered!" +  "\n \n"
                         f"Login below.")
            
            #Celery task to send email
            # new_user_welcome_email.delay(username,email_address)
            
            return redirect('sar_home')
                
        else:
            # Return the form with POST data
            user_form = UserRegisterForm(request.POST)
            profile_form = UserProfileForm(request.POST)
            print("form not valid",user_form.errors)
            print("profile_form not valid",profile_form.errors)
            
            for field in user_form.errors:
                user_form[field].field.widget.attrs['class'] += 'form-group textinput textInput form-control form-control is-invalid'
            
    
    context = {"user_form":user_form,"profile_form":profile_form}
    
    return render(request, template,context)
    

def user_login(request):

    template = "registration/login.html"
    
    is_user_authenticated = request.user.is_authenticated
    print("is_user_authenticated first check",is_user_authenticated)
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                print("Successful login")
                is_user_authenticated = request.user.is_authenticated
                print("is_user_authenticated first main check",is_user_authenticated) 
                
                response = redirect('sar_home')
                response.set_cookie('site', "saratings.com")
                
                return response
                

            else:
               print("SAR login: User is None")
               messages.error(request,  "Invalid username or password")

        else:
            messages.error(request, "Invalid username or password")
            
            # Return the form with POST data
            form = AuthenticationForm(request.POST, data=request.POST)
            print("login_form not valid",form.errors)
            
                    
    form = AuthenticationForm()
    
    context = {"form": form,"is_user_authenticated":is_user_authenticated}

    return render(request, template, context)

def user_logout(request):
    
    logout(request)
    
    return redirect('sar_home')

def user_activation(request, profile_ref):
    
    """
    From ResearchExpress
    View not currently used
    """

    message = "Profile activated. You can now login."

    get_user = get_object_or_404(UserProfile,profile_ref=profile_ref)

    print("get_user profile id check",get_user.id)
    get_user.is_user_activated= True
    get_user.save()
    
    template = "registration/user_activation.html"

    context = {"message": message}

    return render(request, template, context)

def sar_home(request):
    
    """
    APP_DIRS = True, so template loader will search for templates inside saratingsapp/templates
    Sections are hidden using style attribute in html
    """
    is_user_authenticated = request.user.is_authenticated
    
    get_username = request.user.username
    
    print("is_user_authenticated first check",is_user_authenticated)
    
    template = "home/sar_home.html"
    
    context = {"is_user_authenticated":is_user_authenticated,"get_username":get_username}
    
    return render(request, template,context)

def sar_about(request):
    
    """
    APP_DIRS = True, so template loader will search for templates inside saratingsapp/templates
    Sections are hidden using style attribute in html
    """
    
    is_user_authenticated = request.user.is_authenticated
    
    get_username = request.user.username
    
    template = "home/sar_about.html"
    
    context = {"is_user_authenticated":is_user_authenticated,"get_username":get_username}
    
    return render(request, template,context)




def sar_mission(request):
    
    """
    APP_DIRS = True, so template loader will search for templates inside saratingsapp/templates
    Sections are hidden using style attribute in html
    """
    
    is_user_authenticated = request.user.is_authenticated
    
    get_username = request.user.username
    
    template = "home/sar_mission.html"
    
    context = {"is_user_authenticated":is_user_authenticated,"get_username":get_username}
    
    return render(request, template,context)

# @cache_page(60*15)
def sar_team(request):
    
    """
    APP_DIRS = True, so template loader will search for templates inside saratingsapp/templates
    Sections are hidden using style attribute in html
    """
    is_user_authenticated = request.user.is_authenticated
    get_username = request.user.username
    
    executives = LeadershipProfile.objects.filter(is_executive=1)
    non_executives = LeadershipProfile.objects.filter(is_non_executive=1)
     
    context = {"is_user_authenticated":is_user_authenticated,"get_username":get_username,
               "executives":executives,"non_executives":non_executives}
    
    template = "home/sar_team.html"
    
    return render(request, template,context)


def sar_contact(request):
    
    """
    APP_DIRS = True, so template loader will search for templates inside saratingsapp/templates
    Sections are hidden using style attribute in html
    """
    is_user_authenticated = request.user.is_authenticated
    get_username = request.user.username
    
    template = "home/sar_contact.html"
    
    context = {"is_user_authenticated":is_user_authenticated,"get_username":get_username}
    
    return render(request, template, context)

def event_homepage(request):
    
    #Only display current and future events
    # get_all_events = SAREvent.objects.filter(event_date__gte=datetime.date.today()).order_by('event_date')
    get_all_events = SAREvent.objects.filter().order_by('-event_date')
    
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
    
    is_user_authenticated = request.user.is_authenticated
    get_username = request.user.username
    
    
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
    
    context = {"get_regulatory_articles":get_regulatory_articles,"is_user_authenticated":is_user_authenticated,
               "get_username":get_username}
    
    return render(request, template, context)

def view_commentary_article(request,unique_id):

    """
    List regulatory articles on a table
    """
    
    is_user_authenticated = request.user.is_authenticated
    get_username = request.user.username
    
    regulatory_article = get_object_or_404(RegulatoryArticle, unique_id=unique_id)
    
    print("regulatory_article",regulatory_article)
    
    template = "articles/regulatory/view_public_commentary_article.html"
    
    context = {"regulatory_article":regulatory_article,"is_user_authenticated":is_user_authenticated,} 
    
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
    is_user_authenticated = request.user.is_authenticated
    get_username = request.user.username

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
    
    context = {"get_rating_publications":get_rating_publications,
               "is_user_authenticated":is_user_authenticated} 
    
    return render(request, template, context)



def ratings_methodology_list(request):

    """
    List regulatory articles on a table
    Using shutil to copy files from media to static to allow viewing of pdfs
    """
    is_user_authenticated = request.user.is_authenticated
    get_username = request.user.username
    
    
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
    
    context = {"get_rating_methodologies":get_rating_methodologies,
               "is_user_authenticated":is_user_authenticated,"get_username":get_username}
    
    return render(request, template, context)


#View not currently used, will be used for publishing research doc for purchase
def resarch_publication_list(request):

    """
    List research publications
    Using shutil to copy files from media to static to allow viewing of pdfs
    """
    is_user_authenticated = request.user.is_authenticated
    get_username = request.user.username
    
    get_research_publications = ResearchPublication.objects.all().order_by('-publication_date')
     
    todays_date = datetime.date.today()
    
    if IS_DEV: 
        source = '/Users/jasonm/SEng/CompanyProjects/SAR/saratings/saratings/media/ratings_publication/'
        destination = '/Users/jasonm/Desktop/TestCopy/'
        
        for publication in get_research_publications:
            
            print("upload_url:","http://127.0.0.1:8001"+publication.upload_file.url)
            
            publication.file_link = "http://127.0.0.1:8001"+publication.upload_file.url
            publication.save()
        
    
    if IS_PROD:
        # source = '/home/ubuntu/saratings/saratings/media/regulatory_articles/'
        # destination = '/home/ubuntu/saratings/saratings/static/assets/file/regulatory_articles/'
        
        source = os.path.join(BASE_DIR,'media/research_publication/') 
        destination = os.path.join(BASE_DIR,'static/assets/file/research_publication/')
        
        for publication in get_research_publications:
            
            file_url = publication.upload_file.url      
            publication.file_link = "https://saratings.com"+file_url.replace("media","static/assets/file")
            publication.save()
        
    print("BASE_DIR:",BASE_DIR)

    # gather all files
    allfiles = os.listdir(source)
    
    # iterate on all files to move them to destination folder
    for fname in allfiles:
        shutil.copy2(os.path.join(source,fname), destination)    
    
    template = "research/research_publication_list.html"
    
    context = {"get_research_publications":get_research_publications,
               "is_user_authenticated":is_user_authenticated,"get_username":get_username}
    
    return render(request, template, context)    



def nuggets_publication_list(request):

    """
    List regulatory articles on a table
    Using shutil to copy files from media to static to allow viewing of pdfs
    """
    is_user_authenticated = request.user.is_authenticated
    get_username = request.user.username
    
    get_nugget_publications = NuggetPublication.objects.all().order_by('-publication_date')
     
    todays_date = datetime.date.today()
    
    if IS_DEV: 
        source = '/Users/jasonm/SEng/CompanyProjects/SAR/saratings/saratings/media/nuggets_publication/'
        destination = '/Users/jasonm/Desktop/TestCopy/'
        
        for publication in get_nugget_publications:
            
            
            
            # print("upload_url:","http://127.0.0.1:8001"+publication.upload_file.url)
            
            # publication.file_link = "http://127.0.0.1:8001"+publication.upload_file.url
            # publication.save()
            pass
        
    
    if IS_PROD:
        # source = '/home/ubuntu/saratings/saratings/media/regulatory_articles/'
        # destination = '/home/ubuntu/saratings/saratings/static/assets/file/regulatory_articles/'
        
        source = os.path.join(BASE_DIR,'media/nuggets_publication/') 
        destination = os.path.join(BASE_DIR,'static/assets/file/nuggets_publication/')
        
        for publication in get_nugget_publications:
            
            # file_url = publication.upload_file.url      
            # publication.file_link = "https://saratings.com"+file_url.replace("media","static/assets/file")
            # publication.save()
            pass
        
    print("BASE_DIR:",BASE_DIR)

    # gather all files
    allfiles = os.listdir(source)
    
    # iterate on all files to move them to destination folder
    for fname in allfiles:
        shutil.copy2(os.path.join(source,fname), destination)    
    
    template = "articles/daily_nuggets/nuggets_publication_list.html"
    
    context = {"is_user_authenticated":is_user_authenticated,"get_username":get_username,
               "get_nugget_publications":get_nugget_publications} 
    
    return render(request, template, context)

def read_nugget(request, unique_id):
    
    is_user_authenticated = request.user.is_authenticated
    get_username = request.user.username or "Guest"
    
    print("read_nugget:is_authenticated:",request.user.is_authenticated)
    get_nugget = NuggetPublication.objects.get(unique_id=unique_id)
    print("get_nugget:",get_nugget)
    
    nugget_comment_form = NuggetCommentForm()
    
    get_nugget_comments = NuggetComment.objects.filter(nugget_id=get_nugget.id).order_by('added_on_date')
    
    count_nugget_comments = NuggetComment.objects.filter(nugget_id=get_nugget.id).count()

    if request.method == "POST":
        final_reply_comment = ""
        nugget_comment_form = NuggetCommentForm(request.POST)
        
        if nugget_comment_form.is_valid():
            nugget_comment_form = nugget_comment_form.save(commit=False)
            nugget_comment_form.nugget = get_nugget
            nugget_comment_form.added_by = request.user
            nugget_comment_form.username = request.user.username
            article_comment = nugget_comment_form.comment
            
            #Check if the comment is a reply to another comment and take the first and last part of the comment
            if "@" and ":" in article_comment:
                reply_comment = nugget_comment_form.comment.split(":")[0] + " " + nugget_comment_form.comment.split(":")[1]
                final_reply_comment = reply_comment
                nugget_comment_form.comment = final_reply_comment
            else:
                nugget_comment_form.comment = article_comment
            
            nugget_comment_form.save()
            
        
            return redirect('read_nugget',unique_id=unique_id)
    
    # if request.user.is_authenticated:
        
    template = "articles/daily_nuggets/read_nugget.html"
    
    context = {"is_user_authenticated":is_user_authenticated,"get_username":get_username,
                "get_nugget":get_nugget,
                "nugget_comment_form":nugget_comment_form,
                "get_nugget_comments":get_nugget_comments,"count_nugget_comments":count_nugget_comments}
    # else:
        
    #     view_error_message =  "Error: You need to be logged in to view this page"
        
    #     print("user not registered")

    #     context = {"view_error_message":view_error_message}
            
    #     return redirect('nuggets_publication_list')
    
    
    return render(request, template, context)

def year_in_review_publication_list(request):

    """
    List regulatory articles on a table
    Using shutil to copy files from media to static to allow viewing of pdfs
    """
    is_user_authenticated = request.user.is_authenticated
    get_username = request.user.username
    
    get_year_in_reviews = YearInReview.objects.all().order_by('-publication_date')
    
    #Use Celery to copy files from media to static
    if IS_DEV: 
        
        source = '/Users/jasonm/SEng/CompanyProjects/SAR/saratings/saratings/media/year_in_review/'
        destination = '/Users/jasonm/Desktop/TestCopy/'
        
        for publication in get_year_in_reviews:
                
            print("upload_url:","http://127.0.0.1:8001"+publication.upload_file.url)
            
            publication.file_link = "http://127.0.0.1:8001"+publication.upload_file.url
            publication.save()
          
    if IS_PROD:
        
        source = os.path.join(BASE_DIR,'media/year_in_review/') 
        destination = os.path.join(BASE_DIR,'static/assets/file/year_in_review/')
        
        for publication in get_year_in_reviews:
                
            file_url = publication.upload_file.url      
            publication.file_link = "https://saratings.com"+file_url.replace("media","static/assets/file")
            publication.save()
    
    print("BASE_DIR:",BASE_DIR)
    
    
    

    # gather all files
    allfiles = os.listdir(source)
    
    # iterate on all files to move them to destination folder
    for fname in allfiles:
        shutil.copy2(os.path.join(source,fname), destination)    
    
    template = "research/year_in_review/year_in_review_publication_list.html"
    
    context = {"is_user_authenticated":is_user_authenticated,"get_username":get_username,
               "get_year_in_reviews":get_year_in_reviews} 
    
    return render(request, template, context)

def purchase_research(request):
    
    get_username = request.user.username
    is_user_authenticated = request.user.is_authenticated
    
    template = "research/purchase_research.html"
    
    research_purchase_form = ResearchPurchaseForm()
    
    if request.method == "POST":
        purchase_form = ResearchPurchaseForm(request.POST)
        
        if purchase_form.is_valid():
            purchase_form = purchase_form.save(commit=False)
            purchase_form.username = request.user.username
            purchase_form.save()
            
            return redirect('research_publication_list')
    
    context = {"is_user_authenticated":is_user_authenticated,
               "get_username":get_username,"research_purchase_form":research_purchase_form}
    
    return render(request, template, context)



def research_reports_subscription_list(request):
    
    """
    All users can view the research subscription list
    """
    
    get_username = request.user.username
    is_user_authenticated = request.user.is_authenticated
    is_user_subscribed = False
    # user_subscription_type = request.user.subscription_type
    is_user_subscription_active = False
    
    get_subscriptions = SARSubscription.objects.all()
    
    template = "research/research_reports_subscription_list.html"
    
    context = {"get_username":get_username,"is_user_authenticated":is_user_authenticated,
               "get_subscriptions":get_subscriptions}
    
    return render(request, template, context)


def research_report_purchase_list(request):
    """
    Only subscribed users can view this page
    """
    
    get_username = request.user.username
    is_user_authenticated = request.user.is_authenticated
    is_user_subscribed = False
    # user_subscription_type = request.user.subscription_type
    is_user_subscription_active = False
   
    get_current_research_reports = ResearchReport.objects.filter(is_report_current=True)
    
    template = "research/research_report_purchase_list.html"
    
    context = {"get_username":get_username,"is_user_authenticated":is_user_authenticated,
               "get_current_research_reports":get_current_research_reports}
    
    return render(request, template, context)





def sar_policy_list(request):

    """
    List policy documents on a table
    Using shutil to copy files from media to static to allow viewing of pdfs
    """
    is_user_authenticated = request.user.is_authenticated
    get_username = request.user.username

    get_policy_documents = SARPolicy.objects.all()
     
    if IS_DEV: 
        source = '/Users/jasonm/SEng/CompanyProjects/SAR/saratings/saratings/media/policy/'
        destination = '/Users/jasonm/Desktop/TestCopy/'
        
        for publication in get_policy_documents:
            
            print("upload_url:","http://127.0.0.1:8001"+publication.upload_file.url)
            
            publication.file_link = "http://127.0.0.1:8001"+publication.upload_file.url
            publication.save()
        
    
    if IS_PROD:
        
        source = os.path.join(BASE_DIR,'media/policy/') 
        destination = os.path.join(BASE_DIR,'static/assets/file/policy/')
        
        for publication in get_policy_documents:
            
            file_url = publication.upload_file.url      
            publication.file_link = "https://saratings.com"+file_url.replace("media","static/assets/file")
            publication.save()
        
    print("BASE_DIR:",BASE_DIR)

    # gather all files
    allfiles = os.listdir(source)
    
    # iterate on all files to move them to destination folder
    for fname in allfiles:
        shutil.copy2(os.path.join(source,fname), destination)    
    
    template = "policies/policy_list.html"
    
    context = {"get_policy_documents":get_policy_documents,
               "is_user_authenticated":is_user_authenticated} 
    
    return render(request, template, context)



def sector_commentary_list(request):

    """
    List policy documents on a table
    Using shutil to copy files from media to static to allow viewing of pdfs
    """
    is_user_authenticated = request.user.is_authenticated
    get_username = request.user.username

    get_sector_commentary_documents = SectorCommentary.objects.all().order_by('-id')
     
    if IS_DEV: 
        source = '/Users/jasonm/SEng/CompanyProjects/SAR/saratings/saratings/media/sector_commentary/'
        destination = '/Users/jasonm/Desktop/TestCopy/'
        
        for publication in get_sector_commentary_documents:
            
            print("upload_url:","http://127.0.0.1:8001"+publication.upload_file.url)
            
            publication.file_link = "http://127.0.0.1:8001"+publication.upload_file.url
            publication.save()
        
    
    if IS_PROD:
        
        source = os.path.join(BASE_DIR,'media/sector_commentary/') 
        destination = os.path.join(BASE_DIR,'static/assets/file/sector_commentary/')
        
        for publication in get_sector_commentary_documents:
            
            file_url = publication.upload_file.url      
            publication.file_link = "https://saratings.com"+file_url.replace("media","static/assets/file")
            publication.save()
        
    print("BASE_DIR:",BASE_DIR)

    # gather all files
    allfiles = os.listdir(source)
    
    # iterate on all files to move them to destination folder
    for fname in allfiles:
        shutil.copy2(os.path.join(source,fname), destination)    
    
    template = "commentary/sector_commentary_list.html"
    
    context = {"get_sector_commentary_documents":get_sector_commentary_documents,
               "is_user_authenticated":is_user_authenticated} 
    
    return render(request, template, context)


def issuer_commentary_list(request):
    
    """
    List policy documents on a table
    Using shutil to copy files from media to static to allow viewing of pdfs
    """
    is_user_authenticated = request.user.is_authenticated
    get_username = request.user.username

    get_issuer_commentary_documents = IssuerCommentary.objects.all().order_by('-id')
     
    if IS_DEV: 
        source = '/Users/jasonm/SEng/CompanyProjects/SAR/saratings/saratings/media/issuer_commentary/'
        destination = '/Users/jasonm/Desktop/TestCopy/'
        
        for publication in get_issuer_commentary_documents:
            
            print("upload_url:","http://127.0.0.1:8001"+publication.upload_file.url)
            
            publication.file_link = "http://127.0.0.1:8001"+publication.upload_file.url
            publication.save()
        
    
    if IS_PROD:
        
        source = os.path.join(BASE_DIR,'media/issuer_commentary/') 
        destination = os.path.join(BASE_DIR,'static/assets/file/issuer_commentary/')
        
        for publication in get_issuer_commentary_documents:
            
            file_url = publication.upload_file.url      
            publication.file_link = "https://saratings.com"+file_url.replace("media","static/assets/file")
            publication.save()
        
    print("BASE_DIR:",BASE_DIR)

    # gather all files
    allfiles = os.listdir(source)
    
    # iterate on all files to move them to destination folder
    for fname in allfiles:
        shutil.copy2(os.path.join(source,fname), destination)    
    
    template = "commentary/issuer_commentary_list.html"
    
    context = {"get_issuer_commentary_documents":get_issuer_commentary_documents,
               "is_user_authenticated":is_user_authenticated} 
    
    return render(request, template, context)



def annual_reports_list(request):

    """
    List annual reports on a table
    Using shutil to copy files from media to static to allow viewing of pdfs
    'Media' not working on production server
    """
    is_user_authenticated = request.user.is_authenticated
    get_username = request.user.username

    get_annual_reports = AnnualReport.objects.all().order_by('-publication_date')
     
    todays_date = datetime.date.today()
    
    if IS_DEV: 
        source = '/Users/jasonm/SEng/CompanyProjects/SAR/saratings/saratings/media/reports/'
        destination = '/Users/jasonm/Desktop/TestCopy/'
        
        for publication in get_annual_reports:
            
            print("upload_url:","http://127.0.0.1:8001"+publication.upload_file.url)
            
            publication.file_link = "http://127.0.0.1:8001"+publication.upload_file.url
            publication.save()
        
    
    if IS_PROD:
        # source = '/home/ubuntu/saratings/saratings/media/regulatory_articles/'
        # destination = '/home/ubuntu/saratings/saratings/static/assets/file/regulatory_articles/'
        
        source = os.path.join(BASE_DIR,'media/reports/annual_reports/') 
        destination = os.path.join(BASE_DIR,'static/assets/file/reports/annual_reports/')
        
        for report in get_annual_reports:
            
            file_url = report.upload_file.url      
            report.file_link = "https://saratings.com"+file_url.replace("media","static/assets/file")
            report.save()
        
    print("BASE_DIR:",BASE_DIR)

    try:
        # gather all files
        allfiles = os.listdir(source)
        
        # iterate on all files to move them to destination folder
        for fname in allfiles:
            shutil.copy2(os.path.join(source,fname), destination)
    except Exception as e:
        print("Error copying files:",e)
    
    template = "reports/annual_reports/annual_reports_list.html"
    
    context = {"get_annual_reports":get_annual_reports,
               "is_user_authenticated":is_user_authenticated} 
    
    return render(request, template, context)