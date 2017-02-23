from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Passive Aggressive Cost-Sharing Application v. 0.1")

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
