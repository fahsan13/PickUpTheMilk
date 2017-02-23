from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to Passive Aggressive Cost-Sharing Application v. 0.1")
