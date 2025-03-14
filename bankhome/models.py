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
        if not username:
            raise ValueError("The Username field is required")
        
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
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
        return True 

    def has_module_perms(self, app_label):
        return True
    
class Transfer(models.Model):
    id=models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    from_id = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='sent_transfers')
    from_new_balance = models.DecimalField(max_digits=10, decimal_places=2)
    to_id = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='received_transfers', default='')
    to_new_balance = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer {self.id}: {self.from_id} -> {self.to_id} ({self.amount})"

    def save(self, *args, **kwargs):
        from_account = self.from_id
        to_account = self.to_id

        if from_account.balance < self.amount:
            raise ValueError("Insufficient funds")
        
        if from_account == self.to_id:
            raise IndexError("From account and to account are the same. That is not permitted.")

        previous_from_balance = from_account.balance
        previous_to_balance = to_account.balance

        self.from_new_balance = previous_from_balance - self.amount
        self.to_new_balance = previous_to_balance + self.amount

        super().save(*args, **kwargs)

        from_account.balance = self.from_new_balance
        to_account.balance = self.to_new_balance
        from_account.save(update_fields=['balance'])
        to_account.save(update_fields=['balance'])

        TransactionLog.objects.create(
            account=from_account,
            transaction_type='transfer',
            amount=self.amount,
            previous_balance=previous_from_balance,
            new_balance=self.from_new_balance
        )


class Withdrawal(models.Model):
    id=models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    from_id = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='withdrawals')
    from_new_balance = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        from_account = self.from_id
        previous_balance = from_account.balance

        if self.amount < from_account.balance:
            self.from_new_balance = previous_balance - self.amount
        else:
            raise ValueError("Insufficient funds.")

        super().save(*args, **kwargs)

        from_account.balance = self.from_new_balance
        from_account.save(update_fields=['balance'])

        TransactionLog.objects.create(
            account=from_account,
            transaction_type='withdrawal',
            amount=self.amount,
            previous_balance=previous_balance,
            new_balance=self.from_new_balance
        )


class Deposit(models.Model):
    id=models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    from_id = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='deposits')
    from_new_balance = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        from_account = self.from_id
        previous_balance = from_account.balance
        self.from_new_balance = previous_balance + self.amount

        super().save(*args, **kwargs)

        from_account.balance = self.from_new_balance
        from_account.save(update_fields=['balance'])

        TransactionLog.objects.create(
            account=from_account,
            transaction_type='deposit',
            amount=self.amount,
            previous_balance=previous_balance,
            new_balance=self.from_new_balance
        )


class TransactionLog(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    ]

    id = models.AutoField(primary_key=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='logs')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    previous_balance = models.DecimalField(max_digits=10, decimal_places=2)
    new_balance = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} - {self.amount} - {self.timestamp}"
