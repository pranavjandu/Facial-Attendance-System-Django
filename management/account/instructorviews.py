
import face_recognition
from .models import Attendance, AttendanceReport, Batch, Instructor, Notification,Students,Mark,MarkReport
from django.shortcuts import redirect, render,HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse

import os
import cv2
import numpy as np

import datetime
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def instructorDashboard(request):
    '''
    Displaying the Homepage template for Instructor
    '''
    return render(request,"Instructor/dashboard.html")

def viewbatch(request):
    '''
    Displaying all the batches for the instructor that logins
    '''
    user_obj=request.user  #getting the user object
    ins_id=user_obj.instructor.id  #getting instructor from django user
    batches=Batch.objects.filter(instructor_id=ins_id)  #filtering batches for instructor
    return render(request,"Instructor/batches.html",{"batches":batches})  #rendering template

def viewstudents(request,bat_id):
    '''
    Getting all the students enrolled in the batch 

    keyword Arguments:

    bat_id : Batch id for batch whose students are to displayed

    '''
    bat_obj=Batch.objects.get(id=bat_id)   #getting batch object from batch id
    students=Students.objects.filter(batch_id=bat_id)    #getting all students in that batch
    return render(request,'Instructor/viewstu.html',{"students":students,"batch":bat_obj}) 

def findEncodings(images):
    '''
    creating a list of encodings for all images 
    '''
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encodeImg=face_recognition.face_encodings(img)[0]
        encodeList.append(encodeImg)
    return encodeList

    

def markAttendance(student_id,att_id):
    '''
    Marking attendance in the DB

    kwargs:

    student_id: ID of student to mark attendance for
    att_id: ID of the attendance object
    '''
    att=Attendance.objects.get(id=att_id)
    attrep=AttendanceReport.objects.get_or_create(attendance_id=att)
    if attrep.status==False:
        attrep.status=True
        attrep.save()
    stu_obj=Students.objects.get(id=student_id)
    attrep[0].student_id.add(stu_obj)


def attendance(request,bat_id):
    '''
    Running attendance marking script for a particular batch

    keyword Arguments:

    bat_id : Batch id for which attendance is to be taken
    '''
    if request.method=="POST":
        batchid=request.POST.get("batchid")
        batch_obj=Batch.objects.get(id=batchid)
        bat_name=batch_obj.batch_name
        att=Attendance.objects.get_or_create(subject_id=batch_obj,attendance_date=datetime.date.today())
        attid=att[0].id
        path='ImageData'    #path in base dir for saving images by BATCH_ID folders
        images=[]           # for name of images with extention
        imageNames=[]       # for name of images without extention
        studentMarked=[]     #list of students already marked present
        exactpath=os.path.join(BASE_DIR,path)
        exactpath=exactpath+"/"+str(batchid)
        myList=os.listdir(exactpath)    #listing all images in folder

        for cls in myList:
            curImg = cv2.imread(f'{exactpath}/{cls}')
            images.append(curImg)
            imageNames.append(os.path.splitext(cls)[0])

        encodeListKnown=findEncodings(images)    #encodings of all known faces of this batch

        cap = cv2.VideoCapture(0)     #capturing video

        while(True):
            success,img=cap.read()
            imgSmall=cv2.resize(img,(0,0),None,0.25,0.25)     #resizing for faster processing
            imgSmall=cv2.cvtColor(imgSmall,cv2.COLOR_BGR2RGB)    #converting image to RGB mode

            facesCurFrame = face_recognition.face_locations(imgSmall)      #getting face location in current image
            encodesCurFrame = face_recognition.face_encodings(imgSmall, facesCurFrame)    #getting face encoding for current image

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):    #checking the encodings and face locations
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                if len(faceDis) is not 0:
                    matchIndex = np.argmin(faceDis)
                    if matches[matchIndex]:   #if the face matches
                        name1 = imageNames[matchIndex]     #this is student id 
                        st_o= Students.objects.get(id=name1)
                        name=st_o.name     #this is student name
                        y1, x2, y2, x1 = faceLoc     #locations of face detected
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4     #resizing image back to normal size
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)   #creating a rectangle around the detected face
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)  
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2) # for showing student name on the rectangle above
                        if name1 not in studentMarked: #marking attendance if not already marked
                            studentMarked.append(name1)    #adding to marked list
                            markAttendance(student_id=name1,att_id=attid)    #marking attendance

            cv2.imshow("Webcam",img)
            key = cv2.waitKey(1) & 0xFF    #for waiting till key 's' is pressed
            if key == ord("s"):
                    break

    bat_obj=Batch.objects.get(id=bat_id)   #getting batch object from batch id
    return render(request,'Instructor/takeattendance.html',{"batch":bat_obj})


def viewAttendance(request,bat_id):
    '''
    for viewing the attendance by date
    '''
    batch=Batch.objects.get(id=bat_id)
    att=Attendance.objects.filter(subject_id=batch)
    return render(request,'Instructor/viewatt.html',{"atts":att,"batch":batch})

def deleteatt(request,att_id):
    '''
    for deleting that attendance object

    if attendance object is deleted the corresponding attendanceReports objects are also deleted automatically
    '''
    if request.method=="POST":
        attid=request.POST.get("attid")
        try:
            att=Attendance.objects.get(id=attid)
            att.delete()     #deleting object
            messages.success(request,"Attendance deleted")
            return redirect('insbatch')
        except:
            messages.error(request,"Something went wrong")
            return redirect('insbatch')

    att=Attendance.objects.get(id=att_id)
    return render(request,'Instructor/deleteattendance.html',{"att":att})
    
def attStudents(request,att_id,bat_id):
    '''
    For viewing students present and absent on a particular date 
    '''
    batch=Batch.objects.get(id=bat_id)
    studentssss=batch.studentss.all()
    ba=[]     #total students in batch
    for stu in studentssss:
        ba.append(stu.id)
    sa=[]   #  students absent
    att=Attendance.objects.get(id=att_id)
    attrep=AttendanceReport.objects.get(attendance_id=att)
    students=attrep.student_id.all()
    sp=[]   # students present
    for s in students:
        sp.append(s.id)
    for x in ba:
        if x not in sp:
            sa.append(Students.objects.get(id=x))
    
    return render(request,"Instructor/attstudents.html",{"students":students,"att":att,"studentabsent":sa})


def sendNotification(request,stu_id):
    '''
    for sending notification to student with student ID as stu_id
    '''
    if request.method=="POST":
        try:
            text=request.POST.get("messtext")
            stuid=request.POST.get("stuid")
            user=request.user   #getting logged in  user
            instructor=Instructor.objects.get(user=user)     #getting instructor object from user
            student=Students.objects.get(id=stuid)
            ruser=student.user  # This is user object of the reciever student
            Notification.objects.create(sendN=instructor,recieveN=ruser,msg_content=text)   #sending notification
            messages.success(request,"Notification Sent successfully")
            return redirect('insdashboard')
        except:
            messages.error(request,"Something went wrong")
            return redirect('insdashboard')
    student=Students.objects.get(id=stu_id)
    return render(request,'Instructor/sendnotif.html',{"student":student})
    

def sendNotification2(request,att_id,stu_id):
    '''
    for sending notification to student with student ID as stu_id and attendance ID as att_id

    This function is redundant but there to prevent a bug.
    '''
    if request.method=="POST":
        try:
            text=request.POST.get("messtext")
            stuid=request.POST.get("stuid")
            user=request.user     #getting logged in  user
            instructor=Instructor.objects.get(user=user)    #getting instructor object from user
            student=Students.objects.get(id=stuid)
            ruser=student.user   # This is user object of the reciever student
            Notification.objects.create(sendN=instructor,recieveN=ruser,msg_content=text)
            messages.success(request,"Notification Sent successfully")
            return redirect('insdashboard')
        except:
            messages.error(request,"Something went wrong")
            return redirect('insdashboard')
    student=Students.objects.get(id=stu_id)
    return render(request,'Instructor/sendnotif.html',{"student":student})

def marks(request):
    '''
    for viewing the list of batches for instructor thats logged in
    '''
    user_obj=request.user  #getting the user object
    ins_id=user_obj.instructor.id  #getting instructor from django user
    batches=Batch.objects.filter(instructor_id=ins_id)  #filtering batches for instructor
    return render(request,"Instructor/marks.html",{"batches":batches})  #rendering template


def listMark(request,bat_id):
    '''
    for getting a list of marks objects corresponding to BATCH ID as bat_id
    '''
    batch=Batch.objects.get(id=bat_id)
    mark_objs=Mark.objects.filter(batch_id=batch)
    return render(request,"Instructor/listmarks.html",{"marks":mark_objs,"bat":bat_id})

def createMarks(request,bat_id):
    '''
    for creating a new marks object

    this function does not have a template of it's own and only has a functionality.
    '''
    batch=Batch.objects.get(id=bat_id)
    mark,success=Mark.objects.get_or_create(batch_id=batch,test_date=datetime.date.today())
    return HttpResponseRedirect(reverse("listmarks",kwargs={"bat_id":bat_id}))

def addMarks(request,mark_id): 
    '''
    for viewing list of students and viewing there marks

    provides functionality of adding or editing marks
    '''
    mark=Mark.objects.get(id=mark_id)
    batch=mark.batch_id
    students=Students.objects.filter(batch_id=batch)    #getting all students in that batch
    markss=[]
    for st in students:
        rep,success=MarkReport.objects.get_or_create(student_id=st,mark_id=mark)
        markss.append(rep)
    zippedlist=zip(students,markss)   # This is done as we cannot loop through two loop simultaneously in django template
    return render(request,"Instructor/addmarks.html",{"students":zippedlist,"mark":mark})
    

def putMarks(request,stu_id,mark_id):
    '''
    For adding or editing the marks by inputing them into input box
    '''
    if request.method=="POST":
        m=request.POST.get("mark")     #getting how many marks student got
        mark=Mark.objects.get(id=mark_id)
        student=Students.objects.get(id=stu_id)
        try:
            rep,success=MarkReport.objects.get_or_create(student_id=student,mark_id=mark)
            if success==True:
                rep.mark=m
                rep.save()
                messages.success(request,"Marks added")
            else:
                rep.mark=m
                rep.save()
                messages.success(request,"Marks edited")
            return HttpResponseRedirect(reverse("addmarks",kwargs={"mark_id":mark.id}))
        except:
            messages.error(request,"Something went wrong")
            return HttpResponseRedirect(reverse("addmarks",kwargs={"mark_id":mark.id}))
    student=Students.objects.get(id=stu_id)
    return render(request,'Instructor/putmarks.html',{"student":student})


def reportPage(request):
    '''
    renders template that shows all the batches of instructor for report generation
    '''
    user_obj=request.user  #getting the user object
    ins_id=user_obj.instructor.id  #getting instructor from django user
    batches=Batch.objects.filter(instructor_id=ins_id)  #filtering batches for instructor
    return render(request,"Instructor/report.html",{"batches":batches})  #rendering template

def reportGenerate(request,bat_id):
    '''
    Generates a csv report and sends a response as an attachment

    kwargs:

    bat_id : batch ID for which report is to be generated
    '''
    batch=Batch.objects.get(id=bat_id)
    studentssss=batch.studentss.all()   #all students in that batch
    response=HttpResponse(content_type='text/csv')

    csv_writer=csv.writer(response)
    csv_writer.writerow(['Student Name','Dates Present','Marks'])

    for student in studentssss:
        datesPRESENT=[]   #getting dates on which student is present
        attreps=student.attendancereports.all()  #getting attendance reports of the student
        for attrep in attreps:
            atten=attrep.attendance_id
            if atten.subject_id==batch:      
                datestring=atten.attendance_date
                datestring=datestring.strftime('%Y-%m-%d')
                datesPRESENT.append(datestring)
        datesPRESENT.sort()
        markREPO=[]    #filtering markreports of this batch with test dates
        markreports=student.markrep.all()
        for markrep in markreports:
            m=markrep.mark_id
            if m.batch_id==batch:
                datestring=m.test_date
                datestring=datestring.strftime('%Y-%m-%d')
                markREPO.append(tuple([datestring,markrep.mark]))

        #writing to rows of csv file

        csv_writer.writerow([student.name,datesPRESENT,markREPO])
    
    response['Content-Disposition']='attachment; filename="report.csv"'
    return response


           

    
