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

from face_recognition import face_encodings
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC




def instructorDashboard(request):
    return render(request,"Instructor/dashboard.html")

def viewbatch(request):
    user_obj=request.user
    ins_id=user_obj.instructor.id
    #Instructor.objects.get(id=user_obj.id)
    #ins_id=ins_obj.id
    batches=Batch.objects.filter(instructor_id=ins_id)
    return render(request,"Instructor/batches.html",{"batches":batches})

def viewstudents(request,bat_id):
    pass