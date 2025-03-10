from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CustomUser(User):

    def create_user(self, email, first_name, last_name, address, balance, password):
        if not email:
            raise ValueError("You have not provided a valid email address.")
    
        email = self.normalize_email(email)
        first_name = self.first_name
        last_name = self.last_name
        address = self.address
        balance = self.balance
        password = self.set_password(password)
        