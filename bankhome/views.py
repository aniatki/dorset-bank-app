from django.shortcuts import render
from .models import Account
from .forms import AccountForm

def login(request):
    return render(request, "login/login.html")

def signup(request):
    form = AccountForm()
    context = {"form": form}
    return render(request, "signup/signup.html", context)

# objs = [{
#         "id": 1,
#         "first_name": "John",
#         "last_name": "Sexton",
#         "address": "12 Main Street",
#         "balance": 8300
#     },
#     {
#         "id": 2,
#         "first_name": "Mary",
#         "last_name": "Sexton",
#         "address": "12 Main Street",
#         "balance": 8300
#     },
#     {
#         "id": 3,
#         "first_name": "Jane",
#         "last_name": "Sexton",
#         "address": "12 Main Street",
#         "balance": 8300
#     }
# ]

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