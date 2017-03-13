from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

# Import user profile from models

from MILK.models import User, UserProfile, Group, Item
from MILK.forms import UserForm, itemForm, groupForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('home')
        else:
            print(form.errors)
    context_dict = {'form':form}

    return render(request, 'MILK/profile_registration.html', context_dict)

def home(request):
    # Placed here assuming we're keeping lists on home page? if I'm wrong, easy to change
    item_list = Item.objects.order_by('id')
    app_url = request.path

    context_dict = {'Items': item_list, 'app_url': app_url }
    response = render(request, 'MILK/home.html', context_dict)
    return response

def sitemap(request):
    app_url = request.path
    response = render(request, 'MILK/sitemap.html', {'app_url': app_url})
    return response

def contact(request):

    app_url = request.path
    return render(request, 'MILK/contact.html', {'app_url': app_url})

def about(request):
    app_url = request.path
    return render(request, 'MILK/about.html', {'app_url': app_url})



# # Work in progress... See Chapter 15 of TwD!
@login_required
def userprofile(request, username):

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    # Retrieve UserProfile extension (containing balance/picture).
    # We will then pass this to the profile.html
    userprofile = UserProfile.objects.get_or_create(user=user)[0]

    form = itemForm()

    if request.method == 'POST':
        form = itemForm(request.POST)

        if form.is_valid():
            item=form.save(commit=True)
            print(item)
        else:
            print(form.errors)
    app_url = request.path
    response = render(request, 'MILK/userprofile.html', {'form':form, 'selecteduser':user, 'userprofile': userprofile})

    return response

@login_required
def creategroup(request):
    form = groupForm()

    if request.method == 'POST':
        form = groupForm(request.POST, user=request.user)
        if form.is_valid():
            group=form.save(commit=True)
            print(group)
        else:
            print(form.errors)

    response = render(request, 'MILK/create-group.html', {'form':form})
    return response
