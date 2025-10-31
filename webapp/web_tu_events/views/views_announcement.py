from ..models import Announcement,Club,Interest
from ..forms import ClubAnnouncementForm
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

# home page
def home(request):
    all_announcement = Announcement.objects.exclude(categories="clubs").exclude(
        categories="alerts"
    ) # ดึงทุกeventยกเว้นclub,alerts
    tu_clubs = Club.objects.filter(origin="tu") # ดึงเฉพาะชุมนุมมหาลัย
    alerts = Announcement.objects.filter(categories="alerts") # ดึงเฉพาะ alerts
    all_club_announcements = Announcement.objects.filter(categories="clubs").order_by(
        "-date"
    )

    if request.user.is_authenticated:
        # ถ้าผู้ใช้ล็อกอินอยู่ให้ดึงรายการกิจกรรมที่ผู้ใช้กดสนใจ
        interested_events = list(
            Interest.objects.filter(user=request.user).values_list(
                "announcement_id", flat=True
            )
        )
    else:
        interested_events = []

    return render(
        request,
        "home.html",
        {
            "all_announcement": all_announcement,
            "clubs": tu_clubs,
            "alerts": alerts,
            "all_club_announcements": all_club_announcements,
            "interested_events": interested_events,
        },
    )

#about page
def about(request):
    return render(request, "about.html")

#all events page
def all_events(request):
    all_announcement = Announcement.objects.exclude(categories="clubs").exclude(
        categories="alerts"
    ) # แสดงเฉพาะกิจกรรมที่ไม่ได้มาจากชุมนุม

    if request.user.is_authenticated:
        # ถ้าผู้ใช้งานล็อกอินให้หากิจกรรมที่ผู้ใช้งานสนใจ
        interested_events = list(
            Interest.objects.filter(user=request.user).values_list(
                "announcement_id", flat=True
            )
        )
    else:
        interested_events = []

    return render(
        request,
        "events/all_events.html",
        {
            "all_announcement": all_announcement,
            "interested_events": interested_events,
        },
    )

# each event detail page
def event_detail(request, announcement_id):
    # ดึงประกาศจากฐานข้อมูล
    announcement = get_object_or_404(Announcement, id=announcement_id)

    if request.user.is_authenticated:
        interested_event_ids = Interest.objects.filter(user=request.user).values_list(
            "announcement__id", flat=True
        )
    else:
        interested_event_ids = []

    return render(
        request,
        "events/event_detail.html",
        {
            "announcement": announcement,
            "interested_event_ids": interested_event_ids,
        },
    )

# category of events
def category_events(request, category):
    announcement = Announcement.objects.filter(categories=category)
    if request.user.is_authenticated:
        # ถ้าผู้ใช้งานล็อกอินให้หากิจกรรมที่ผู้ใช้งานสนใจ
        interested_events = list(
            Interest.objects.filter(user=request.user).values_list(
                "announcement_id", flat=True
            )
        )
    else:
        interested_events = []
    return render(
        request,
        "events/category_events.html",
        {
            "announcement": announcement,
            "category": category,
            "interested_events": interested_events,
        },
    )
    
def toggle_interest(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    user = request.user

    # ตรวจสอบว่าผู้ใช้งานสนใจอยู่หรือไม่
    if Interest.objects.filter(user=request.user, announcement=announcement).exists():
        # ถ้าผู้ใช้งานเคยสนใจกิจกรรมนี้แล้ว ให้ยกเลิก
        Interest.objects.filter(user=request.user, announcement=announcement).delete()
        messages.success(request, "You have unmarked this event as interested.")
    else:
        # ถ้าผู้ใช้งานยังไม่สนใจ ให้กดสนใจ
        Interest.objects.create(user=request.user, announcement=announcement)
        messages.success(request, "You have marked this event as interested.")

    referer = request.META.get("HTTP_REFERER", "/")
    return HttpResponseRedirect(referer)

def event_edit(request, announcement_id):
    # ดึงประกาศที่ต้องการแก้ไขจากฐานข้อมูล
    announcement = get_object_or_404(Announcement, id=announcement_id)

    # ตรวจสอบสิทธิ์ของผู้ใช้ว่าเป็นเจ้าของประกาศ
    if announcement.student != request.user.student:
        # ถ้าไม่ใช่เจ้าของประกาศจะไม่สามารถแก้ไขได้
        return redirect("event-detail", announcement_id=announcement_id)

    # ถ้าได้requestแบบ POST ให้บันทึกข้อมูลที่แก้ไข
    if request.method == "POST":
        form = ClubAnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()  # บันทึกข้อมูลที่แก้ไข
            # กลับไปที่หน้ารายละเอียดของประกาศที่แก้ไข
            return redirect(
                "event-detail", announcement_id=announcement.id
            )  # กลับไปที่หน้ารายละเอียดของประกาศที่แก้ไข
    else:
        # กรณีที่แสดงฟอร์มให้กรอกข้อมูลใหม่
        form = ClubAnnouncementForm(instance=announcement)

    # ส่งฟอร์มและประกาศไปที่เทมเพลต
    return render(
        request,
        "events/edit_event.html",
        {
            "form": form,
            "announcement": announcement,
        },
    )

def event_delete(request, announcement_id):
    # ดึงประกาศที่ต้องการลบ
    announcement = get_object_or_404(Announcement, id=announcement_id)

    # ตรวจสอบว่าเป็นผู้สร้างประกาศนี้หรือไม่
    if announcement.student == request.user.student:
        announcement.delete()  # ลบประกาศจากฐานข้อมูล
        messages.success(request, "Announcement deleted successfully!")
        return redirect("clubs_announcement_list")
    return redirect("clubs_announcement_list")

