from django.contrib import admin
from .models import Student,Announcement,Club,Lost,Found,Interest
from django.db.models import Count
    
class StudentAdmin(admin.ModelAdmin):
    list_display = ["username" ,"name" ,"email", "student_id","club"]
    search_fields = ('name', 'email', 'student_id', 'username')
    # readonly_fields = ('password',)
            
    # แสดงเฉพาะข้อมูลของuserที่ไม่ใช่admin    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(user__is_staff=False, user__is_superuser=False)
    
class InterestedUsersViewInline(admin.TabularInline):
    model = Interest
    extra = 0  
    readonly_fields = ('user', 'announcement', 'interested_at')
    can_delete = False
    
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["title","categories" ,"club" , "start_date","end_date", "interest_count"]
    inlines = [InterestedUsersViewInline]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # เพิ่ม field 'interest_count' ไปยัง queryset
        return queryset.annotate(interest_count=Count('interested_users'))

    # แสดงจำนวนคนที่สนใจในแต่ละกิจกรรม
    def interest_count(self, obj):
        return obj.interest_count  # เข้าถึง 'interest_count' ที่เรา annotate ไว้
    interest_count.short_description = 'Number of Interested Users' 
    
class ClubAdmin(admin.ModelAdmin):
    list_display = ["title","origin" ,"enable_to_join"]
     
class LostAdmin(admin.ModelAdmin):
    list_display = ["items_name","lost_at" ,"contact" , "founded_status"]

class FoundAdmin(admin.ModelAdmin):
    list_display = ["items_name","found_at" ,"contact" , "founded_status"]
    
# class InterestAdmin(admin.ModelAdmin):
#     list_display = ('user', 'announcement', 'interested_at')
#     search_fields = ('user__username', 'announcement__title')


        
# Register your models here.     
admin.site.register(Student, StudentAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Lost, LostAdmin)
admin.site.register(Found, FoundAdmin)
# admin.site.register(Interest, InterestAdmin)
