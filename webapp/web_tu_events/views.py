from .models import Announcement, Found, Lost, Interest, Club
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from .forms import FoundForm, LostForm, ClubAnnouncementForm, StudentProfileForm
from django.http import HttpResponseRedirect,HttpResponse

# Create your views here.
def home(request):
    all_announcement = Announcement.objects.exclude(categories="clubs").exclude(categories="alerts")
    clubs = Club.objects.filter(origin="tu")
    alerts = Announcement.objects.filter(categories="alerts")  
    all_club_announcements = Announcement.objects.filter(categories="clubs").order_by("-date")
     
    if request.user.is_authenticated:
        # ถ้าผู้ใช้งานล็อกอินให้หากิจกรรมที่ผู้ใช้งานสนใจ
        interested_events = list(Interest.objects.filter(user=request.user).values_list('announcement_id', flat=True))
    else:
        interested_events = []
             
    return render(request, "home.html", {'all_announcement': all_announcement, 'clubs': clubs, 'alerts':alerts, 'all_club_announcements' : all_club_announcements,             "interested_events": interested_events,
 })


def about(request):
    return render(request, "about.html")


# def login(request):
#     return render(request, "login.html")


def all_events(request):
    all_announcement = Announcement.objects.exclude(categories="clubs").exclude(categories="alerts")
    
    if request.user.is_authenticated:
        # ถ้าผู้ใช้งานล็อกอินให้หากิจกรรมที่ผู้ใช้งานสนใจ
        interested_events = list(Interest.objects.filter(user=request.user).values_list('announcement_id', flat=True))
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



def event_detail(request, announcement_id):
    # ดึงประกาศจากฐานข้อมูล
    announcement = get_object_or_404(Announcement, id=announcement_id)

    # ตรวจสอบว่า announcement.student เชื่อมโยงกับ request.user.student หรือไม่
    if hasattr(announcement, 'student') and hasattr(request.user, 'student'):
        print(f"Announcement student: {announcement.student}")
        print(f"Logged-in user student: {request.user.student}")

        # เปรียบเทียบว่าเป็นคนเดียวกันหรือไม่
        if announcement.student == request.user.student:
            print("This is the student's announcement!")

    if request.user.is_authenticated:
        interested_event_ids = Interest.objects.filter(user=request.user).values_list('announcement__id', flat=True)
    else:
        interested_event_ids = []

    return render(request, "events/event_detail.html", {
        "announcement": announcement,
        "interested_event_ids": interested_event_ids,
    })


def category_events(request, category):
    announcement = Announcement.objects.filter(categories=category)
    if request.user.is_authenticated:
        # ถ้าผู้ใช้งานล็อกอินให้หากิจกรรมที่ผู้ใช้งานสนใจ
        interested_events = list(Interest.objects.filter(user=request.user).values_list('announcement_id', flat=True))
    else:
        interested_events = []
    return render(
        request,
        "events/category_events.html",
        {"announcement": announcement, "category": category, "interested_events": interested_events,
},
    )

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "Invalid username.")
                return redirect("login")

            # ตรวจสอบรหัสผ่าน
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, "Invalid password.")
                return redirect("login")

            # เมื่อเข้าสู่ระบบสำเร็จ
            login(request, user)

            # ตรวจสอบว่าเป็น superuser หรือไม่
            if user.is_superuser:
                return redirect("admin:index")  # ไปที่หน้า admin ของ Django

            # ถ้าไม่ใช่ superuser, ตรวจสอบว่ามี 'next' หรือไม่
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect("home")  # หรือหน้าอื่นที่ต้องการให้ผู้ใช้เข้า

        else:
            messages.error(request, "Both fields are required.")
            return redirect("login")
    
    else:
        form = AuthenticationForm()

    # ส่งแบบฟอร์มกลับไปที่เทมเพลต
    return render(request, "login.html", {"form": form})


# โพสของที่เจอ
def create_found_item(request):
    if request.method == "POST":
        form = FoundForm(request.POST, request.FILES)
        if form.is_valid():
            found_item = form.save(commit=False)
            found_item.student = request.user.student
            found_item.save()
            return redirect("found_items_list")
    else:
        form = FoundForm()

    return render(request, "found/create_found_item.html", {"form": form})


# หน้ารวมของที่เจอ
def found_items_list(request):
    found_items = Found.objects.all().order_by('founded_status','-id')
    return render(request, "found/found_items_list.html", {"found_items": found_items})


# โพสของหาย
def create_lost_item(request):
    if request.method == "POST":
        form = LostForm(request.POST, request.FILES)
        if form.is_valid():
            lost_item = form.save(commit=False)
            lost_item.student = request.user.student
            lost_item.save()
            return redirect("lost_items_list")
    else:
        form = LostForm()

    return render(request, "lost/create_lost_item.html", {"form": form})


# หน้ารวมของหาย
def lost_items_list(request):
    lost_items = Lost.objects.filter().order_by('founded_status','-id')
    return render(request, "lost/lost_items_list.html", {"lost_items": lost_items})


# สมาชิกชุมนุมโพสประกาศกิจกรรม
@login_required
def club_create_announcement(request):
    # if not request.user.username.startswith("tu_"):
    #     return redirect("home")  # ถ้าไม่ใช่accountชุมนุมจะกลับไปหน้าhome
    
    if not request.user.student.club:
        # messages.error(request, "You must be a member of a club to create an announcement.")
        return redirect("home")    

    if request.method == "POST":
        form = ClubAnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.student = request.user.student
            # announcement.club = request.user.student.club
            announcement.categories = "clubs"
            announcement.save()
            messages.success(request, "Announcement created successfully!")
            
            # Redirect ไปที่หน้า club_announcement_list
            return redirect('event-detail', announcement_id=announcement.id)
    else:
        form = ClubAnnouncementForm()

    return render(request, "clubs/create_club_post.html", {"form": form})


# รวมโพสจากทุกclub
def all_club_list(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to log in first.")
        return redirect('login')    
    
    student = request.user.student  # ดึง Student object จาก User ที่ล็อกอินอยู่

    # ถ้าเป็น admin ให้แสดงทุก clubs และ dropdown ให้เลือก origin
    if request.user.is_superuser:
        # ถ้าเป็น admin ให้เลือกดู clubs ทั้งหมด
        clubs = Club.objects.all()  # แสดงทุก clubs
        faculty_name = "All Faculties"  # สำหรับแสดงว่าเป็นทุกคณะ
    else:
        student_id = str(student.student_id)  # ดึง student_id
        faculty_code = student_id[2:4]  # ดึงตัวเลขตัวที่ 3-4 (จากการแปลงเป็น string)
        faculty_name = get_faculty_name(get_faculty_by_code(faculty_code))  
        clubs = Club.objects.filter(origin=get_faculty_by_code(faculty_code))  # กรองตามคณะ

    # กรองประกาศที่เกี่ยวข้องกับ clubs
    all_club_announcements = Announcement.objects.filter(categories="clubs").order_by("-date")
    
    # กรอง TU clubs โดยใช้ origin="tu"
    tu_clubs = Club.objects.filter(origin="tu")
    tu_club_announcements = all_club_announcements.filter(club__in=tu_clubs)
    
    faculty_club_announcements = all_club_announcements.filter(club__in=clubs)
    
    if request.user.is_authenticated:
        # ถ้าผู้ใช้งานล็อกอินให้หากิจกรรมที่ผู้ใช้งานสนใจ
        interested_events = list(Interest.objects.filter(user=request.user).values_list('announcement_id', flat=True))
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
            "clubs": clubs,          # Clubs ตามคณะ หรือ ทุกคณะสำหรับ admin
            "tu_clubs": tu_clubs,     # Clubs ของ TU
            "faculty_name": faculty_name,  # ชื่อคณะ
            "interested_events": interested_events,            
        },
    )


def tu_clubs_list(request):
    # ดึงข้อมูล Club ที่มี origin="tu"
    clubs = Club.objects.filter(origin="tu")
    all_club_announcements = Announcement.objects.filter(categories="clubs").order_by("-date")
    
    tu_club_announcements = all_club_announcements.filter(club__in=clubs)

    if request.user.is_authenticated:
        # ถ้าผู้ใช้งานล็อกอินให้หากิจกรรมที่ผู้ใช้งานสนใจ
        interested_events = list(Interest.objects.filter(user=request.user).values_list('announcement_id', flat=True))
    else:
        interested_events = []
        
    # ส่งข้อมูล Club ไปยังเทมเพลต
    return render(request, "clubs/tu_clubs.html", {
        "clubs": clubs,
        "tu_club_announcements": tu_club_announcements,
        "interested_events": interested_events,                    
    })

def club_detail(request, club_id):
    # ดึงข้อมูล Club ตาม club_id
    club = get_object_or_404(Club, id=club_id)

    # ดึงข้อมูล Announcement ที่มีการเชื่อมโยงกับ Club นี้
    announcements = Announcement.objects.filter(club=club)

    if request.user.is_authenticated:
        # ถ้าผู้ใช้งานล็อกอินให้หากิจกรรมที่ผู้ใช้งานสนใจ
        interested_events = list(Interest.objects.filter(user=request.user).values_list('announcement_id', flat=True))
    else:
        interested_events = []
        
    # ส่งข้อมูล Club และ Announcement ไปยังเทมเพลต
    return render(request, "clubs/club_detail.html", {
        "club": club,
        "announcements": announcements,
        "interested_events": interested_events,                                
    })

def lost_detail(request, lost_id):
    lost = get_object_or_404(Lost, id=lost_id)
    return render(request, "lost/lost_item_detail.html", {"lost": lost})


def found_detail(request, found_id):
    found = get_object_or_404(Found, id=found_id)
    return render(request, "found/found_item_detail.html", {"found": found})


def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out", extra_tags='success')
    return redirect("login")


def lost_edit(request, lost_id):
    lost = get_object_or_404(Lost, id=lost_id)

    if request.method == "POST":
        form = LostForm(request.POST, request.FILES, instance=lost)
        if form.is_valid():
            if not request.FILES.get('image'):
                form.instance.image = lost.image            
            form.save()
            return redirect('lost_detail',lost_id=lost_id) 
    else:
        form = LostForm(instance=lost)
        
    return render(request, "lost/edit_lost_item.html", {"form": form, "lost": lost})

def lost_delete(request, lost_id):
    lost_item = get_object_or_404(Lost, id=lost_id)
    
    if lost_item.student == request.user.student:
        lost_item.delete()
        return redirect('lost_items_list')
    else:
        return redirect('lost_items_list')


def found_edit(request, found_id):
    found = get_object_or_404(Found, id=found_id)
    if request.method == 'POST':
        form = FoundForm(request.POST, request.FILES, instance=found)
        if form.is_valid():
            form.save()
            return redirect('found_detail', found_id=found_id)
    else:
        form = FoundForm(instance=found)    
    return render(request, "found/edit_found_item.html", {"form": form,"found": found})

def found_delete(request, found_id):
    found_item = get_object_or_404(Found, id=found_id)
    
    if found_item.student == request.user.student:
        found_item.delete()
        return redirect('found_items_list')
    else:
        return redirect('found_items_list')    

# กดสนใจกิจกรรม
# @login_required
def toggle_interest(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    user = request.user

    # ตรวจสอบว่าผู้ใช้งานสนใจอยู่หรือไม่
    if Interest.objects.filter(user=request.user, announcement=announcement).exists():
        # ถ้าผู้ใช้งานเคยสนใจกิจกรรมนี้แล้ว ให้ยกเลิก
        Interest.objects.filter(user=request.user, announcement=announcement).delete()
        messages.success(request, "คุณได้ยกเลิกการกดสนใจกิจกรรมนี้แล้ว")
    else:
        # ถ้าผู้ใช้งานยังไม่สนใจ ให้กดสนใจ
        Interest.objects.create(user=request.user, announcement=announcement)
        messages.success(request, "คุณได้กดสนใจกิจกรรมนี้แล้ว")
    
    referer = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer)

def my_account(request):
    if request.user.is_authenticated:
        student = request.user.student           

        # หากมีการส่งฟอร์ม (POST) ให้บันทึกการเปลี่ยนแปลง
        if request.method == 'POST':
            form = StudentProfileForm(request.POST, request.FILES, instance=student)
            if form.is_valid():
                form.save()  # บันทึกการเปลี่ยนแปลง
                return redirect('my_account')  # เมื่อบันทึกเสร็จแล้วให้รีเฟรชหน้า

        else:
            form = StudentProfileForm(instance=student)

        return render(request, "my_account/personal_info.html", {
            "student": student,
            "form": form
        })
    else:
        messages.warning(request, "You need to log in first.")        
        return redirect('login') 

def lost_found_history(request):
    if not hasattr(request.user, 'student') or not request.user.student:
        lost_items = []
        found_items = []
    else:
        lost_items = Lost.objects.filter(student=request.user.student).order_by('founded_status', '-id')
        found_items = Found.objects.filter(student=request.user.student).order_by('founded_status', '-id')

    return render(request, "my_account/lost_found_history.html", {'lost_items': lost_items, 'found_items': found_items})

    
def my_events(request):
    if request.user.is_authenticated:
        interested_events = Interest.objects.filter(user=request.user).select_related('announcement')
    else:
        interested_events = []

    return render(request, 'my_account/my_events.html', {
        'interested_events': interested_events
    })

def get_faculty_by_code(faculty_code):
    faculty_map = {
        '01': 'law',
        '02': 'business',
        '03': 'political_science',
        '04': 'economics',
        '05': 'social_administration',
        '06': 'liberal_arts',
        '07': 'journalism_mass_comm',
        '08': 'sociology_anthropology',
        '09': 'science_technology',
        '10': 'engineering',
        '11': 'medicine',
        '12': 'allied_health',
        '13': 'dentistry',
    }
    return faculty_map.get(faculty_code, 'law')  # ค่าพื้นฐานคือ 'law'

def get_faculty_name(faculty_code):
    faculties = {
        'law': 'Faculty of Law (คณะนิติศาสตร์)',
        'business': 'Faculty of Business (คณะพาณิชยศาสตร์และการบัญชี)',
        'political_science': 'Faculty of Political Science (คณะรัฐศาสตร์)',
        'economics': 'Faculty of Economics (คณะเศรษฐศาสตร์)',
        'social_administration': 'Faculty of Social Administration (คณะสังคมสงเคราะห์ศาสตร์)',
        'sociology_anthropology': 'Faculty of Sociology and Anthropology (คณะสังคมวิทยาและมานุษยวิทยา)',
        'liberal_arts': 'Faculty of Liberal Arts (คณะศิลปศาสตร์)',
        'journalism_mass_comm': 'Faculty of Journalism and Mass Communication (คณะวารสารศาสตร์และสื่อสารมวลชน)',
        'science_technology': 'Faculty of Science and Technology (คณะวิทยาศาสตร์และเทคโนโลยี)',
        'engineering': 'Faculty of Engineering (คณะวิศวกรรมศาสตร์)',
        'architecture_planning': 'Faculty of Architecture and Planning (คณะสถาปัตยกรรมศาสตร์และการผังเมือง)',
        'medicine': 'Faculty of Medicine (คณะแพทยศาสตร์)',
        'allied_health': 'Faculty of Allied Health Sciences (คณะสหเวชศาสตร์)',
        'dentistry': 'Faculty of Dentistry (คณะทันตแพทยศาสตร์)',
        'nursing': 'Faculty of Nursing (คณะพยาบาลศาสตร์)',
        'public_health': 'Faculty of Public Health (คณะสาธารณสุขศาสตร์)',
    }
    full_name = faculties.get(faculty_code, 'Unknown Faculty')
    english_name = full_name.split(' (')[0] 
    return english_name

def clubs_by_faculty(request):
    # ตรวจสอบว่าผู้ใช้เข้าสู่ระบบแล้วหรือยัง
    if not request.user.is_authenticated:
        return HttpResponse("You need to log in first.")
    
    # ดึง student_id จากผู้ใช้ที่ล็อกอิน
    student = request.user.student  # ดึง Student object จาก User ที่ล็อกอินอยู่
    student_id = str(student.student_id)  # แปลง student_id เป็นสตริง

    if not student_id:
        return HttpResponse("Error: No student ID found in user profile.")

    # ถ้า student_id มีความยาวน้อยกว่า 4 ตัว (กรณีผิดปกติ)
    if len(student_id) < 4:
        return HttpResponse("Error: Invalid student ID format.")

    faculty_code = student_id[2:4]  # ดึงตัวเลขตัวที่ 3-4 (จากการแปลงเป็น string)
    faculty_name = get_faculty_name(get_faculty_by_code(faculty_code))  # ฟังก์ชันแปลง faculty_code เป็นชื่อคณะ

    # กรอง Club ตามคณะ
    clubs = Club.objects.filter(origin=get_faculty_by_code(faculty_code))  # ฟังก์ชัน `get_faculty_by_code` ใช้แปลง `faculty_code` เป็นชื่อคณะ

    # ดึงประกาศที่เกี่ยวข้องกับคลับในคณะนี้
    all_club_announcements = Announcement.objects.filter(
        categories="clubs",
        club__in=clubs  # กรองประกาศที่เชื่อมโยงกับคลับในคณะนี้
    ).order_by("-date")
    
    if request.user.is_authenticated:
        # ถ้าผู้ใช้งานล็อกอินให้หากิจกรรมที่ผู้ใช้งานสนใจ
        interested_events = list(Interest.objects.filter(user=request.user).values_list('announcement_id', flat=True))
    else:
        interested_events = []    

    # ส่งข้อมูลไปยังเทมเพลต
    return render(request, "clubs/faculty_clubs.html", {
        "clubs": clubs,
        "faculty_name": faculty_name,
        "announcements": all_club_announcements,  # ส่งประกาศไปยังเทมเพลต
        "interested_events": interested_events,                    
    })

@login_required
def edit_profile(request):
    # ดึงข้อมูล Student ของ user ที่ล็อกอินอยู่
    student = request.user.student

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()  # บันทึกข้อมูลที่แก้ไขลงในฐานข้อมูล
            return redirect('my_account')  # เปลี่ยนเส้นทางไปที่หน้าโปรไฟล์ 
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'my_account/edit_profile.html', {'form': form, 'student': student})

def event_edit(request, announcement_id):
    # ดึงประกาศที่ต้องการแก้ไขจากฐานข้อมูล
    announcement = get_object_or_404(Announcement, id=announcement_id)

    # ตรวจสอบสิทธิ์ของผู้ใช้ว่าเป็นเจ้าของประกาศ
    if announcement.student != request.user.student:
        return redirect('event-detail', announcement_id=announcement_id)  # ถ้าไม่ใช่เจ้าของประกาศจะไม่สามารถแก้ไขได้
    
    # หากรับการร้องขอแบบ POST ให้บันทึกข้อมูลที่แก้ไข
    if request.method == 'POST':
        form = ClubAnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()  # บันทึกข้อมูลที่แก้ไข
            return redirect('event-detail', announcement_id=announcement.id)  # กลับไปที่หน้ารายละเอียดของประกาศที่แก้ไข
    else:
        # กรณีที่แสดงฟอร์มให้กรอกข้อมูลใหม่
        form = ClubAnnouncementForm(instance=announcement)

    # ส่งฟอร์มและประกาศไปที่เทมเพลต
    return render(request, "events/edit_event.html", {
        "form": form,
        "announcement": announcement,
    })
    
def event_delete(request, announcement_id):
    # ดึงประกาศที่ต้องการลบ
    announcement = get_object_or_404(Announcement, id=announcement_id)
    
    # ตรวจสอบว่าเป็นผู้สร้างประกาศนี้หรือไม่
    if announcement.student == request.user.student:
        announcement.delete()  # ลบประกาศจากฐานข้อมูล
        messages.success(request, "Announcement deleted successfully!")
        return redirect('clubs_announcement_list')    
    return redirect('clubs_announcement_list')

def club_post_history(request):
    # ตรวจสอบว่า user มี student หรือไม่
    if not hasattr(request.user, 'student') or not request.user.student:
        announcements = []  # ถ้าไม่มี student ให้ return list ว่าง
    else:
        # ดึงประกาศทั้งหมดที่ผู้ใช้โพสต์โดยใช้ student ของผู้ใช้
        announcements = Announcement.objects.filter(student=request.user.student).order_by('-date')  # กรองโดย student ของผู้ใช้

    # ส่งข้อมูลไปยัง template
    return render(request, "my_account/club_post_history.html", {'announcements': announcements})