from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse

from users.forms import CustomUserChangeForm
from .forms import (ResumeForm, ProfileUpdateForm, WorkExperienceForm, CertificationForm,
                    EducationForm, SkillFormSet, LanguageForm)
from .models import Certification, Education, Language, Resume, Skill, WorkExperience
from formtools.wizard.views import SessionWizardView


FORMS = [('resumes', ResumeForm),
         ('work_experience', WorkExperienceForm),
         ('certifications', CertificationForm),
         ('education', EducationForm),
         ('skills', SkillFormSet),
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
        WorkExperience.objects.create(position=work_experience_form_data['position'],
                                      company=work_experience_form_data['company'],
                                      city=work_experience_form_data['city'],
                                      start_date=work_experience_form_data['start_date'],
                                      end_date=work_experience_form_data['end_date'],
                                      achievements=work_experience_form_data['achievements'],
                                      resume=resume, )

        certifications_form_data = self.get_cleaned_data_for_step('certifications')
        Certification.objects.create(name=certifications_form_data['name'],
                                     date_obtained=certifications_form_data['date_obtained'],
                                     city=certifications_form_data['city'],
                                     resume=resume, )

        education_form_data = self.get_cleaned_data_for_step('education')
        Education.objects.create(school=education_form_data['school'],
                                 degree=education_form_data['degree'],
                                 gpa=education_form_data['gpa'],
                                 city=education_form_data['city'],
                                 start_date=education_form_data['start_date'],
                                 end_date=education_form_data['end_date'],
                                 resume=resume, )

        # TODO: Insert loop here to loop over skills
        skills_form_data = self.get_cleaned_data_for_step('skills')
        Skill.objects.create(name=skills_form_data[0]['name'],
                             competency=skills_form_data[0]['competency'],
                             resume=resume, )

        languages_form_data = self.get_cleaned_data_for_step('languages')
        Language.objects.create(name=languages_form_data['name'],
                                competency=languages_form_data['competency'],
                                resume=resume, )

        return HttpResponseRedirect(reverse('resumes:my-resumes'))
