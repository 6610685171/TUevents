from django import forms
from .models import Found,Lost,Announcement,Student

class FoundForm(forms.ModelForm):
    class Meta:
        model = Found
        fields = ['items_name', 'image', 'description', 'found_at', 'contact', 'founded_status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'founded_status': forms.CheckboxInput(),
        }

class LostForm(forms.ModelForm):
    class Meta:
        model = Lost
        fields = ['items_name', 'image', 'description', 'lost_at', 'contact', 'founded_status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'founded_status': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'founded_status'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.image:  # If the instance already has an image
            self.fields['image'].required = False

class ClubAnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'image', 'start_date', 'end_date', 'place','club']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
    categories = forms.ChoiceField(
        choices=Announcement.CATEGORIES_CHOICES,
        initial='clubs',  # กำหนดค่าเริ่มต้นเป็น 'clubs'
        widget=forms.Select(attrs={'readonly': 'readonly'}),  # ป้องกันไม่ให้ผู้ใช้เลือกค่า
    )

    # ปรับการตั้งค่า readonly ในฟอร์มในกรณีที่คุณไม่ต้องการให้ผู้ใช้แก้ไขค่า
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ปิดการแก้ไขฟิลด์ categories ที่ผู้ใช้ไม่ต้องกรอก
        self.fields['categories'].disabled = True        
        
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['image']