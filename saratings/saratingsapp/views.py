from django.shortcuts import render
from django.http import HttpResponse

def sar_home(request):
    
    #APP_DIRS = True, so template loader will search for templates inside saratingsapp/templates
    template = "sar_home.html"
    
    return render(request, template)