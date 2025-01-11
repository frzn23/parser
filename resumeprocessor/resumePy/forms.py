from django import forms
from .models import Candidate

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['file']