from django.db import models

# Create your models here.

class User(models.Model):
    fullName = models.TextField()
    userName = models.TextField()
    passwordHash = models.TextField()
    email = models.TextField()
    budget = models.TextField()
    profilePicture = models.ImageField(null=True, blank=True, upload_to="images/profile picture")