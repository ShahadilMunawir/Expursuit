import os
from uuid import uuid4
from django.db import models
from django.utils import timezone

# Create your models here.

def generate_image_filename(instance, filename):
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    filename, extension = os.path.splitext(filename)
    new_filename = f"{timestamp}_{str(uuid4().hex)}{extension}"
    return f"images/profile picture/{new_filename}"

class User(models.Model):
    fullName = models.TextField()
    username = models.TextField()
    passwordHash = models.TextField()
    email = models.TextField()
    budget = models.TextField()
    profilePicture = models.ImageField(null=True, blank=True, upload_to=generate_image_filename)