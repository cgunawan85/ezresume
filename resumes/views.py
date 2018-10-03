from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .forms import ResumeForm


@login_required()
def my_resumes(request):
    return render(request, 'resumes/myresumes.html')


@login_required()
def resume_view(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            temp.save()
            return HttpResponseRedirect(reverse('resumes:my-resumes'))
    else:
        form = ResumeForm()
    return render(request, 'resumes/resume.html', {'form': form})
