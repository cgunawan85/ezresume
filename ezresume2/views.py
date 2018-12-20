from django.shortcuts import render


def home_view(request):
    return render(request, 'home-indo.html')


def privacy(request):
    return render(request, 'privacy.html')
