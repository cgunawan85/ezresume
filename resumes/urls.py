from django.urls import path

from . import views

urlpatterns = [
    path('', views.my_resumes, name='my-resumes'),
    path('resume_info/', views.create_resume, name='resume-info'),
]