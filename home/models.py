from django.db import models

# Create your models here.

class Expense(models.Model):
    userId = models.TextField()
    category = models.TextField()
    amount = models.TextField()
    paymentType = models.TextField()
    date = models.TextField()
    description = models.TextField()