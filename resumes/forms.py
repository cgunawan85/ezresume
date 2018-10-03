from django import forms
from django.forms import ModelForm

from .models import Resume


class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['name', ]
