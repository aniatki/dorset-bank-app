from django.shortcuts import render
from .forms import AccountForm
from .models import Account, User
from django.contrib import messages



users = Account.objects.all()

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            messages.success(request, 'Successfully logged in.')
        except:
            messages.error(request, 'User does not exist.')
    context = {}
    return render(request, "login/login.html", context)

def signup_view(request):
    form = AccountForm()
    context = {"form": form}
    return render(request, "signup/signup.html", context)

def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html', {"users": users})

def read_view(request, pk):
    user = Account.objects.get(pk=pk)
    context = {'user': user}
    return render(request, 'read/read.html', context)