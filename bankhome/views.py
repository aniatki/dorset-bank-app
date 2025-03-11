from django.shortcuts import render
from .forms import AccountForm

def login(request):
    return render(request, "login/login.html")

def signup(request):
    form = AccountForm()
    context = {"form": form}
    return render(request, "signup/signup.html", context)


def dashboard(request):
    objs = Account.objects
    return render(request, 'dashboard/dashboard.html', {"objs": objs})

def read(request, pk):
    obj = None
    for i in objs:
        if i['id'] == int(pk):
            obj = i
    context = {'o': obj}
    return render(request, 'read/read.html', context)