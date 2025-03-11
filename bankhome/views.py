from django.shortcuts import render
from .forms import AccountForm
from .models import Account

users = Account.objects.all()

def login(request):
    return render(request, "login/login.html")

def signup(request):
    form = AccountForm()
    context = {"form": form}
    return render(request, "signup/signup.html", context)

def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {"users": users})

def read(request, pk):
    user = Account.objects.get(pk=pk)
    context = {'user': user}
    return render(request, 'read/read.html', context)