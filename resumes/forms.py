from django.forms import ModelForm, Textarea, TextInput
from django import forms
from django.forms import modelformset_factory
from django.forms.models import BaseModelFormSet

from .choices import COMPETENCY_CHOICES
from users.models import Profile
from .models import Certification, Education, Language, Resume, Skill, WorkExperience


class MyModelFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(MyModelFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


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


WorkExperienceFormSet = modelformset_factory(WorkExperience, form=WorkExperienceForm, formset=MyModelFormSet,
                                             validate_min=True, extra=1, max_num=3)


class CertificationForm(ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'date_obtained', 'city', ]
        widgets = {'date_obtained': TextInput(attrs={'class': 'date-picker'})}


CertificationFormSet = modelformset_factory(Certification, form=CertificationForm, formset=MyModelFormSet,
                                            extra=1, max_num=5)


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'degree', 'major', 'gpa', 'city', 'start_date', 'end_date', ]
        widgets = {'start_date': TextInput(attrs={'class': 'date-picker'}),
                   'end_date': TextInput(attrs={'class': 'date-picker'}), }
        labels = {'gpa': 'GPA'}


EducationFormSet = modelformset_factory(Education, form=EducationForm, formset=MyModelFormSet, extra=1, max_num=3)


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'competency', ]
        # TODO: Default for competency has to be none
        widgets = {'competency': forms.Select(choices=COMPETENCY_CHOICES, attrs={'class': 'form-control'}),
                   'name': TextInput(attrs={'placeholder': 'For example: Microsoft Excel'}), }


SkillFormSet = modelformset_factory(Skill, form=SkillForm, formset=MyModelFormSet, extra=1, max_num=5)


class LanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'competency', ]
        # TODO: Default for competency has to be none
        widgets = {'competency': forms.Select(choices=COMPETENCY_CHOICES, attrs={'class': 'form-control'}),
                   'name': TextInput(attrs={'placeholder': 'For example: English or Mandarin'}), }


LanguageFormSet = modelformset_factory(Language, form=LanguageForm, formset=MyModelFormSet, extra=1, max_num=5)


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        # TODO: Restrict phone number to 0-9 numerals
        fields = ['address', 'address2', 'city', 'country', 'phone_number', 'linked_in', 'objective', 'profile_pic', ]
        widgets = {'objective': Textarea(attrs={'class': 'objective-box', 'cols': 50, 'rows': 10,
                                                'maxlength': 500,
                                                'placeholder': 'A short blurb telling the hiring manager what skills, '
                                                'knowledge, and abilities you have that will help the '
                                                'company achieve its goals. Max length is 500 characters.'}),
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
