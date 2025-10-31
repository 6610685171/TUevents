from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("events/all_events/", views.all_events, name="all_events"),
    path("events/<int:announcement_id>/", views.event_detail, name="event-detail"),
    path("events/<str:category>/", views.category_events, name="category_events"),
    path('events/<int:announcement_id>/edit/', views.event_edit, name='event-edit'),
    path('events/<int:announcement_id>/delete/', views.event_delete, name='event-delete'),     
    path('announcement/<int:announcement_id>/interest/', views.toggle_interest, name='toggle_interest'),

    path("lost/list/", views.lost_items_list, name="lost_items_list"),
    path("lost/<int:lost_id>/", views.lost_detail, name="lost_detail"),
    path("lost/create/", views.create_lost_item, name="create_lost_item"),
    path("lost/edit_lost_item/<int:lost_id>/", views.lost_edit, name="lost_edit"),
    path('lost/delete/<int:lost_id>/', views.lost_delete, name='lost_delete'),    
    path("found/list/", views.found_items_list, name="found_items_list"),
    path("found/<int:found_id>/", views.found_detail, name="found_detail"),
    path("found/create/", views.create_found_item, name="create_found_item"),
    path("found/edit_found_item/<int:found_id>", views.found_edit, name="found_edit"),
    path('found/delete/<int:found_id>/', views.found_delete, name='found_delete'),

    path("clubs/club_announcement_list/",views.all_club_list,name="clubs_announcement_list"),
    path('clubs/tu_clubs', views.tu_clubs_list, name="tu_clubs"),
    path('clubs/faculty_clubs', views.clubs_by_faculty, name='clubs_by_faculty'),    
    path('clubs/club_detail/<club_id>', views.club_detail , name="club_detail"),
    path("clubs/club_create_announcement/",views.club_create_announcement,name="clubs_create_announcement"),

    path('my_account/personal_info', views.my_account, name='my_account'), 
    path('edit_profile/', views.edit_profile, name='edit_profile'),  
    path('my_account/lost_found_history', views.lost_found_history, name='lost_found_history'),
    path('my_account/my_events', views.my_events , name='my_events'),
    path('my_account/my_club_post_history/', views.club_post_history, name='my_club_post_history'),   

    path("clubs/club_announcement_list_admin/",views.all_club_list_admin,name="clubs_announcement_list_admin"), 
    path('clubs/faculty_clubs_admin', views.clubs_by_faculty_admin, name='clubs_by_faculty_admin'),               
]
