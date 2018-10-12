from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, render_to_response
from django.urls import reverse

from users.forms import CustomUserChangeForm
from .forms import (ResumeForm, ProfileUpdateForm, WorkExperienceFormSet, CertificationFormSet,
                    EducationFormSet, SkillFormSet, LanguageFormSet)
from .models import Certification, Education, Language, Resume, Skill, WorkExperience
from formtools.wizard.views import SessionWizardView


FORMS = [('resumes', ResumeForm),
         ('work_experience', WorkExperienceFormSet),
         ('certifications', CertificationFormSet),
         ('education', EducationFormSet),
         ('skills', SkillFormSet),
         ('languages', LanguageFormSet), ]

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


class ResumeWizard(LoginRequiredMixin, SessionWizardView):
    login_url = '/login/'

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        user = self.request.user

        resume_form_data = self.get_cleaned_data_for_step('resumes')
        resume_name = resume_form_data['name']
        resume = Resume.objects.create(name=resume_name, user=user)

        work_experience_form_data = self.get_cleaned_data_for_step('work_experience')
        for work_experience in work_experience_form_data:
            WorkExperience.objects.create(position=work_experience.get('position'),
                                          company=work_experience.get('company'),
                                          city=work_experience.get('company'),
                                          start_date=work_experience.get('start_date'),
                                          end_date=work_experience.get('end_date'),
                                          achievements=work_experience.get('achievements'),
                                          resume=resume, )

        certifications_form_data = self.get_cleaned_data_for_step('certifications')
        for certifications in certifications_form_data:
            Certification.objects.create(name=certifications['name'],
                                         date_obtained=certifications['date_obtained'],
                                         city=certifications['city'],
                                         resume=resume, )

        education_form_data = self.get_cleaned_data_for_step('education')
        for education in education_form_data:
            Education.objects.create(school=education['school'],
                                     degree=education['degree'],
                                     major=education['major'],
                                     gpa=education['gpa'],
                                     city=education['city'],
                                     start_date=education['start_date'],
                                     end_date=education['end_date'],
                                     resume=resume, )

        skills_form_data = self.get_cleaned_data_for_step('skills')
        for skill in skills_form_data:
            Skill.objects.create(name=skill['name'],
                                 competency=skill['competency'],
                                 resume=resume, )

        languages_form_data = self.get_cleaned_data_for_step('languages')
        for language in languages_form_data:
            Language.objects.create(name=language['name'],
                                    competency=language['competency'],
                                    resume=resume, )

        messages.add_message(self.request, messages.SUCCESS, 'Your resume has been saved!')
        return HttpResponseRedirect(reverse('resumes:my-resumes'))
