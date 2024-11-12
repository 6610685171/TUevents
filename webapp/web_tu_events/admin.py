from django.contrib import admin
from .models import Student,Announcement,Club,Lost,Found

class StudentAdmin(admin.ModelAdmin):
    list_display = ["student_id" ,"name" ,"email", "username"]
    search_fields = ('name', 'email', 'student_id', 'username')
    readonly_fields = ('password',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(user__is_staff=False, user__is_superuser=False)
    
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["title","categories" ,"date" , "start_date","end_date"]
    
class ClubAdmin(admin.ModelAdmin):
    list_display = ["title","origin" ,"enable_to_join"]
     
class LostAdmin(admin.ModelAdmin):
    list_display = ["items_name","lost_at" ,"contact" , "founded_status"]

class FoundAdmin(admin.ModelAdmin):
    list_display = ["items_name","found_at" ,"contact" , "founded_status"]
        
# Register your models here.     
admin.site.register(Student, StudentAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Lost, LostAdmin)
admin.site.register(Found, FoundAdmin)
