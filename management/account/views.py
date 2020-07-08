from .models import CustomUser
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import StudentForm,CreateUserModel
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

def registerStudent(request):
    pass

def registerInstructor(request):
    if request.method=="POST":
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name,user_type=2)
            user.instructor.name=first_name+" "+last_name
            user.save()
            messages.success(request," Instructor added successfully ")
            return redirect('addInstructor')
        except:
            messages.error(request," Error occured. Please Try again!")
            return redirect('addInstructor')
    return render(request,'HOD/add_instructor.html')

def dash(request):
    return render(request,'HOD/dashboard.html')

def manageCourse(request):
    return render(request,'HOD/course.html')

def logoutUser(request):
    logout(request)
    return redirect('loginpage')