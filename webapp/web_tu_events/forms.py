from django import forms
from .models import Found,Lost,Announcement

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
        fields = ['title', 'description', 'image', 'start_date', 'end_date', 'place']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }