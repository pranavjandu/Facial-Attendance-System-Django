
from .models import Batch, Course, CustomUser, Instructor,Students
from django.shortcuts import redirect, render,HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.urls import reverse
from .filters import InstructorFilter,StudentFilter,CourseFilter,BatchFilter
from json import dumps

import os
import dlib
import cv2
from imutils import face_utils,resize
from imutils.video import VideoStream
from imutils.face_utils import FaceAligner

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
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        batch=request.POST.get("batch_id")
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
    batch=Batch.objects.all()
    return render(request,'HOD/add_student.html',{"batches":batch})

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
        starttime=request.POST.get("start_time")
        endtime=request.POST.get("end_time")
        days=request.POST.getlist("day")
        days=dumps(days)
        try:
            course_obj=Course.objects.get(id=course)
            name=course_obj.course_name
            name=batch_name+" "+name
            instructor_obj=Instructor.objects.get(id=instructor)
            batch=Batch(batch_name=name,course_id=course_obj,instructor_id=instructor_obj,start_time=starttime,end_time=endtime,days=days)
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

def editInstructor(request,ins_id):
    if request.method=="POST":
        instructor_id=request.POST.get("instructor_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")

        try:
            user=CustomUser.objects.get(id=instructor_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()
            

            ins_model=Instructor.objects.get(user=instructor_id)
            ins_model.name=first_name+" "+last_name
            ins_model.save()
            messages.success(request,"Successfully Edited Instructor")
            return HttpResponseRedirect(reverse("editi",kwargs={"ins_id":instructor_id}))
        except:
            messages.error(request,"Failed to Edit Instructor")
            return HttpResponseRedirect(reverse("editi",kwargs={"ins_id":instructor_id}))
    ins=Instructor.objects.get(user=ins_id)
    return render(request,"HOD/edit_instructor.html",{"instructor":ins})

def editStudent(request,stu_id):
    if request.method=="POST":
        student_id=request.POST.get("student_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        batch_id=request.POST.get("batch_id")

        try:
            user=CustomUser.objects.get(id=student_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()
                

            stu_model=Students.objects.get(user=student_id)
            stu_model.name=first_name+" "+last_name
            batch_obj=Batch.objects.get(id=batch_id)
            stu_model.batch_id=batch_obj
            stu_model.save()
            messages.success(request,"Successfully Edited Student")
            return HttpResponseRedirect(reverse("edits",kwargs={"stu_id":student_id}))
        except:
            messages.error(request,"Failed to Edit Student")
            return HttpResponseRedirect(reverse("edits",kwargs={"stu_id":student_id}))
    stu=Students.objects.get(user=stu_id)
    batch=Batch.objects.all()
    return render(request,"HOD/edit_student.html",{"student":stu,"batches":batch})


def editCourse(request,cou_id):
    if request.method=="POST":
        course_id=request.POST.get("course_id")
        cou_name=request.POST.get("course_name")
        try:
            cou_obj=Course.objects.get(id=course_id)
            cou_obj.course_name=cou_name
            cou_obj.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("editc",kwargs={"cou_id":course_id}))
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("editc",kwargs={"cou_id":course_id}))
            
    cou=Course.objects.get(id=cou_id)
    return render(request,"HOD/edit_course.html",{"course":cou})


def editBatch(request,bat_id):
    ''' Passes batch id to templte HTML, renders it and handle details edit request. 

        Keyword Arguments: 
        bat_id -- Batch id of the batch that needs to be modified.
    '''
    if request.method=="POST":   # control comes here when submit button is pressed
        batchid=request.POST.get("batch_id")
        batchname=request.POST.get("batch_name")
        courseid=request.POST.get("course_id")
        instructorid=request.POST.get("instructor_id")
        starttime=request.POST.get("start_time")
        endtime=request.POST.get("end_time")
        days=request.POST.getlist("day")
        try:
            batch_obj=Batch.objects.get(id=batchid)
            batch_obj.batch_name=batchname
            course_obj=Course.objects.get(id=courseid)
            instructor_obj=Instructor.objects.get(id=instructorid)
            batch_obj.course_id=course_obj
            batch_obj.instructor_id=instructor_obj
            batch_obj.start_time=starttime
            batch_obj.end_time=endtime
            days=dumps(days)
            batch_obj.days=days
            batch_obj.save()
            messages.success(request,"Successfully Edited Batch ")
            return HttpResponseRedirect(reverse("editb",kwargs={"bat_id":batchid}))
        except:
            messages.error(request,"Failed to edit Batch ")
            return HttpResponseRedirect(reverse("editb",kwargs={"bat_id":batchid}))
    cou=Course.objects.all()
    batch=Batch.objects.get(id=bat_id)
    ins=Instructor.objects.all()
    listofdays=batch.days
    return render(request,"HOD/edit_batch.html",{"batch":batch,"instructors":ins,"courses":cou,"listofdays":listofdays})


def registerFace(request,us_id):
    if request.method=="POST":
        id = request.POST.get("userid")
        try:
            if(os.path.exists('face_data/dataset/{}/'.format(id))==False):
                os.makedirs('face_data/dataset/{}/'.format(id))
            directory='face_data/dataset/{}/'.format(id)

            # Face detection by HOG face detector
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor('face_data/shape_predictor_68_face_landmarks.dat') 
            fa = FaceAligner(predictor , desiredFaceWidth = 96)
            #video stream
            videost = VideoStream(src=0).start()
            
            # counter to stop loop after 100 photos
            datacounter = 0
            while(True):
                frame = videost.read()    #reading frame
                frame = resize(frame ,width = 800)
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert to grayscale
                #this will detect image in frame
                faces = detector(gray_frame,0)
                #There can be multiple faces in above
                for face in faces:
                    if face is None:
                        continue
                    (x,y,w,h) = face_utils.rect_to_bb(face)
                    face_aligned = fa.align(frame,gray_frame,face)
                    # As the program captures an image, it is written to the folder dataset
                    datacounter = datacounter+1
                    cv2.imwrite(directory+'/'+str(datacounter)+'.jpg'	, face_aligned)
                    face_aligned = resize(face_aligned ,width = 400)
                    #for creating a rectangle on the face
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
                    # Before continuing to the next loop, I want to give it a little pause
                    cv2.waitKey(10)

                #for Showing the image in a window
                cv2.imshow("Add Images",frame)
                cv2.waitKey(2)
                #For loop break condition for 50 photos
                if(datacounter>49):
                    break
            
            # stopping the videostream
            videost.stop()
            # destroy window
            cv2.destroyAllWindows()
            #To make faceTaken to True in database
            user=CustomUser.objects.get(id=us_id)
            stuid=user.students.id
            stu_obj=Students.objects.get(id=stuid)
            stu_obj.faceTaken=True
            stu_obj.save()
            messages.success(request,"Face data added successfully")
            return HttpResponseRedirect(reverse("createdataset",kwargs={"us_id":id}))
        except:
            messages.error(request,"Error occured while adding data")
            return HttpResponseRedirect(reverse("createdataset",kwargs={"us_id":id}))
    return render(request,"HOD/createdataset.html",{"userid":us_id})



