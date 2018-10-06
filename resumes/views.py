from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from users.forms import CustomUserChangeForm
from .forms import ResumeForm, ProfileUpdateForm, WorkExperienceForm
from .models import Resume


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
# This view is for updating profile in create resume flow
def edit_profile_form(request):
    if request.method == 'POST':
        u_form = CustomUserChangeForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been saved!')
            return HttpResponseRedirect(reverse('resumes:edit-work-experience'))
    else:
        u_form = CustomUserChangeForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'p_form': p_form,
               'u_form': u_form,
               }
    return render(request, 'resumes/profile_form.html', context)


@login_required()
def edit_work_experience(request):
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            # need to add resume.id to work experience before saving
            messages.success(request, 'Your work experience has been saved!')
            return HttpResponseRedirect(reverse('resumes:edit-work-experience'))
    else:
        form = WorkExperienceForm()
    return render(request, 'resumes/work_experience_form.html', {'form': form})


@login_required()
def delete_resume(request, pk):
    resume = Resume.objects.get(pk=pk)
    resume.delete()
    messages.success(request, "Your resume has been deleted!")
    return HttpResponseRedirect(reverse('resumes:my-resumes'))


