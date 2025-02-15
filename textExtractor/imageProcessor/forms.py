from django import forms
from .models import ExtractedImage

class ExtractedImageForm(forms.ModelForm):
    class Meta:
        model = ExtractedImage
        fields = ('image',)