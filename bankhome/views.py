from django.shortcuts import get_object_or_404, render, redirect
from .forms import AccountForm, CustomUserCreationForm, TransactionForm, DepositForm, WithdrawalForm
from .models import Account, User, Transaction
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            messages.success(request, 'Successfully logged in.')
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard_view')
        else:
            messages.error(request, "Username or password does not exist.")

    context = {}
    return render(request, "login/login.html", context)

def logout_view(request):
    try:
        logout(request)
        messages.success(request, "Successfully logged out.")
    except:
        messages.error(request, "There was an issue trying to log out.")
    
    return redirect("login_view")

def signup_view(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, "Account was created successfully.")
            return redirect('dashboard_view')
        
        else:
            messages.error(request, "Something went wrong")

    context = {"form": form}
    return render(request, "signup/signup.html", context)

def dashboard_view(request):
    accounts = Account.objects.all().order_by('-updated')
    return render(request, 'dashboard/dashboard.html', {"accounts": accounts})
        

def read_view(request, pk):
    account = Account.objects.get(pk=pk)
    context = {'account': account}
    return render(request, 'read/read.html', context)

def create_view(request):
    form = AccountForm()
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.save()
            messages.success(request, "Account was created successfully.")
            return redirect('dashboard_view')
    context = {"form": form}
    return render(request, 'actions/create.html', context)

def edit_view(request, pk):
    account = Account.objects.get(pk=pk)
    form = AccountForm(instance=account)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Entry was updated.")
            return redirect('dashboard_view')

    context = {"account":account}
    return render(request, 'actions/edit.html', context)

def delete_view(request, pk):
    account = get_object_or_404(Account, id=pk)
    account.delete()
    messages.success(request, f"{account.first_name} was deleted from the database.")
    return redirect('dashboard_view')

def transfer_view(request):
    form = TransactionForm()
    if request.method == "POST":
        amount = request.POST.get('amount')
        from_id = request.POST.get('from_id')
        to_id = request.POST.get('to_id')

        if not all([amount, from_id, to_id]):
            messages.error(request, "Please, complete all the fields.")

        try:
            amount = Decimal(amount)
            from_account = Account.objects.get(id=from_id)
            to_account = Account.objects.get(id=to_id)

            if from_account.balance < amount:
                messages.error(request, "Insufficient funds")

            transaction = Transaction(
                amount=amount,
                from_id=from_account,
                to_id=to_account,
            )
            transaction.save()
            messages.success(request, "Transaction completed.")
            return redirect('dashboard_view')

        except:
            messages.error(request, "Invalid transaction")
            return redirect('transfer_view')
        
    return render(request, 'actions/transfer.html', {"form": form})

def deposit_view(request):
    form = DepositForm()
    if request.method == "POST":
        amount = request.POST.get('amount')
        from_id = request.POST.get('from_id')

        if not all([amount, from_id]):
            messages.error(request, "Please, complete all the fields.")

        try:
            amount = Decimal(amount)
            from_account = Account.objects.get(id=from_id)

            transaction = Transaction(
                amount=amount,
                from_id=from_account,
                # to_id=from_account,
            )
            print(transaction.amount)
            print(transaction.from_id)
            print(transaction)

            transaction.save()
            messages.success(request, f"Deposit of {amount} completed.")
            return redirect('dashboard_view')

        except:
            messages.error(request, "Invalid transaction")
            return redirect('deposit_view')
    return render(request, 'actions/deposit.html', {"form":form})

def withdrawal_view(request):
    form = DepositForm()
    if request.method == "POST":
        amount = request.POST.get('amount')
        from_id = request.POST.get('from_id')

        if not all([amount, from_id]):
            messages.error(request, "Please, complete all the fields.")

        try:
            amount = Decimal(amount)
            from_account = Account.objects.get(id=from_id)

            if from_account.balance < amount:
                messages.error(request, "Insufficient funds")

            transaction = Transaction(
                amount=amount,
                from_id=from_account,
                to_id=from_account,
            )
            print(transaction)
            transaction.save()
            messages.success(request, f"Withdrawal of {amount} completed.")
            return redirect('dashboard_view')

        except:
            messages.error(request, "Invalid transaction")
            return redirect('withdrawal_view')
    return render(request, 'actions/withdraw.html', {"form":form})