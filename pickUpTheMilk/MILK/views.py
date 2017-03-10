from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from MILK.models import User, UserProfile, Group, Item
from MILK.forms import itemForm, groupForm, UserProfileForm
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

# TO-DO - list all members of a group
# Let admin of a group add other members
# This could be done by checking against group details
# if (currentuser == administrator)
#   display links to allow them to add users@login_required
def userprofile(request, username):

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('home')

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

    response = render(request, 'MILK/userprofile.html', {'form':form, 'selecteduser':user, 'userprofile': userprofile,})

    return response

# TO-DO- figure out a way to get the 'create group' link to disappear from
# a user's page if they already have a group

@login_required
def creategroup(request):

    # Don't know if this should be here but it throws up errors after first 'if'
    form = groupForm(request.user, request.POST)

    # Get currently logged in user.
    user=request.user

    if request.method == 'POST':
        # form = groupForm(request.user, request.POST)
        if form.is_valid():
            # Save the group
            group=form.save(commit=True)
            # Get group name from form; field within form containing name is 'group'!
            groupname=form.cleaned_data['group']
            # Add user to this newly created group :)
            user.groups.add(groupname)
            print(group)
        else:
            print(form.errors)

    response = render(request, 'MILK/create-group.html', {'form':form})
    return response
