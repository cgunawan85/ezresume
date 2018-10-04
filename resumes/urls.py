from django.urls import path

from . import views

urlpatterns = [
    path('', views.my_resumes, name='my-resumes'),
    path('create-resume/', views.resume_view, name='create-resume'),
    path('profile/', views.update_profile, name='update-profile'),
    path('delete/<int:pk>/', views.delete_resume, name='delete-resume'),
]
