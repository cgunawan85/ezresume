from django_countries.fields import CountryField
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from tinymce.models import HTMLField
from django.core.files.storage import default_storage
from django_resized import ResizedImageField


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = CountryField(blank_label='(Select country)', blank=True)
    linked_in = models.CharField(max_length=255, blank=True)
    objective = HTMLField(blank=True)
    profile_pic = ResizedImageField(size=[300, 300], quality=100, default="profile-pics/default.jpg", upload_to="profile-pics")
    sub_expires_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.email
    '''
    def save(self, force_insert=False, using=None):
        # calling super, using args and kwargs
        super().save()

        img = Image.open(default_storage.open(self.profile_pic.name, 'r'))

        if img.height > 300 or img.width > 300:
            output_size = (100, 100)
            img.thumbnail(output_size)
            img.save(default_storage.save(self.profile_pic.name, 'r'), 'PNG')
            img.close()
	'''
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    # use choice field for package?
    package = models.CharField(max_length=255)
    total = models.IntegerField()
    paid_status = models.BooleanField(default=False)

    def __str__(self):
        return self.package
