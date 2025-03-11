from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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
    
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """Creates and returns a regular user."""
        if not username:
            raise ValueError("The Username field is required")
        
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """Creates and returns a superuser."""
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        """Required for Django authentication to work correctly."""
        return self.get(username=username)

class User(AbstractBaseUser):
    username = models.CharField(db_index=True, unique=True, max_length=50)
    password = models.CharField(max_length=100)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        """Return True if user has a specific permission."""
        return True 

    def has_module_perms(self, app_label):
        """Return True if user has permissions for an app."""
        return True 