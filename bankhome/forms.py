from django.forms import ModelForm
from .models import Account, User, Transaction, Deposit, Withdrawal
from django import forms
from django.contrib.auth.forms import UserCreationForm

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'address', 'balance']

class UserForm(ModelForm):
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

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'from_id', 'to_id']

class DepositForm(ModelForm):
    class Meta:
        model = Deposit
        fields = ['amount', 'from_id']

class WithdrawalForm(ModelForm):
    class Meta:
        model = Withdrawal
        fields = ['amount', 'from_id']