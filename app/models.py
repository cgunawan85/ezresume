from django.db import models
from users.models import User
from django.utils import timezone


class Resume(models.Model):
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Resume, self).save(*args, **kwargs)
