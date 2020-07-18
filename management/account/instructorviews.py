
import face_recognition
from .models import Attendance, AttendanceReport, Batch, Course, CustomUser, Instructor,Students
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

from face_recognition import face_encodings
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

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
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encodeImg=face_recognition.face_encodings(img)[0]
        encodeList.append(encodeImg)
    return encodeList

    

def markAttendance(student_id,att_id):
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
        path='ImageData'
        images=[]
        imageNames=[]
        studentMarked=[]
        exactpath=os.path.join(BASE_DIR,path)
        exactpath=exactpath+"/"+str(batchid)
        myList=os.listdir(exactpath)

        for cls in myList:
            curImg = cv2.imread(f'{exactpath}/{cls}')
            images.append(curImg)
            imageNames.append(os.path.splitext(cls)[0])

        encodeListKnown=findEncodings(images)    #encodings of all known faces of this 

        cap = cv2.VideoCapture(0)

        while(True):
            success,img=cap.read()
            imgSmall=cv2.resize(img,(0,0),None,0.25,0.25)
            imgSmall=cv2.cvtColor(imgSmall,cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgSmall)
            encodesCurFrame = face_recognition.face_encodings(imgSmall, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                if len(faceDis) is not 0:
                    matchIndex = np.argmin(faceDis)
                    if matches[matchIndex]:
                        name1 = imageNames[matchIndex]     #this is student id 
                        st_o= Students.objects.get(id=name1)
                        name=st_o.name     #this is student name
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                        if name1 not in studentMarked:
                            studentMarked.append(name1)
                            markAttendance(student_id=name1,att_id=attid)

            cv2.imshow("Webcam",img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("s"):
                    break

    bat_obj=Batch.objects.get(id=bat_id)   #getting batch object from batch id
    return render(request,'Instructor/takeattendance.html',{"batch":bat_obj})


def viewAttendance(request,bat_id):
    batch=Batch.objects.get(id=bat_id)
    att=Attendance.objects.filter(subject_id=batch)
    return render(request,'Instructor/viewatt.html',{"atts":att})

def deleteatt(request,att_id):
    if request.method=="POST":
        attid=request.POST.get("attid")
        try:
            att=Attendance.objects.get(id=attid)
            att.delete()
            messages.success(request,"Attendance deleted")
            return redirect('insbatch')
        except:
            messages.error(request,"Something went wrong")
            return redirect('insbatch')

    att=Attendance.objects.get(id=att_id)
    return render(request,'Instructor/deleteattendance.html',{"att":att})
    
