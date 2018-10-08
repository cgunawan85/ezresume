from django.db import models
from users.models import User
# TODO: Add training model and determine which fields are optional


class Resume(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class WorkExperience(models.Model):
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    achievements = models.TextField()
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return self.position

    class Meta:
        verbose_name_plural = "Work Experience"


class Certification(models.Model):
    name = models.CharField(max_length=255)
    date_obtained = models.DateTimeField()
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Education(models.Model):
    school = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    gpa = models.FloatField(blank=True)
    city = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return self.school

    class Meta:
        verbose_name_plural = "Education"


class Language(models.Model):
    name = models.CharField(max_length=255)
    competency = models.IntegerField()
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=255)
    competency = models.IntegerField()
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

