from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

# class CustomUser(User):

#     def create_user(self, email, first_name, last_name, address, balance, password):
#         if not email:
#             raise ValueError("You have not provided a valid email address.")
    
#         email = self.normalize_email(email)
#         first_name = self.first_name
#         last_name = self.last_name
#         address = self.address
#         balance = self.balance
#         password = self.set_password(password)
        

class Account(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    id_number = models.IntegerField(validators=[MaxValueValidator(999)])
    balance = models.IntegerField(validators=[MaxValueValidator(999999)])
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"