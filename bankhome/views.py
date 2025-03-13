from django.shortcuts import get_object_or_404, render, redirect
from .forms import AccountForm, CustomUserCreationForm
from .models import Account, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
    accounts = Account.objects.all()
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
    form = Account.objects.get(pk=pk)
    context = {"form":form}
    return render(request, 'actions/edit.html', context)

def delete_view(request, pk):
    account = get_object_or_404(Account, id=pk)
    account.delete()
    messages.success(request, f"Entry {account.first_name, account.last_name} was deleted from the database.")
    return redirect('dashboard_view')