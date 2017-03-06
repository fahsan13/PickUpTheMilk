from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

# Import user profile from models

from MILK.models import User, Group, Item
from MILK.forms import UserForm, itemForm, groupForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def home(request):

    #Placed here assuming we're keeping lists on home page? if I'm wrong, easy to change
    item_list = Item.objects
    context_dict = {'Items': item_list}

    response = render(request, 'MILK/home.html', context_dict)
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
