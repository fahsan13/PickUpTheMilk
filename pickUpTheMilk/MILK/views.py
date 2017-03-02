from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Import user profile from models

from MILK.models import User
from MILK.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def home(request):
    response = render(request, 'MILK/home.html', {})
    return response

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
def userprofile(request, userID):
    userID = User.objects.get(userID)
    return render(request, 'MILK/userprofile.html', userID)
