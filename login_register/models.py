from django.db import models

# Create your models here.

class User(models.Model):
    fullname = models.TextField()
    username = models.TextField()
    password = models.TextField()
    email = models.TextField()
    budget = models.TextField()
    profilePicture = models.ImageField(null=True, blank=True, upload_to="images/")