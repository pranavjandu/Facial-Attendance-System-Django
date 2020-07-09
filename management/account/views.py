from .models import Batch, Course, CustomUser, Instructor,Students
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import AddStudentForm
from .filters import InstructorFilter,StudentFilter,CourseFilter,BatchFilter

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


def registerStudent(request):
    
    if request.method=="POST":
        form=AddStudentForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            batch=form.cleaned_data["batch1"]
            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.students.name=first_name+" "+last_name
                batch_obj=Batch.objects.get(id=batch)
                user.students.batch_id=batch_obj
                user.save()
                messages.success(request," Student added successfully ")
                return redirect('addStudent')
            except:
                messages.error(request," Error occured. Please Try again!")
                return redirect('addStudent')
        else:
            messages.error(request," Error occured. Please Try again!")
            return redirect('addStudent')
    
    form=AddStudentForm()
    return render(request,'HOD/add_student.html',{"form":form})

def dash(request):
    return render(request,'HOD/dashboard.html')

def addCourse(request):
    if request.method=="POST":
        course_name=request.POST.get("course_name")
        try:
            course=Course(course_name=course_name)
            course.save()
            messages.success(request,"Course "+course_name+" successfully added! ")
            return redirect('addCourses')
        except:
            messages.error(request,"Error occured ! Please Try again.")
            return redirect('addCourses')
    return render(request,'HOD/add_course.html')


def addBatch(request):
    if request.method=="POST":
        batch_name=request.POST.get("batch_name")
        course=request.POST.get("course_id")
        instructor=request.POST.get("instructor_id")
        try:
            course_obj=Course.objects.get(id=course)
            name=course_obj.course_name
            name=batch_name+" "+name
            instructor_obj=Instructor.objects.get(id=instructor)
            batch=Batch(batch_name=name,course_id=course_obj,instructor_id=instructor_obj)
            batch.save()
            messages.success(request,"Batch "+batch_name+" successfully added! ")
            return redirect('addBatch')
        except:
            messages.error(request,"Error occured ! Please Try again.")
            return redirect('addBatch')
    courses=Course.objects.all()
    instructors=Instructor.objects.all()
    context={'courses':courses,'instructors':instructors}
    return render(request,'HOD/add_batch.html',context)

def logoutUser(request):
    logout(request)
    return redirect('loginpage')

def manageInstructor(request):
    ins=Instructor.objects.all()
    myfilter=InstructorFilter(request.GET,queryset=ins)
    ins=myfilter.qs
    return render(request,"HOD/manage_instructor.html",{"instructors":ins,"myfilter":myfilter})

def manageStudent(request):
    stu=Students.objects.all()
    myfilter=StudentFilter(request.GET,queryset=stu)
    stu=myfilter.qs
    return render(request,"HOD/manage_students.html",{"students":stu,"myfilter":myfilter})

def manageCourse(request):
    cou=Course.objects.all()
    myfilter=CourseFilter(request.GET,queryset=cou)
    cou=myfilter.qs
    return render(request,"HOD/manage_course.html",{"courses":cou,"myfilter":myfilter})

def manageBatch(request):
    bat=Batch.objects.all()
    myfilter=BatchFilter(request.GET,queryset=bat)
    bat=myfilter.qs
    return render(request,"HOD/manage_batch.html",{"batches":bat,"myfilter":myfilter})