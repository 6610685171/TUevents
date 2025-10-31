from django.http import HttpResponse
from django.shortcuts import render
from ..models import *

def all_club_list_admin(request):
    if not request.user.is_superuser:
        return HttpResponse("You do not have permission to view this page.")

    clubs = Club.objects.exclude(origin="tu")  # แสดงทุก clubs ยกเว้นของมอ
    faculty_name = "All Faculties"  # สำหรับแสดงว่าเป็นทุกคณะ

    # กรองประกาศที่เกี่ยวข้องกับ clubs
    all_club_announcements = Announcement.objects.filter(categories="clubs").order_by(
        "-date"
    )

    # กรอง TU clubs โดยใช้ origin="tu"
    tu_clubs = Club.objects.filter(origin="tu")
    tu_club_announcements = all_club_announcements.filter(club__in=tu_clubs)

    faculty_club_announcements = all_club_announcements.filter(club__in=clubs)

    if request.user.is_authenticated:
        # ถ้าผู้ใช้งานล็อกอินให้หากิจกรรมที่ผู้ใช้งานสนใจ
        interested_events = list(
            Interest.objects.filter(user=request.user).values_list(
                "announcement_id", flat=True
            )
        )
    else:
        interested_events = []

    # ส่งข้อมูลไปยังเทมเพลต
    return render(
        request,
        "clubs/clubs_announcement_list_admin.html",
        {
            "all_club_announcements": all_club_announcements,
            "tu_club_announcements": tu_club_announcements,
            "faculty_club_announcements": faculty_club_announcements,
            "clubs": clubs,  # Clubs ตามคณะ หรือ ทุกคณะสำหรับ admin
            "tu_clubs": tu_clubs,  # Clubs ของ TU
            "faculty_name": faculty_name,  # ชื่อคณะ
            "interested_events": interested_events,
        },
    )


def clubs_by_faculty_admin(request):
    if not request.user.is_superuser:
        return HttpResponse("You do not have permission to view this page.")

    # กรองออกเฉพาะ clubs ที่มี origin เป็น 'tu'
    clubs = Club.objects.exclude(origin="tu")

    clubs = Club.objects.exclude(origin="tu")  # กรองออกเฉพาะ clubs ที่มี origin เป็น 'tu'
    faculty_name = "All Faculties"  # สำหรับ admin จะดูข้อมูลทุกคณะ

    # ดึงประกาศทั้งหมดที่เกี่ยวข้องกับคลับ
    all_club_announcements = Announcement.objects.filter(
        categories="clubs", club__in=clubs  # กรองประกาศที่เชื่อมโยงกับคลับ
    ).order_by("-date")

    # ตรวจสอบกิจกรรมที่ผู้ใช้งานสนใจ
    if request.user.is_authenticated:
        interested_events = list(
            Interest.objects.filter(user=request.user).values_list(
                "announcement_id", flat=True
            )
        )
        interested_events = list(
            Interest.objects.filter(user=request.user).values_list(
                "announcement_id", flat=True
            )
        )
    else:
        interested_events = []
        interested_events = []

    # ส่งข้อมูลไปยังเทมเพลต
    return render(
        request,
        "clubs/faculty_clubs_admin.html",
        {
            "clubs": clubs,
            "faculty_name": faculty_name,
            "announcements": all_club_announcements,  # ส่งประกาศไปยังเทมเพลต
            "interested_events": interested_events,
        },
    )