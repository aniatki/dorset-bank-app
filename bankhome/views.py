from django.shortcuts import render, redirect
from .forms import AccountForm
from .models import Account, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
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
    logout(request)
    return redirect("login_view")

def signup_view(request):
    form = AccountForm()
    context = {"form": form}
    return render(request, "signup/signup.html", context)

@login_required
def dashboard_view(request):
    users = Account.objects.all()
    return render(request, 'dashboard/dashboard.html', {"users": users})
        

@login_required
def read_view(request, pk):
    user = Account.objects.get(pk=pk)
    context = {'user': user}
    return render(request, 'read/read.html', context)