from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
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

    def get_form_initial(self, step):
        if 'pk' in self.kwargs:
            return {}
        return self.initial_dict.get(step, {})

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

        work_experience_form_data = self.get_cleaned_data_for_step('work_experience')
        for work_experience in work_experience_form_data:
            we_obj = work_experience.get('id')
            we_kwargs = {'position': work_experience.get('position'),
                         'company': work_experience.get('company'),
                         'city': work_experience.get('city'),
                         'start_date': work_experience.get('start_date'),
                         'end_date': work_experience.get('end_date'),
                         'achievements': work_experience.get('achievements'),
                         'resume': resume, }
            if we_obj:
                WorkExperience.objects.filter(id=we_obj.id).update(**we_kwargs)
            else:
                WorkExperience.objects.create(**we_kwargs)

        certification_form_data = self.get_cleaned_data_for_step('certifications')
        for certification in certification_form_data:
            cert_obj = certification.get('id')
            cert_kwargs = {'name': certification.get('name'),
                           'date_obtained': certification.get('date_obtained'),
                           'city': certification.get('city'),
                           'resume': resume, }
            if cert_obj:
                Certification.objects.filter(id=cert_obj.id).update(**cert_kwargs)
            else:
                Certification.objects.create(**cert_kwargs)

        education_form_data = self.get_cleaned_data_for_step('education')
        for education in education_form_data:
            edu_obj = education.get('id')
            edu_kwargs = {'school': education.get('school'),
                          'degree': education.get('degree'),
                          'major': education.get('major'),
                          'gpa': education.get('gpa'),
                          'city': education.get('city'),
                          'start_date': education.get('start_date'),
                          'end_date': education.get('end_date'),
                          'resume': resume, }
            if edu_obj:
                Education.objects.filter(id=edu_obj.id).update(**edu_kwargs)
            else:
                Education.objects.create(**edu_kwargs)

        skill_form_data = self.get_cleaned_data_for_step('skills')
        for skill in skill_form_data:
            skill_obj = skill.get('id')
            skill_kwargs = {'name': skill.get('name'),
                            'competency': skill.get('competency'),
                            'resume': resume, }
            if skill_obj:
                Skill.objects.filter(id=skill_obj.id).update(**skill_kwargs)
            else:
                Skill.objects.create(**skill_kwargs)

        language_form_data = self.get_cleaned_data_for_step('languages')
        for language in language_form_data:
            lang_obj = language.get('id')
            lang_kwargs = {'name': language.get('name'),
                           'competency': language.get('competency'),
                           'resume': resume, }
            if lang_obj:
                Language.objects.filter(id=lang_obj.id).update(**lang_kwargs)
            else:
                Language.objects.create(**lang_kwargs)

        messages.add_message(self.request, messages.SUCCESS, 'Your resume has been saved!')
        return HttpResponseRedirect(reverse('resumes:my-resumes'))

    '''
    [{'name': 'Test', 'user': None}, [
        {'position': '', 'company': '', 'city': '', 'start_date': None, 'end_date': None, 'achievements': '',
         'resume': None, 'id': None}], [{'name': '', 'date_obtained': None, 'city': '', 'resume': None, 'id': None}], [
         {'school': '', 'degree': '', 'major': '', 'gpa': None, 'city': '', 'start_date': None, 'end_date': None,
          'resume': None, 'id': None}], [{'name': '', 'competency': None, 'resume': None, 'id': None}],
     [{'name': '', 'competency': None, 'resume': None, 'id': None}]]

    def done(self, form_list, **kwargs):
        # TODO: Refactor this code to use modelform methods like save()
        user = self.request.user
        resume_form_data = self.get_cleaned_data_for_step('resumes')
        resume_name = resume_form_data['name']
        resume = Resume.objects.create(name=resume_name, user=user)

        work_experience_form_data = self.get_cleaned_data_for_step('work_experience')
        for work_experience in work_experience_form_data:
            we_obj = work_experience.get('id')
            # There is id in the form even though its hidden
            print('we_obj', we_obj, type(we_obj))
            we_kwargs = {'position': work_experience.get('position'),
                         'company': work_experience.get('company'),
                         'city': work_experience.get('city'),
                         'start_date': work_experience.get('start_date'),
                         'end_date': work_experience.get('end_date'),
                         'achievements': work_experience.get('achievements'),
                         'resume': resume, }

            if we_obj:
                # update object (have to filter first to get queryset for update)
                # This is the easiest way to update multiple fields on an object
                WorkExperience.objects.filter(id=we_obj.id).update(**we_kwargs)
            else:
                WorkExperience.objects.create(**we_kwargs)
                """
                WorkExperience.objects.create(position=work_experience.get('position'),
                                          company=work_experience.get('company'),
                                          city=work_experience.get('city'),
                                          start_date=work_experience.get('start_date'),
                                          end_date=work_experience.get('end_date'),
                                          achievements=work_experience.get('achievements'),
                                          resume=resume, )
                """

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
        '''
