from django import forms
from .models import Found,Lost

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
            'founded_status': forms.CheckboxInput(),
        }