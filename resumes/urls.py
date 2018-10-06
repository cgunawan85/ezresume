from django.urls import path

from . import views

urlpatterns = [
    path('', views.my_resumes, name='my-resumes'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('edit-profile-form/', views.edit_profile_form, name='edit-profile-form'),
    path('edit-work-experience-form/', views.edit_work_experience, name='edit-work-experience'),
    path('delete/<int:pk>/', views.delete_resume, name='delete-resume'),
]
