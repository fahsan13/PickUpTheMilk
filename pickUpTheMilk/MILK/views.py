from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from MILK.models import User, UserProfile, Group, Item
from MILK.forms import itemForm, groupForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# View for second page in 2-step registration process. Required as we're
# using registration-redux package and still want to populate the UserProfile
# fields --(initial) balance and picture-- when the user registers.
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

# View for the home page of the site.
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
    # We will then pass this to profile.html
    userprofile = UserProfile.objects.get_or_create(user=user)[0]




    form = itemForm()

    if request.method == 'POST':
        form = itemForm(request.POST)

        if form.is_valid():
            item=form.save(commit=True)
            group = user.groups.all(id=0)
            item.groupBuying = request.POST[group]
            item.save()

            print(item)

        else:
            print(form.errors)

     # List not populating on usder profile page, not sure why yet

    item_list = Item.objects.order_by('id')
    context_dict = {'Items': item_list}
    response = render(request, 'MILK/userprofile.html', context_dict, {'form':form, 'selecteduser':user, 'userprofile': userprofile,})
    return response

# View for create-group.html.
# Need to implement error handling for when
# group with a given name already exists IF
# we don't later refactor this so that we use
# group IDs in URLs instead of unique group names but thats
# a bit harder and I can't be bothered right now.
@login_required
def creategroup(request):

    form = groupForm(request.POST)

    # Get currently logged in user.
    user=request.user

    if request.method == 'POST':
        form = groupForm(request.user, request.POST)
        if form.is_valid():
            # Save the group
            group=form.save(commit=True)
            # Get group name from form; field within form containing name is 'group'!
            groupname=form.cleaned_data['group']
            # Add user to this newly created group :)
            user.groups.add(groupname)
            print(group)
            return userprofile(request, user.username)
        else:
            print(form.errors)

    response = render(request, 'MILK/create-group.html', {'form':form})
    return response

def userprofile(request, username):

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('home')

    # Retrieve UserProfile extension (containing balance/picture).
    # We will then pass this to profile.html
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

# View for communal group page
# NOTE: urls for a group can't have spaces yet - regex doesn't
# account for them. May need to clean group names to remove spaces
# when they're created.
@login_required
def grouppage(request, groupname):
    # Work in progress...
    try:
        group = Group.objects.get(name=groupname)
    except Group.DoesNotExist:
        return redirect('home')

    response = render(request, 'MILK/grouppage.html', {'group':group})
    return response
