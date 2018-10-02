from django.shortcuts import render


def my_resumes(request):
    return render(request, 'resumes/myresumes.html')


def create_resume(request):
    return render(request, 'resumes/resume.html')
