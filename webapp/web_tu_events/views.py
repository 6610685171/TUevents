from django.shortcuts import render, redirect
from .models import Announcement
# Create your views here.


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def login(request):
    return render(request, "login.html")

def events(request):
    all_announcement = Announcement.objects.all()
    return render(request, "events.html", {'all_announcement': all_announcement})