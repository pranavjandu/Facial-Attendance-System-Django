
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
# Create your views here.

def loginpage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.user_type=='1':
                return redirect('dashboard')
            elif user.user_type=='2':
                return redirect('insdashboard')
            elif user.user_type=='3':
                return redirect('studashboard')
        else:
            messages.info(request," Wrong Credentials! Please Try again or contact your administrator")

    return render(request,'login.html')




def logoutUser(request):
    logout(request)
    return redirect('loginpage')




