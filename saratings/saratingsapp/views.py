from django.shortcuts import render
from django.http import HttpResponse
import os

if 'F16' in os.uname()[1]:
    url_home = "http://localhost:8000/"
    
if 'aws' in os.uname()[2]:
    url_home = "http://saratings.com/"

def sar_home(request):
    
    """
    APP_DIRS = True, so template loader will search for templates inside saratingsapp/templates
    Sections are hidden using style attribute in html
    """
    
    template = "sar_home.html"
    
    return render(request, template)