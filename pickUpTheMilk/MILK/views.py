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

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if valid username/pw combo
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                # Inactive account, so no login
                return HttpResponse("Your account is disabled.")
        else:
            # Invalid login details
            print("Invalid login details:{0},{1}".format(username, password))
            return HttpResponse("Invalid login details supplied")

    else:
        # Request not a HTTP POST, so display login form
        return render(request, 'MILK/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    # Take user back to homepage
    return HttpResponseRedirect(reverse('home'))

def register(request):
    # Boolean to track registration status, will become True
    # if user is successfully registered.
    registered = False

    # HTTP request type must be POST
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            # Save their form to the database
            user = user_form.save()

            # Hash and save their password
            user.set_password(user.password)
            user.save()

            registered = True
        else:
            # Invalid form - print errors
            print(user_form.errors)

    else:
        # Not a HTTP POST, so render form using ModelForm instances
        user_form = UserForm()

    return render(request,
                    'MILK/register.html',
                    {'user_form': user_form,
                    'registered': registered})


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
