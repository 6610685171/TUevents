from django.contrib import admin
from .models import Student,Announcement,Club,Lost,Found

class StudentInfo(admin.ModelAdmin):
    list_display = ["email","name" ,"student_id" , "username"]
    
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["title","categories" ,"date" , "start_date","end_date"]
    
class ClubAdmin(admin.ModelAdmin):
    list_display = ["title","origin" ,"enable_to_join"]
     
class LostAdmin(admin.ModelAdmin):
    list_display = ["items_name","lost_at" ,"contact" , "founded_status"]

class FoundAdmin(admin.ModelAdmin):
    list_display = ["items_name","found_at" ,"contact" , "founded_status"]
        
# Register your models here.     
admin.site.register(Student, StudentInfo)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Lost, LostAdmin)
admin.site.register(Found, FoundAdmin)
