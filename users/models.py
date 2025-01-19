from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='profile/', blank=True, null=True, default='profile/default.png')
    resume = models.FileField(upload_to='resume/', blank=True, null=True)