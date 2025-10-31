from ..forms import StudentProfileForm
from ..models import Interest,Found,Lost
from django.shortcuts import redirect,render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def my_account(request):
    student = getattr(request.user, "student", None)

    if not student:
        # ป้องกันกรณี user ไม่มี student profile (เช่น admin หรือ staff)
        return HttpResponse("No student profile found for this user.", status=404)

    return render(request, "my_account/personal_info.html", {"student": student})

@login_required
def edit_profile(request):
    # ดึงข้อมูล Student ของ user ที่ล็อกอินอยู่
    student = getattr(request.user, "student", None)
    if not student:
        # ป้องกัน error ถ้า user ไม่มี student profile
        return HttpResponse("No student profile found for this user.", status=404)

    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("my_account")  # กลับไปหน้าโปรไฟล์หลังบันทึก
    else:
        form = StudentProfileForm(instance=student)

    context = {"form": form, "student": student}
    return render(request, "my_account/edit_profile.html", context)

@login_required
def my_events(request):
    user_interests = (
        Interest.objects
        .filter(user=request.user)
        .select_related("announcement")  # ลดจำนวน query
        .order_by("-announcement__date")  # เรียงตามวันที่กิจกรรม (optional)
    )
    context = {"interested_events": user_interests}
    return render(request, "my_account/my_events.html", context)


@login_required
def lost_found_history(request):
    student = getattr(request.user, "student", None)
    lost_items, found_items = [], []

    if student:
        lost_items = (Lost.objects.filter(student=student).order_by("founded_status", "-id"))
        found_items = (Found.objects.filter(student=student).order_by("founded_status", "-id"))

    context = {
        "lost_items": lost_items,
        "found_items": found_items,
    }
    return render(request, "my_account/lost_found_history.html", context)
