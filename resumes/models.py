from django.db import models

from .choices import LANGUAGE_COMPETENCY_CHOICES, SKILL_COMPETENCY_CHOICES
from users.models import User

from tinymce.models import HTMLField


class Resume(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name


class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, blank=True)
    position = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    achievements = HTMLField(blank=True)

    def __str__(self):
        return self.position

    class Meta:
        verbose_name_plural = "Work Experience"
        ordering = ['-end_date', ]


class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=255, blank=True)
    date_obtained = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_obtained', ]


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, blank=True)
    school = models.CharField(max_length=255, blank=True)
    degree = models.CharField(max_length=255, blank=True)
    major = models.CharField(max_length=255, blank=True)
    gpa = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.school

    class Meta:
        verbose_name_plural = "Education"
        ordering = ['-end_date', ]


class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=255, blank=True)
    competency = models.IntegerField(choices=SKILL_COMPETENCY_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=255, blank=True)
    competency = models.IntegerField(choices=LANGUAGE_COMPETENCY_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name
