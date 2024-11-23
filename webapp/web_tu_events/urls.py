from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("events/all_events.html", views.all_events, name="all_events"),
    path("events/<int:announcement_id>/", views.event_detail, name="event-detail"),
    path("events/<str:category>/", views.category_events, name="category_events"),
    path('found/create/', views.create_found_item, name='create_found_item'),
    path('found/list/', views.found_items_list, name='found_items_list'), 
    path('lost/create/', views.create_lost_item, name='create_lost_item'),
    path('lost/list/', views.lost_items_list, name='lost_items_list'),
    path('clubs/club_create_announcement/', views.club_create_announcement, name='clubs_create_announcement'),
    path('clubs/club_announcement_list/', views.all_club_announcement_list, name='clubs_announcement_list'),
    path('lost/<int:lost_id>/', views.lost_detail, name='lost_detail'),
    path('found/<int:found_id>/', views.found_detail, name='found_detail'),
    path('lost/edit_lost_item/<lost_id>', views.lost_edit, name="lost_edit"),
    path('found/edit_found_item/<found_id>', views.found_edit, name="found_edit")
]
