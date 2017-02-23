from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Import user profile from models

from MILK.models import User

def home(request):

    response = render(request, 'MILK/home.html', {})
    return response

def login(request):
    return HttpResponse("PLACEHOLDER: Login page")

def register(request):
    return HttpResponse("PLACEHOLDER: Register now! (don't know why you'd want to...)")

def sitemap(request):
    return HttpResponse("PLACEHOLDER: Not present- the greatest sitemap the world has ever seen")

def contact(request):
    return HttpResponse("PLACEHOLDER: Contact one of the 5 fools behind this site")

def about(request):
    return HttpResponse("PLACEHOLDER: About this broken web app")

def creategroup(request):
    return HttpResponse("PLACEHOLDER: Create a new group")

# # Work in progress...
# def profile(request, profileID):
#     profileID = Profile.objects.get(profileID)
#     return HttpResponse("PLACEHOLDER: Your profile")
