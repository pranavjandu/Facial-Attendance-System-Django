from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.

def loginpage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.info(request,"wrong credentials")

    return render(request,'login.html')

def dash(request):
    return render(request,'HOD/dashboard.html')

def manageCourse(request):
    return render(request,'HOD/course.html')