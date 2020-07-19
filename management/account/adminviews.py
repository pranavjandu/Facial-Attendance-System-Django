from .models import Batch, Course, CustomUser, Instructor,Students
from django.shortcuts import redirect, render,HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .filters import InstructorFilter,StudentFilter,CourseFilter,BatchFilter
from json import dumps,loads

import os
import cv2
import face_recognition
from.exceptions import MultipleFaceException
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 
def dash(request):
    '''
    Nothing on dashboard
    Blank for future purposes
    '''
    return render(request,'HOD/dashboard.html')


 
def registerInstructor(request):
    '''
    For adding a new instructor 
    '''
    if request.method=="POST":
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        try:   #creating CustomUser object
            user=CustomUser.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name,user_type=2)
            user.instructor.name=first_name+" "+last_name #adding name to instructor object
            user.save()
            messages.success(request," Instructor added successfully ")
            return redirect('addInstructor')
        except:
            messages.error(request," Error occured. Please Try again!")
            return redirect('addInstructor')
    return render(request,'HOD/add_instructor.html')


def registerStudent(request):
    '''
    for adding a new student
    '''
    
    if request.method=="POST":
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        batch=request.POST.getlist("batch_id") #getting an array of batches selected in html template
        ba=[]
        for b in batch:   #looping through the array
            batchh_obj=Batch.objects.get(id=b)
            ba.append(batchh_obj.batch_name)    #adding batch name to array for converting to string
        batch_arr=dumps(ba) #converting the array to json.dump string
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
            user.students.name=first_name+" "+last_name
            user.save()  #created user object and saving as student object
            stu_obj=Students.objects.get(user=user)
            stu_obj.batch_array=batch_arr   #saving the dump as string
            stu_obj.save()
            for bid in batch:
                batch_obj=Batch.objects.get(id=bid)
                stu_obj.batch_id.add(batch_obj)     #addition of manyToManyField
            messages.success(request," Student added successfully ")
            return redirect('addStudent')
        except:
            messages.error(request," Error occured. Please Try again!")
            return redirect('addStudent')
    batch=Batch.objects.all()
    return render(request,'HOD/add_student.html',{"batches":batch})


def addCourse(request):
    '''
    for adding a new course
    '''
    if request.method=="POST":
        course_name=request.POST.get("course_name")
        try:
            course=Course(course_name=course_name) #creating course object
            course.save()
            messages.success(request,"Course "+course_name+" successfully added! ")
            return redirect('addCourses')
        except:
            messages.error(request,"Error occured ! Please Try again.")
            return redirect('addCourses')
    return render(request,'HOD/add_course.html')


def addBatch(request):
    '''
    for addition of a new batch
    '''
    if request.method=="POST":
        batch_name=request.POST.get("batch_name")
        course=request.POST.get("course_id")
        instructor=request.POST.get("instructor_id")
        starttime=request.POST.get("start_time")
        endtime=request.POST.get("end_time")
        days=request.POST.getlist("day")
        try:
            course_obj=Course.objects.get(id=course)
            name=course_obj.course_name
            name=batch_name+" "+name
            instructor_obj=Instructor.objects.get(id=instructor)
            batch=Batch(batch_name=name,course_id=course_obj,instructor_id=instructor_obj,start_time=starttime,end_time=endtime,days=days)
            batch.save()
            bat_id=batch.id
            directory=f'ImageData/{str(bat_id)}'  #for saving students images of this batch
            path=os.path.join(BASE_DIR,directory)
            os.makedirs(path, exist_ok = True)   #creating a folder by batch ID
            messages.success(request,"Batch "+batch_name+" successfully added! ")
            return redirect('addBatch')
        except OSError as error:    #handling exceptions
            messages.error(request,error)
            return redirect('addBatch')
        except:
            messages.error(request,"Error occured ! Please Try again.")
            return redirect('addBatch')
    courses=Course.objects.all()
    instructors=Instructor.objects.all()
    context={'courses':courses,'instructors':instructors}
    return render(request,'HOD/add_batch.html',context)


def manageInstructor(request):
    '''
    lists the instructors so that admin can manage instructor

    also lets admin filter out the query
    '''
    ins=Instructor.objects.all()
    myfilter=InstructorFilter(request.GET,queryset=ins)
    ins=myfilter.qs
    return render(request,"HOD/manage_instructor.html",{"instructors":ins,"myfilter":myfilter})

def manageStudent(request):  
    '''
    lists the students so that admin can manage them and edit details

    also lets admin filter out the query
    '''
    stu=Students.objects.all()
    myfilter=StudentFilter(request.GET,queryset=stu)
    stu=myfilter.qs
    return render(request,"HOD/manage_students.html",{"students":stu,"myfilter":myfilter})

def manageCourse(request):    
    '''
    lists the courses so that admin can manage and edit

    also lets admin filter out the query
    '''
    cou=Course.objects.all()
    myfilter=CourseFilter(request.GET,queryset=cou)
    cou=myfilter.qs
    return render(request,"HOD/manage_course.html",{"courses":cou,"myfilter":myfilter})

def manageBatch(request): 
    '''
    lists the batches so that admin can manage

    also lets admin filter out the query
    '''
    bat=Batch.objects.all()
    myfilter=BatchFilter(request.GET,queryset=bat)
    bat=myfilter.qs
    return render(request,"HOD/manage_batch.html",{"batches":bat,"myfilter":myfilter})

def editInstructor(request,ins_id):
    '''
    handles the editing of instructor objects
    '''
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

def deleteFaceTemp(student_id):
    '''
    for deleting the student images after edit in students objects
    '''
    stu_obj=Students.objects.get(id=student_id)
    if stu_obj.faceTaken==True:

        batcharray=stu_obj.batch_id.all()       #getting list of students batches
        ba=[]
        for b in batcharray:
            ba.append(b.id)
        for c in ba:
            os.remove((os.path.join(BASE_DIR,"ImageData/"))+str(c)+"/"+str(student_id)+'.jpg')
        stu_obj.faceTaken=False
        stu_obj.save()

def editStudent(request,us_id):
    '''
    handles all the edits made in student object
    '''
    if request.method=="POST":
        student_id=request.POST.get("student_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        batch_id=request.POST.getlist("batch_id")
        ba=[]
        for b in batch_id:    #looping through all the batches student is enrolled in
            batchh_obj=Batch.objects.get(id=b)
            ba.append(batchh_obj.batch_name)
        batch_arr=dumps(ba)    #saving all the batches list as an string using json library

        try:
            user=CustomUser.objects.get(id=us_id)
            
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()
                

            stu_model=Students.objects.get(user=user)
            stu_model.name=first_name+" "+last_name
            deleteFaceTemp(student_id)       #deleting the face data of student in each edit as batch details could have been changed IMP
            stu_model.batch_array=batch_arr    #saving the string of batches list
            stu_model.batch_id.clear()
            stu_model.save()
            for bid in batch_id:
                batch_obj=Batch.objects.get(id=bid)
                stu_model.batch_id.add(batch_obj)
            stu_model.save()
            messages.success(request,"Successfully Edited Student")
            return HttpResponseRedirect(reverse("edits",kwargs={"us_id":us_id}))
        except:
            messages.error(request,"Failed to Edit Student")
            return HttpResponseRedirect(reverse("edits",kwargs={"stu_id":student_id}))
    user=CustomUser.objects.get(id=us_id)
    stu=Students.objects.get(user=user)
    batch=Batch.objects.all()
    listofbatch=loads(stu.batch_array)
    return render(request,"HOD/edit_student.html",{"student":stu,"batches":batch,"listofbatch":listofbatch})


def editCourse(request,cou_id):
    '''
    handles edit in details of course object by course ID
    '''
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
            days=dumps(days)   #json.dumps to convert to string
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


def deleteBatch(request,bat_id):
    '''
    deletes the batch object by BATCH ID provided and also deletes the entire folder of image data for that batch
    '''
    if request.method=="POST":
        batchid=request.POST.get("batchid")
        try:
            batch_obj=Batch.objects.get(id=batchid)
            name=batch_obj.batch_name
            
            stuarr=batch_obj.studentss.all()       #getting students in batch
            stuarray=[]
            for stu in stuarr:
                stuarray.append(stu.id)
            batch_obj.delete()
            for stu_id in stuarray:
                stu_obj=Students.objects.get(id=stu_id)
                batcharray=stu_obj.batch_id.all()       #getting list of students batches
                ba=[]
                for b in batcharray:
                    ba.append(b.batch_name)
                batch_arr=dumps(ba)

                stu_obj.batch_array=batch_arr
                stu_obj.save()
            dire=os.path.join(BASE_DIR,"ImageData")
            path=os.path.join(dire,str(bat_id))
            shutil.rmtree(path)   # deleting the image data for this batch

            messages.success(request,"Batch "+name+" deleted successfully")
            return redirect('manageb')
        except:
            messages.error(request,"Something went wrong! Could not delete batch")
            return redirect('manageb')
    batch=Batch.objects.get(id=bat_id)
    return render(request,"HOD/delete_batch.html",{"batch":batch})

def studentBatchReset(student):
    '''
    for reseting the batch of student object
    '''
    batches=student.batch_id.all()
    ba=[]
    for b in batches:
        ba.append(b.batch_name)
    batch_arr=dumps(ba)
    student.batch_array=batch_arr
    student.save()


def deleteAllBatchData(batchids):
    dire=os.path.join(BASE_DIR,"ImageData")
    for bat_id in batchids:
        path=os.path.join(dire,str(bat_id))
        shutil.rmtree(path)   # deleting the image data for this batch


def deleteCourse(request,cou_id):
    '''
    It deletes the course object
    '''
    if request.method=="POST":
        try:
            courseid=request.POST.get("courseid")
            course=Course.objects.get(id=courseid)
            batches=Batch.objects.filter(course_id=course)
            biid=[]  # for storing batch ids of batches to be deleted
            course.delete()
            students=Students.objects.all()
            for student in students:
                studentBatchReset(student)
            for batch in batches:
                biid.append(batch.id)
            deleteAllBatchData(biid)    # deleting all image data for batches that are automatically deleted
            messages.success(request,"Course Deleted")
            return redirect('managec')
        except:
            messages.error(request,"Something Went Wrong")
            return redirect('managec')
    course=Course.objects.get(id=cou_id)
    return render(request,"HOD/delete_course.html",{"course":course})

def deleteInstructor(request,ins_id):
    '''
    deletes the instructor object from DB
    '''
    if request.method=="POST":
        instructorid=request.POST.get("instructorid")
        try:
            instructor=Instructor.objects.get(id=instructorid)
            us=instructor.user.id
            user=CustomUser.objects.get(id=us)
            user.delete()
            messages.success(request,"Instructor Deleted Successfully")
            return redirect('managei')
        except CustomUser.DoesNotExist:
            messages.error(request,"Instructor Does not exist")
            return redirect('managei')
        except Exception as e:
            messages.error(request,str(e))
            return redirect('managei')
    instructor=Instructor.objects.get(id=ins_id)
    return render(request,"HOD/delete_instructor.html",{"instructor":instructor})

def deleteStudent(request,stu_id):
    '''
    deletes the instructor object
    '''
    if request.method=="POST":
        studentid=request.POST.get("studentid")
        try:
            student=Students.objects.get(id=studentid)
            batcharray=student.batch_id.all()       #getting list of students batches
            if student.faceTaken == True:
                ba=[]
                for b in batcharray:
                    ba.append(b.id)
                for c in ba:
                    os.remove((os.path.join(BASE_DIR,"ImageData/"))+str(c)+"/"+str(studentid)+'.jpg')
            us=student.user.id
            user=CustomUser.objects.get(id=us)
            user.delete()
            messages.success(request,"Student Deleted Successfully")
            return redirect('manages')
        except CustomUser.DoesNotExist:
            messages.error(request,"Instructor Does not exist")
            return redirect('manages')
        except Exception as e:
            messages.error(request,str(e))
            return redirect('manages')
    student=Students.objects.get(id=stu_id)
    return render(request,"HOD/delete_student.html",{"student":student})

def registerFace(request,us_id):
    '''
    for registering image data for student and storing in folder by batch id
    '''
    if request.method=="POST":
        try:
            userid=request.POST.get("userid")
            user=CustomUser.objects.get(id=userid)
            stu_obj=Students.objects.get(user=user)
            batcharray=stu_obj.batch_id.all()       #getting list of students batches
            ba=[]
            for b in batcharray:
                ba.append(b.id)
            cap=cv2.VideoCapture(0)
            while True:
                success,img = cap.read()
                imgSmall = cv2.resize(img, (0,0), None, 0.25, 0.25)
                imgSmall=cv2.cvtColor(imgSmall,cv2.COLOR_BGR2RGB)

                facesCurFrame = face_recognition.face_locations(imgSmall)    # getting faces in current frame
                if len(facesCurFrame)>1:
                    raise MultipleFaceException("Multiple faces or No face detected in the frame")
                elif len(facesCurFrame)==0:
                    raise MultipleFaceException("No face Detected")
                else:
                    for c in ba:
                        cv2.imwrite((os.path.join(BASE_DIR,"ImageData/"))+str(c)+"/"+str(stu_obj.id)+'.jpg',imgSmall)
                    stu_obj.faceTaken=True
                    stu_obj.save()
                    messages.success(request,"Face added successfully")
                    break
            cv2.imshow("Image",img)
            cv2.waitKey(0)
            cap.release()
            cv2.destroyAllWindows()


            return render(request,"HOD/createdataset.html",{"userid":userid})
        except MultipleFaceException as error:
            messages.error(request,error)
            cap.release()
            cv2.destroyAllWindows()
        except:
            messages.error(request,"Something went wrong! Try Again")
            cv2.destroyAllWindows()

            
    return render(request,"HOD/createdataset.html",{"userid":us_id})


def deleteFace(request,us_id):
    '''
    for deleting the image capture of the student
    '''
    if request.method=="POST":
        try:
            studentid=request.POST.get("studentid")
            stu_obj=Students.objects.get(id=studentid)
            batcharray=stu_obj.batch_id.all()       #getting list of students batches
            ba=[]
            for b in batcharray:
                ba.append(b.id)
            for c in ba:
                os.remove((os.path.join(BASE_DIR,"ImageData/"))+str(c)+"/"+str(studentid)+'.jpg')
            stu_obj.faceTaken=False
            stu_obj.save()
            messages.success(request,"Face Data Removed")
            return redirect('manages')
        except:
            messages.error(request,"Something Went Wrong")
            return redirect('manages')
    us=CustomUser.objects.get(id=us_id)
    student=Students.objects.get(user=us)
    if student.faceTaken==False:
        messages.error(request,"Face Data Not added in the first place")
        return redirect('manages')
    else:
        return render(request,"HOD/delete_face.html",{"student":student})
    