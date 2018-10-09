from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from users.forms import CustomUserChangeForm
from .forms import ResumeForm, ProfileUpdateForm, WorkExperienceForm, CertificationForm
from .models import Resume
from formtools.wizard.views import SessionWizardView


FORMS = [('resumes', ResumeForm),
         ('work_experience', WorkExperienceForm),
         ('certifications', CertificationForm), ]

TEMPLATES = {'resumes': 'resumes/resume.html',
             'work_experience': 'resumes/work_experience.html',
             'certifications': 'resumes/certifications.html', }


@login_required()
def my_resumes(request):
    resumes = Resume.objects.all()
    # creates resume from modal pop up
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            temp.save()
            messages.success(request, 'Your resume has been created!')
            return HttpResponseRedirect(reverse('resumes:edit-profile-form'))
    else:
        form = ResumeForm()
    return render(request, 'resumes/my_resumes.html', {'resumes': resumes, 'form': form})


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


# TODO: Add login required mixin to this view
class ResumeWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        return HttpResponseRedirect(reverse('resumes:my-resumes'))

