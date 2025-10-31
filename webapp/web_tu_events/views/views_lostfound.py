from ..models import Found,Lost
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from ..forms import FoundForm,LostForm

# หน้ารวมของที่เจอ
def found_items_list(request):
    found_items = Found.objects.order_by("founded_status", "-id")
    return render(request, "found/found_items_list.html", {"found_items": found_items})

# หน้ารวมของหาย
def lost_items_list(request):
    lost_items = Lost.objects.order_by("founded_status", "-id")
    return render(request, "lost/lost_items_list.html", {"lost_items": lost_items})

# โพสต์ของที่เจอ
@login_required
def create_found_item(request):
    form = FoundForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST" and form.is_valid():
        found_item = form.save(commit=False)
        found_item.student = getattr(request.user, "student", None)
        found_item.save()
        return redirect("found_items_list")

    return render(request, "found/create_found_item.html", {"form": form})

# โพสต์ของหาย
@login_required
def create_lost_item(request):
    form = LostForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST" and form.is_valid():
        lost_item = form.save(commit=False)
        lost_item.student = getattr(request.user, "student", None)
        lost_item.save()
        return redirect("lost_items_list")

    return render(request, "lost/create_lost_item.html", {"form": form})

def lost_detail(request, lost_id):
    lost_item = get_object_or_404(Lost, id=lost_id) # ดึงLost objectที่id=lost_id
    return render(request, "lost/lost_item_detail.html", {"lost": lost_item})

def found_detail(request, found_id):
    found_item = get_object_or_404(Found, id=found_id)
    return render(request, "found/found_item_detail.html", {"found": found_item})

def lost_edit(request, lost_id):
    lost_item = get_object_or_404(Lost, id=lost_id)

    if request.method == "POST":
        form = LostForm(request.POST, request.FILES, instance=lost_item)
        if form.is_valid():
            if not request.FILES.get("image"):
                form.instance.image = lost_item.image
            form.save()
            return redirect("lost_detail", lost_id=lost_id)
    else:
        form = LostForm(instance=lost_item)

    return render(request, "lost/edit_lost_item.html", {"form": form, "lost": lost_item})

def lost_delete(request, lost_id):
    lost_item = get_object_or_404(Lost, id=lost_id)

    if lost_item.student == request.user.student: # checkว่าเจ้าของitemนี้ใช่คนเดียวกับที่loginอยู่ไหม
        lost_item.delete()
        return redirect("lost_items_list")
    else:
        return redirect("lost_items_list")

def found_edit(request, found_id):
    found_item = get_object_or_404(Found, id=found_id)
    if request.method == "POST":
        form = FoundForm(request.POST, request.FILES, instance=found_item)
        if form.is_valid():
            if not request.FILES.get("image"):
                form.instance.image = found_item.image
            form.save()
            return redirect("found_detail", found_id=found_id)
    else:
        form = FoundForm(instance=found_item)
    return render(request, "found/edit_found_item.html", {"form": form, "found": found_item})

def found_delete(request, found_id):
    found_item = get_object_or_404(Found, id=found_id)

    if found_item.student == request.user.student:
        found_item.delete()
        return redirect("found_items_list")
    else:
        return redirect("found_items_list")
