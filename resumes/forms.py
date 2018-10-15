from django.forms import ModelForm, Textarea, TextInput, DateInput
from django import forms
from django.forms import modelformset_factory
from django.forms.models import BaseModelFormSet

from .choices import COMPETENCY_CHOICES
from users.models import Profile
from .models import Certification, Education, Language, Resume, Skill, WorkExperience


# allows validation on empty forms for ResumeWizard
class MyModelFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(MyModelFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['name', ]
        widgets = {'name': TextInput(attrs={'placeholder': 'For example: Data Scientist or Sales Manager'}), }
        labels = {'name': 'Resume name'}


class WorkExperienceForm(ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['position', 'company', 'city', 'start_date', 'end_date', 'achievements', ]
        widgets = {'start_date': TextInput(attrs={'class': 'date-picker', 'placeholder': 'MM/DD/YYYY'}),
                   'end_date': TextInput(attrs={'class': 'date-picker', 'placeholder': 'MM/DD/YYYY'}),
                   'achievements': Textarea(attrs={'class': 'objective-box', 'cols': 50, 'rows': 10}),
                   'position': TextInput(attrs={'placeholder': 'For example: Bank Teller'}),
                   'company': TextInput(attrs={'placeholder': 'For example: Bank Central Asia'}),
                   'city': TextInput(attrs={'placeholder': 'For example: Jakarta'}), }


WorkExperienceFormSet = modelformset_factory(WorkExperience, form=WorkExperienceForm, formset=MyModelFormSet,
                                             validate_min=True, extra=1, max_num=3)


class CertificationForm(ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'date_obtained', 'city', ]
        widgets = {'date_obtained': TextInput(attrs={'class': 'date-picker',
                                                     'placeholder': 'MM/DD/YYYY'}),
                   'name': TextInput(attrs={'placeholder': 'For example: Certified Technical Architect'}),
                   'city': TextInput(attrs={'placeholder': 'For example: New York'}), }
        labels = {'name': 'Certification name'}


CertificationFormSet = modelformset_factory(Certification, form=CertificationForm, formset=MyModelFormSet,
                                            extra=1, max_num=5)


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'degree', 'major', 'gpa', 'city', 'start_date', 'end_date', ]
        widgets = {'start_date': TextInput(attrs={'class': 'date-picker', 'placeholder': 'MM/DD/YYYY'}),
                   'end_date': TextInput(attrs={'class': 'date-picker', 'placeholder': 'MM/DD/YYYY'}),
                   'school': TextInput(attrs={'placeholder': 'For example: University of San Francisco'}),
                   'degree': TextInput(attrs={'placeholder': 'For example: Bachelor of Science'}),
                   'major': TextInput(attrs={'placeholder': 'For example: Economics'}),
                   'gpa': TextInput(attrs={'placeholder': 'For example: 3.7'}),
                   'city': TextInput(attrs={'placeholder': 'For example: San Francisco'}), }
        labels = {'gpa': 'GPA'}


EducationFormSet = modelformset_factory(Education, form=EducationForm, formset=MyModelFormSet, extra=1, max_num=3)


class SkillForm(ModelForm):
    def clean(self):
        cleaned_data = super(SkillForm, self).clean()
        name = cleaned_data.get('name')
        competency = cleaned_data.get('competency')

        if name and competency not in [1, 2, 3, 4, 5]:
                raise forms.ValidationError("Please select a competency level for your skill")

        if competency in [1, 2, 3, 4, 5] and not name:
                raise forms.ValidationError("Please enter a skill first")

    class Meta:
        model = Skill
        fields = ['name', 'competency', ]
        widgets = {'competency': forms.Select(choices=COMPETENCY_CHOICES, attrs={'class': 'form-control'}),
                   'name': TextInput(attrs={'placeholder': 'For example: Microsoft Excel'}), }
        labels = {'name': 'Skill name'}


SkillFormSet = modelformset_factory(Skill, form=SkillForm, formset=MyModelFormSet, extra=1, max_num=5)


class LanguageForm(ModelForm):
    def clean(self):
        cleaned_data = super(LanguageForm, self).clean()
        name = cleaned_data.get('name')
        competency = cleaned_data.get('competency')

        if name and competency not in [1, 2, 3, 4, 5]:
                raise forms.ValidationError("Please select a competency level for your language")

        if competency in [1, 2, 3, 4, 5] and not name:
                raise forms.ValidationError("Please enter a language first")

    class Meta:
        model = Language
        fields = ['name', 'competency', ]
        widgets = {'competency': forms.Select(choices=COMPETENCY_CHOICES, attrs={'class': 'form-control'}),
                   'name': TextInput(attrs={'placeholder': 'For example: English or Mandarin'}), }
        labels = {'name': 'Language name'}


LanguageFormSet = modelformset_factory(Language, form=LanguageForm, formset=MyModelFormSet, extra=1, max_num=5)


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        # TODO: Restrict phone number to 0-9 numerals
        fields = ['job_title', 'address', 'address2', 'city', 'country', 'phone_number', 'linked_in', 'objective',
                  'profile_pic', ]
        widgets = {'job_title': TextInput(attrs={'placeholder': 'What is your desired job title?'}),
                   'address': TextInput(attrs={'placeholder': 'What is your home street address?'}),
                   'address2': TextInput(attrs={'placeholder': 'Neighborhood or sub-district'}),
                   'city': TextInput(attrs={'placeholder': 'What city do you live in?'}),
                   'phone_number': TextInput(attrs={'placeholder': 'What is your mobile number?', }),
                   'linked_in': TextInput(attrs={'placeholder': 'What is your LinkedIn profile?'}), }
        labels = {"linked_in": "LinkedIn profile",
                  "phone_number": "Mobile number",
                  "profile_pic": "Profile picture",
                  "objective": "Career objective",
                  "address2": "Address", }
