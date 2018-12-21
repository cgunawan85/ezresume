import logging

from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from formtools.wizard.views import SessionWizardView

from users.forms import CustomUserChangeForm
from .forms import (ResumeForm, ProfileUpdateForm, WorkExperienceFormSet, CertificationFormSet,
                    EducationFormSet, SkillFormSet, LanguageFormSet)
from .models import Resume, WorkExperience, Certification, Education, Skill, Language
from .forms import ChooseForm

import pdfcrowd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    user = request.user
    pp_url = user.profile.profile_pic.url.strip('/')
    resume = Resume.objects.get(pk=pk)
    form = ChooseForm(request.POST)
    group = Group.objects.get(name='paying_user')
    if request.method == 'GET':
        form = ChooseForm()
    elif request.method == 'POST' and 'view-resume' in request.POST:
        if form.is_valid() and form.cleaned_data['resume_template'] == 'jakarta':
            return render(request, 'resumes/jakarta.html', {'form': form, 'resume': resume, 'pp_url': pp_url})
        if form.is_valid() and form.cleaned_data['resume_template'] == 'new_york':
            return render(request, 'resumes/new_york.html', {'form': form, 'resume': resume, 'pp_url': pp_url})
        if form.is_valid() and form.cleaned_data['resume_template'] == 'tokyo':
            return render(request, 'resumes/tokyo.html', {'form': form, 'resume': resume, 'pp_url': pp_url})
        if form.is_valid() and form.cleaned_data['resume_template'] == 'rome':
            return render(request, 'resumes/rome.html', {'form': form, 'resume': resume, 'pp_url': pp_url})
        if form.is_valid() and form.cleaned_data['resume_template'] == 'sf':
            return render(request, 'resumes/san_francisco.html', {'form': form, 'resume': resume, 'pp_url': pp_url})
    # two buttons on one page
    elif form.is_valid() and request.method == 'POST' and 'export-resume' in request.POST:
        if request.user.groups.filter(name='paying_user').exists():
            # code for exporting pdfcrowd goes here
            client = pdfcrowd.HtmlToPdfClient('chrisgunawan85', 'ea5734a7dc5aabbded5e65d8a32de8a4')
            client.setUsePrintMedia(True)
            client.setPageHeight('-1')
            client.setDebugLog(True)
            # set HTTP response headers
            pdf_response = HttpResponse(content_type='application/pdf')
            pdf_response['Cache-Control'] = 'max-age=0'
            pdf_response['Accept-Ranges'] = 'none'
            content_disp = 'attachment' if 'asAttachment' in request.POST else 'inline'
            pdf_response['Content-Disposition'] = content_disp + '; filename=my_resume.pdf'

            if form.cleaned_data['resume_template'] == 'jakarta':
                html = render_to_string('resumes/jakarta.html', {'resume': resume, 'pp_url': pp_url})
            if form.cleaned_data['resume_template'] == 'new_york':
                html = render_to_string('resumes/new_york.html', {'resume': resume, 'pp_url': pp_url})
            if form.cleaned_data['resume_template'] == 'tokyo':
                html = render_to_string('resumes/tokyo.html', {'resume': resume, 'pp_url': pp_url})
            if form.cleaned_data['resume_template'] == 'rome':
                html = render_to_string('resumes/rome.html', {'resume': resume, 'pp_url': pp_url})
            if form.cleaned_data['resume_template'] == 'sf':
                html = render_to_string('resumes/san_francisco.html', {'resume': resume, 'pp_url': pp_url})

            client.convertStringToStream(html, pdf_response)
            # send the generated PDF
            return pdf_response
        else:
            messages.info(request, "Please purchase a package to export to PDF format")
            return HttpResponseRedirect(reverse('resumes:payment'))
    return render(request, 'resumes/choose.html', {'form': form, 'resume': resume})


@login_required()
def my_resumes(request):
    user = request.user
    resumes = Resume.objects.filter(user=user).order_by('-created_at')
    return render(request, 'resumes/my_resumes.html', {'resumes': resumes})


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
        else:
            if step == 'resumes':
                return None

            if step == 'work_experience':
                return WorkExperience.objects.none()

            if step == 'certifications':
                return Certification.objects.none()

            if step == 'education':
                return Education.objects.none()

            if step == 'skills':
                return Skill.objects.none()

            if step == 'languages':
                return Language.objects.none()
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
