from django.urls import path

from . import views

urlpatterns = [
    path('', views.my_resumes, name='my-resumes'),
    path('create-resume/', views.create_resume, name='create-resume'),
    path('profile/', views.update_profile, name='update-profile'),
    path('update-profile/', views.update_profile_form, name='update-profile-form'),
    path('delete/<int:pk>/', views.delete_resume, name='delete-resume'),
]
