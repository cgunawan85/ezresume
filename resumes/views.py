from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from formtools.wizard.views import SessionWizardView

from users.forms import CustomUserChangeForm
from .forms import (ResumeForm, ProfileUpdateForm, WorkExperienceFormSet, CertificationFormSet,
                    EducationFormSet, SkillFormSet, LanguageFormSet)
from .models import Resume
from .forms import ChooseForm


FORMS = [('resumes', ResumeForm),
         ('work_experience', WorkExperienceFormSet),
         ('certifications', CertificationFormSet),
         ('education', EducationFormSet),
         ('skills', SkillFormSet),
         ('languages', LanguageFormSet), ]

FORM_TYPES = ('work_experience', 'certifications', 'education', 'skills', 'languages')

TEMPLATES = {'resumes': 'resumes/resumes.html',
             'work_experience': 'resumes/work_experience.html',
             'certifications': 'resumes/certifications.html',
             'education': 'resumes/education.html',
             'skills': 'resumes/skills.html',
             'languages': 'resumes/languages.html', }


@login_required()
def choose(request, pk):
    resume = Resume.objects.get(pk=pk)
    if request.method == 'POST':
        form = ChooseForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['resume_template'] == 'jakarta':
                return render(request, 'resumes/jakarta.html', {'form': form, 'resume': resume})
            if form.cleaned_data['resume_template'] == 'new_york':
                return render(request, 'resumes/new_york.html', {'form': form, 'resume': resume})
            if form.cleaned_data['resume_template'] == 'tokyo':
                return render(request, 'resumes/tokyo.html', {'form': form, 'resume': resume})
            if form.cleaned_data['resume_template'] == 'rome':
                return render(request, 'resumes/rome.html', {'form': form, 'resume': resume})
            if form.cleaned_data['resume_template'] == 'sf':
                return render(request, 'resumes/san_francisco.html', {'form': form, 'resume': resume})
    else:
        form = ChooseForm()
    return render(request, 'resumes/choose.html', {'form': form, 'resume': resume})


@login_required()
def my_resumes(request):
    user = request.user
    resumes = Resume.objects.filter(user=user)
    return render(request, 'resumes/my_resumes.html', {'resumes': resumes})


@login_required()
def view_resume(request, pk):
    resume = Resume.objects.get(pk=pk)
    return render(request, 'resumes/tokyo.html', {'resume': resume})


@login_required()
def faq(request):
    return render(request, 'resumes/faq.html')


@login_required()
def templates(request):
    return render(request, 'resumes/templates.html')


@login_required()
def edit_profile(request):
    if request.method == 'POST':
        u_form = CustomUserChangeForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been saved!')
            return HttpResponseRedirect(reverse('resumes:edit-profile'))
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


def dict_has_data(input_dict):
    has_data = False
    for key in input_dict:
        if input_dict[key]:
            has_data = True
            break
    return has_data


class ResumeWizard(LoginRequiredMixin, SessionWizardView):
    login_url = '/login/'

    """
    def get_form_initial(self, step):
        if 'pk' in self.kwargs:
            return {}
        return self.initial_dict.get(step, {})
    """

    def get_form_instance(self, step):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            resume = Resume.objects.get(id=pk)

            if step == 'resumes':
                return resume

            if step == 'work_experience':
                return resume.workexperience_set.all()

            if step == 'certifications':
                return resume.certification_set.all()

            if step == 'education':
                return resume.education_set.all()

            if step == 'skills':
                return resume.skill_set.all()

            if step == 'languages':
                return resume.language_set.all()
        return None

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        user = self.request.user
        resume_form_data = self.get_cleaned_data_for_step('resumes')
        resume_name = resume_form_data['name']
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
        else:
            pk = None
        resume, created = Resume.objects.update_or_create(id=pk, defaults={'user': user,
                                                                           'name': resume_name, })

        for form_name in FORM_TYPES:
            form_data_list = self.get_cleaned_data_for_step(form_name)
            for form_data in form_data_list:
                if not dict_has_data(form_data):
                    continue
                form_data['resume'] = resume

                form_instance = self.get_form(step=form_name)
                obj = form_data.pop('id')
                if obj:
                    form_instance.model.objects.filter(id=obj.id).update(**form_data)
                else:
                    form_instance.model.objects.create(**form_data)

        messages.add_message(self.request, messages.SUCCESS, 'Your resume has been saved!')
        return HttpResponseRedirect(reverse('resumes:my-resumes'))
