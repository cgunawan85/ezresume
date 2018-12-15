from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')


def privacy(request):
    return render(request, 'privacy.html')
