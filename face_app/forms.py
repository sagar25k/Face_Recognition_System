# face_app/forms.py
from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'roll_number', 'image_path']  # 'image_path' will be a JSON field containing paths of images
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'image_path': forms.FileInput(attrs={'class': 'form-control'}),
        }
