from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def login(request):
    return render(request, "login/login.html")

def signup(request):
    return render(request, "signup/signup.html")

# @login_required
def dashboard(request):
    context = {
        "id": 1,
        "first_name": "John",
        "last_name": "Sexton",
        "address": "12 Main Street",
        "balance": 8300
    }
    return render(request, 'dashboard/dashboard.html', context)