from django.db import models

# Create your models here.

class Expense(models.Model):
    userId = models.TextField()
    category = models.TextField()
    amount = models.TextField()
    paymentType = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    dateTime = models.DateTimeField()
    description = models.TextField()
    billPicture = models.ImageField(null=True, blank=True, upload_to="images/bills")