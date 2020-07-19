from .models import Attendance, Batch, Course, CustomUser, Instructor, Mark, MarkReport, Notification,Students
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

def studentDashboard(request):
    if request.method=="POST":
        try:
            x=request.POST.get("delete")
            notifics=Notification.objects.filter(recieveN=request.user)
            for n in notifics:
                n.delete()
            messages.success(request,"Successfully Cleared")
            return redirect('studashboard')
        except:
            messages.error(request,"Something went wrong")
            return redirect('studashboard')
    notifics=Notification.objects.filter(recieveN=request.user)
    return render(request,"Student/dashboard.html",{"notification":notifics})


def stuCourses(request):
    student=Students.objects.get(user=request.user)
    batches=student.batch_id.all()
    return render(request,"Student/batches.html",{"batches":batches})

def seeAttendance(request,bat_id):
    batch=Batch.objects.get(id=bat_id)
    atten=Attendance.objects.filter(subject_id=batch)
    user=request.user
    student=Students.objects.get(user=user)
    attreps=student.attendancereports.all()
    attendanceObjects=[]     #getting attendance objects for days present 
    for attrep in attreps:
        atten=attrep.attendance_id
        if atten.subject_id==batch:
            attendanceObjects.append(atten)
    return render(request,"Student/seeatten.html",{"attendances":attendanceObjects,"batch":batch})


def seeMarks(request,bat_id):
    batch=Batch.objects.get(id=bat_id)
    user=request.user
    student=Students.objects.get(user=user)
    markobjs=Mark.objects.filter(batch_id=batch)
    mreports=[]
    for markobj in markobjs:
        stat=MarkReport.objects.filter(mark_id=markobj,student_id=student).exists()
        if stat==True: 
            markrep=MarkReport.objects.get(mark_id=markobj,student_id=student)
            mreports.append(markrep)
    return render(request,"Student/seemark.html",{"marks":mreports,"batch":batch})