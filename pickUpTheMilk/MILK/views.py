from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Import user profile from models

from MILK.models import User, Group
from MILK.forms import UserForm, itemForm, groupForm, UserProfileForm
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

# # Work in progress...
@login_required
def userprofile(request):
    form = itemForm()

    if request.method == 'POST':
        form = itemForm(request.POST)



    if form.is_valid():
        item=form.save(commit=True)
        print(item)
    else:
        print(form.errors)



    response = render(request, 'MILK/userprofile.html', {'form':form})

    return response

@login_required
def creategroup(request):
    form = groupForm()

    if request.method == 'POST':
        form = groupForm(request.POST)

    if form.is_valid():
        group=form.save(commit=True)
        print(group)
    else:
        print(form.errors)

    response = render(request, 'MILK/create-group.html', {'form':form})
    return response

#work in progess, adding profle pic
def register(request):
    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #if forms are valid
        if profile_form.is_valid():

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered =True
        else:

            print(user_form.errors, profile_form.errors)
    else:

        profile_form =UserProfileForm()

    return render(request, 'registration/registration_form.html',{'profile_form': profile_form})