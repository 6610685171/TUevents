from django.shortcuts import render, redirect, get_object_or_404
from .models import Announcement
# Create your views here.


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def login(request):
    return render(request, "login.html")

def all_events(request):
    all_announcement = Announcement.objects.all()
    return render(request, "events/all_events.html", {'all_announcement': all_announcement})

def event_detail(request, announcement_id):
    announcement = get_object_or_404(Announcement, id = announcement_id)
    return render(request, "events/event_detail.html", {"announcement": announcement})

def category_events(request, category):
    announcement = Announcement.objects.filter(categories=category)
    return render(request, "events/category_events.html", {"announcement": announcement, "category": category})