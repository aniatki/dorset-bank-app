from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
 
class Account(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    balance = models.IntegerField(validators=[MaxValueValidator(999999)])
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"