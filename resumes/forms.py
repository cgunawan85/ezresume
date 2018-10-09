from django.forms import ModelForm, Textarea, TextInput
from django import forms

from .choices import COMPETENCY_CHOICES
from users.models import Profile
from .models import Certification, Education, Language, Resume, Skill, WorkExperience


class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['name', ]


class WorkExperienceForm(ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['position', 'company', 'city', 'start_date', 'end_date', 'achievements', ]
        widgets = {'start_date': TextInput(attrs={'class': 'date-picker'}),
                   'end_date': TextInput(attrs={'class': 'date-picker'}),
                   'achievements': Textarea(attrs={'class': 'objective-box', 'cols': 50, 'rows': 10}), }


class CertificationForm(ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'date_obtained', 'city', ]
        widgets = {'date_obtained': TextInput(attrs={'class': 'date-picker'})}


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'degree', 'gpa', 'city', 'start_date', 'end_date', ]
        widgets = {'start_date': TextInput(attrs={'class': 'date-picker'}),
                   'end_date': TextInput(attrs={'class': 'date-picker'}), }


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'competency', ]
        widgets = {'competency': forms.Select(choices=COMPETENCY_CHOICES, attrs={'class': 'form-control'}), }


class LanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'competency', ]
        widgets = {'competency': forms.Select(choices=COMPETENCY_CHOICES, attrs={'class': 'form-control'}), }


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'city', 'country', 'phone_number', 'linked_in', 'objective', 'profile_pic', ]
        widgets = {'objective': Textarea(attrs={'class': 'objective-box', 'cols': 50, 'rows': 10}),
                   'city': TextInput(attrs={'placeholder': 'What city do you live in?'}),
                   }
        labels = {"linked_in": "LinkedIn profile",
                  "phone_number": "Mobile number",
                  "profile_pic": "Profile picture",
                  "objective": "Professional objective", }
