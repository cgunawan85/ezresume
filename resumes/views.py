from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse

from users.forms import CustomUserChangeForm
from .forms import (ResumeForm, ProfileUpdateForm, WorkExperienceForm, CertificationForm,
                    EducationForm, SkillForm, LanguageForm)
from .models import Resume
from formtools.wizard.views import SessionWizardView


FORMS = [('resumes', ResumeForm),
         ('work_experience', WorkExperienceForm),
         ('certifications', CertificationForm),
         ('education', EducationForm),
         ('skills', SkillForm),
         ('languages', LanguageForm), ]

TEMPLATES = {'resumes': 'resumes/resumes.html',
             'work_experience': 'resumes/work_experience.html',
             'certifications': 'resumes/certifications.html',
             'education': 'resumes/education.html',
             'skills': 'resumes/skills.html',
             'languages': 'resumes/languages.html', }


@login_required()
def my_resumes(request):
    resumes = Resume.objects.all()
    return render(request, 'resumes/my_resumes.html', {'resumes': resumes})


@login_required()
def edit_profile(request):
    if request.method == 'POST':
        u_form = CustomUserChangeForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been saved!')
            return HttpResponseRedirect(reverse('resumes:update-profile'))
    else:
        u_form = CustomUserChangeForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'p_form': p_form,
               'u_form': u_form,
               }
    return render(request, 'resumes/profile.html', context)


@login_required()
def delete_resume(request, pk):
    resume = Resume.objects.get(pk=pk)
    resume.delete()
    messages.success(request, "Your resume has been deleted!")
    return HttpResponseRedirect(reverse('resumes:my-resumes'))


class ResumeWizard(LoginRequiredMixin, SessionWizardView):
    login_url = '/login/'

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        return HttpResponseRedirect(reverse('resumes:my-resumes'))

