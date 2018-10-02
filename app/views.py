from django.shortcuts import render


def my_resumes(request):
    return render(request, 'app/myresumes.html')
