from django.db import models
from users.models import User


class Resume(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class WorkExperience(models.Model):
    position = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    achievements = models.TextField(blank=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return self.position

    class Meta:
        verbose_name_plural = "Work Experience"


class Certification(models.Model):
    name = models.CharField(max_length=255, blank=True)
    date_obtained = models.DateTimeField(blank=True)
    city = models.CharField(max_length=255, blank=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Education(models.Model):
    school = models.CharField(max_length=255, blank=True)
    degree = models.CharField(max_length=255, blank=True)
    gpa = models.FloatField(blank=True)
    city = models.CharField(max_length=255, blank=True)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return self.school

    class Meta:
        verbose_name_plural = "Education"


class Skill(models.Model):
    name = models.CharField(max_length=255, blank=True)
    competency = models.IntegerField(blank=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=255, blank=True)
    competency = models.IntegerField(blank=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


