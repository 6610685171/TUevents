from . import views
from django.urls import path

urlpatterns = [
    path("", views.home , name="home" ),
    path("about", views.about, name="about"),
    path("login", views.login, name="login"),
    path("events/events.html", views.events, name="events"),
    path("events/<int:announcement_id>/", views.event_detail, name="event-detail")
]