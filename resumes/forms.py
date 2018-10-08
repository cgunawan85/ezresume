from django.forms import DateInput, ModelForm, Textarea, TextInput

from .models import Resume, WorkExperience
from users.models import Profile

# TODO: Create forms for all resume models


class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['name', ]
        widgets = {'name': TextInput(attrs={'placeholder': 'Example: Business Development Executive'}),
                   }
        labels = {"name": "Position you are applying for", }


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


class WorkExperienceForm(ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['position', 'company', 'city', 'start_date', 'end_date', 'achievements', ]
        widgets = {
            'start_date': DateInput(attrs={'class': 'date-picker'}),
            'end_date': DateInput(attrs={'class': 'date-picker'}),
            'achievements': Textarea(attrs={'class': 'objective-box', 'cols': 50, 'rows': 10}),
        }
