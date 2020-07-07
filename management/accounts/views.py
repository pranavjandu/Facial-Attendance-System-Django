from django.shortcuts import render,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserModel

# Create your views here.

def dashboard(request):
    return render(request,'accounts/base.html')

def login(request):
    return render(request,'accounts/login.html')

def authen(request):
    if request.method=="POST":
        return HttpResponse("Login working") 

def register(request):
    form=CreateUserModel()
    if request.method=="POST":
        form=CreateUserModel(request.POST)
        if form.is_valid():
            form.save()

    context={'form':form}
    return render(request,'accounts/register.html',context)
