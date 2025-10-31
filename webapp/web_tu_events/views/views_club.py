from ..models import Club,Announcement,Interest
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from ..forms import ClubAnnouncementForm
from django.contrib import messages
from .utils import *
from django.http import HttpResponse

def tu_clubs_list(request):
    # ดึงข้อมูล Club ที่มี origin="tu"
    tu_clubs = Club.objects.filter(origin="tu")
    # ดึงประกาศที่อยู่ในหมวด clubs และเป็นของ TU club เท่านั้น
    tu_club_announcements = Announcement.objects.filter(
        categories="clubs",
        club__in=tu_clubs
    ).select_related("club").order_by("-date")  # preload ข้อมูล club ลดจำนวน query

    if request.user.is_authenticated:
        # ถ้าผู้ใช้งานล็อกอินให้หากิจกรรมที่ผู้ใช้งานสนใจ
        interested_events = list(
            Interest.objects.filter(user=request.user).values_list(
                "announcement_id", flat=True
            )
        )
    else:
        interested_events = []

    # ส่งข้อมูล Club ไปยังเทมเพลต
    return render(
        request,
        "clubs/tu_clubs.html",
        {
            "clubs": tu_clubs,
            "tu_club_announcements": tu_club_announcements,
            "interested_events": interested_events,
        },
    )


def club_detail(request, club_id):
    # ดึงข้อมูล Club ตาม club_id
    club = get_object_or_404(Club, id=club_id)

    # ดึงข้อมูล Announcement ที่มีการเชื่อมโยงกับ Club นี้
    announcements = Announcement.objects.filter(club=club)

    if request.user.is_authenticated:
        # ถ้าผู้ใช้งานล็อกอินให้หากิจกรรมที่ผู้ใช้งานสนใจ
        interested_events = list(
            Interest.objects.filter(user=request.user).values_list(
                "announcement_id", flat=True
            )
        )
    else:
        interested_events = []

    # ส่งข้อมูล Club และ Announcement ไปยังเทมเพลต
    return render(
        request,
        "clubs/club_detail.html",
        {
            "club": club,
            "announcements": announcements,
            "interested_events": interested_events,
        },
    )
    
# สมาชิกชุมนุมโพสประกาศกิจกรรม
@login_required
def club_create_announcement(request):
    if not request.user.student.club:
        return redirect("home")

    if request.method == "POST":
        form = ClubAnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.student = request.user.student
            announcement.categories = "clubs"
            announcement.save()
            messages.success(request, "Announcement created successfully!")

            # Redirect ไปที่หน้า club_announcement_list
            return redirect("event-detail", announcement_id=announcement.id)
    else:
        form = ClubAnnouncementForm()

    return render(request, "clubs/create_club_post.html", {"form": form})


# รวมโพสจากทุกclub
def all_club_list(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to log in first.")
        return redirect("login")

    student = request.user.student  # ดึง Student object จาก User ที่ล็อกอินอยู่

    # ดึงรหัสคณะจาก student_id (ตัวเลขที่ 3-4)
    student_id = str(student.student_id)  # ดึง student_id
    faculty_code = student_id[2:4]
    
    # แปลงรหัสคณะเป็นชื่อคณะ    
    faculty_name = get_faculty_name(get_faculty_by_code(faculty_code))
    
    # ดึง clubs ตามคณะ    
    clubs = Club.objects.filter(origin=get_faculty_by_code(faculty_code))

    # กรองประกาศที่เกี่ยวข้องกับ clubs
    all_club_announcements = Announcement.objects.filter(categories="clubs").order_by(
        "-date"
    )

    # กรอง TU clubs โดยใช้ origin="tu"
    tu_clubs = Club.objects.filter(origin="tu")
    tu_club_announcements = all_club_announcements.filter(club__in=tu_clubs)

    # แยกประกาศตาม faculty
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
        "clubs/clubs_announcement_list.html",
        {
            "all_club_announcements": all_club_announcements,
            "tu_club_announcements": tu_club_announcements,
            "faculty_club_announcements": faculty_club_announcements,
            "clubs": clubs,  # Clubs ตามคณะ หรือ ทุกคณะสำหรับ admin
            "tu_clubs": tu_clubs,  # Clubs ของ TU
            "faculty_name": faculty_name,  # ชื่อคณะ
            "interested_events": interested_events,
            "interested_events": interested_events,
        },
    )

def clubs_by_faculty(request):
    # ตรวจสอบว่าผู้ใช้เข้าสู่ระบบแล้วหรือยัง
    if not request.user.is_authenticated:
        return HttpResponse("You need to log in first.")

    # ดึง student_id จากผู้ใช้ที่ล็อกอิน
    student = request.user.student  
    student_id = str(student.student_id)  # แปลง student_id เป็นสตริง

    # ดึงรหัสคณะจาก student_id (ตัวเลขที่ 3-4)
    faculty_code = student_id[2:4]
    # แปลงรหัสคณะเป็นชื่อคณะ
    faculty_name = get_faculty_name(get_faculty_by_code(faculty_code))

    # กรอง Club ตามคณะ
    clubs = Club.objects.filter(origin=get_faculty_by_code(faculty_code))

    # ดึงประกาศที่เกี่ยวข้องกับคลับในคณะนี้
    all_club_announcements = Announcement.objects.filter(
        categories="clubs", club__in=clubs  # กรองประกาศที่เชื่อมโยงกับคลับในคณะนี้
    ).order_by("-date")

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
        "clubs/faculty_clubs.html",
        {
            "clubs": clubs,
            "faculty_name": faculty_name,
            "announcements": all_club_announcements,  # ส่งประกาศไปยังเทมเพลต
            "interested_events": interested_events,
        },
    )

def club_post_history(request):
    # ตรวจสอบว่าผู้ใช้เข้าสู่ระบบแล้วหรือยัง
    if not request.user.is_authenticated:
        return HttpResponse("You need to log in first.")    
    # ตรวจสอบว่า user มี student หรือไม่
    student = getattr(request.user, "student", None)

    if student:
        # ดึงประกาศทั้งหมดที่ผู้ใช้โพสต์
        announcements = Announcement.objects.filter(student=student).order_by("-date")
    else:
        announcements = []  # ถ้าไม่มี student ให้ return list ว่าง

    return render(
        request, "my_account/club_post_history.html", {"announcements": announcements}
    )

