from django.forms import ModelForm, Textarea, TextInput
from django import forms

from users.models import Profile

# TODO: Create forms for all resume models and add widgets


class ResumeForm(forms.Form):
    name = forms.CharField(label='Resume name', max_length=255)


class WorkExperienceForm(forms.Form):
    position = forms.CharField(max_length=255, required=False)
    company = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=255, required=False)
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'date-picker'}), required=False)
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'date-picker'}), required=False)
    achievements = forms.CharField(widget=forms.Textarea(attrs={'class': 'objective-box', 'cols': 50, 'rows': 10}),
                                   required=False)


class CertificationForm(forms.Form):
    name = forms.CharField(label='Certification name', max_length=255, required=False)
    date_obtained = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'date-picker'}), required=False)
    city = forms.CharField(max_length=255, required=False)


class EducationForm(forms.Form):
    school = forms.CharField(max_length=255, required=False)
    degree = forms.CharField(max_length=255, required=False)
    gpa = forms.FloatField(required=False)
    city = forms.CharField(max_length=255, required=False)
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'date-picker'}), required=False)
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'date-picker'}), required=False)


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
                  "objective": "Professional objective",
                  }

