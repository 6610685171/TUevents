from . import views
from django.urls import path

urlpatterns = [
    path("", views.home , name="home" ),
    path("about", views.about, name="about"),
    path("login", views.login, name="login"),
    path("events/all_events.html", views.all_events, name="all_events"),
    path("events/<int:announcement_id>/", views.event_detail, name="event-detail"),
    path('events/<str:category>/', views.category_events, name='category_events')
]