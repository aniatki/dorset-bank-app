from django.forms import ModelForm
from .models import Account, User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = "__all__"

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        widgets = {
            'password': forms.PasswordInput(),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']