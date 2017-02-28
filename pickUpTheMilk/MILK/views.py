from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Import user profile from models

from MILK.models import User

def home(request):

    response = render(request, 'MILK/home.html', {})
    return response

def login(request):
    response = render(request, 'MILK/login.html', {})
    return response

def register(request):
    return render(request, 'MILK/register.html', {})

def sitemap(request):
    response = render(request, 'MILK/sitemap.html', {})
    return response

def contact(request):
    return render(request, 'MILK/contact.html', {})

def about(request):
    return render(request, 'MILK/about.html', {})

def creategroup(request):
    return HttpResponse("PLACEHOLDER: Create a new group")

# # Work in progress...
# def profile(request, profileID):
#     profileID = Profile.objects.get(profileID)
#     return HttpResponse("PLACEHOLDER: Your profile")
