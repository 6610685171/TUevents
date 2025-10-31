from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    form = AuthenticationForm(data=request.POST or None)    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                
                # เมื่อ login สำเร็จแล้ว ตรวจสอบว่าเป็น superuser หรือไม่
                if user.is_superuser:
                    return redirect("admin:index")  # ไปที่หน้า admin ของ Django

                # ถ้าไม่ใช่ superuser, ตรวจสอบว่ามี 'next' หรือไม่
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request, "Please fill in both fields.")
    else:
        # ถ้ามี ?next=... แสดงข้อความเตือน (คือถ้าเข้าหน้าอื่นทั้งที่ยังไม่login หลังเด้งมาหน้าloginให้เตือนว่าต้องloginก่อน)
        next_url = request.GET.get("next")
        if next_url:
            messages.warning(request, "You need to log in first.")
            
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out", extra_tags="success")
    return redirect("login")
