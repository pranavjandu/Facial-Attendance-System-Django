from .models import Batch, Course, CustomUser, Instructor,Students
from django.shortcuts import redirect, render,HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.urls import reverse
from .filters import InstructorFilter,StudentFilter,CourseFilter,BatchFilter
from json import dumps,loads

import os
import dlib
import cv2
from imutils import face_utils,resize
from imutils.video import VideoStream
from imutils.face_utils import FaceAligner
import face_recognition
from face_recognition import face_encodings
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

from PIL import Image
from.exceptions import MultipleFaceException
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 

def dash(request):
    return render(request,'HOD/dashboard.html')


 
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
        batch=request.POST.getlist("batch_id")
        ba=[]
        for b in batch:
            batchh_obj=Batch.objects.get(id=b)
            ba.append(batchh_obj.batch_name)
        batch_arr=dumps(ba)
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
            user.students.name=first_name+" "+last_name
            user.save()
            stu_obj=Students.objects.get(user=user)
            stu_obj.batch_array=batch_arr
            stu_obj.save()
            for bid in batch:
                batch_obj=Batch.objects.get(id=bid)
                stu_obj.batch_id.add(batch_obj)
            messages.success(request," Student added successfully ")
            return redirect('addStudent')
        except:
            messages.error(request," Error occured. Please Try again!")
            return redirect('addStudent')
    batch=Batch.objects.all()
    return render(request,'HOD/add_student.html',{"batches":batch})


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
        try:
            course_obj=Course.objects.get(id=course)
            name=course_obj.course_name
            name=batch_name+" "+name
            instructor_obj=Instructor.objects.get(id=instructor)
            batch=Batch(batch_name=name,course_id=course_obj,instructor_id=instructor_obj,start_time=starttime,end_time=endtime,days=days)
            batch.save()
            bat_id=batch.id
            directory=f'ImageData/{str(bat_id)}'
            path=os.path.join(BASE_DIR,directory)
            os.makedirs(path, exist_ok = True) 
            messages.success(request,"Batch "+batch_name+" successfully added! ")
            return redirect('addBatch')
        except OSError as error:
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
        batch_id=request.POST.getlist("batch_id")
        ba=[]
        for b in batch_id:
            batchh_obj=Batch.objects.get(id=b)
            ba.append(batchh_obj.batch_name)
        batch_arr=dumps(ba)

        try:
            user=CustomUser.objects.get(id=student_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()
                

            stu_model=Students.objects.get(user=student_id)
            stu_model.name=first_name+" "+last_name
            stu_model.batch_array=batch_arr
            stu_model.save()
            for bid in batch_id:
                batch_obj=Batch.objects.get(id=bid)
                stu_model.batch_id.add(batch_obj)
            stu_model.save()
            messages.success(request,"Successfully Edited Student")
            return HttpResponseRedirect(reverse("edits",kwargs={"stu_id":student_id}))
        except:
            messages.error(request,"Failed to Edit Student")
            return HttpResponseRedirect(reverse("edits",kwargs={"stu_id":student_id}))
    stu=Students.objects.get(user=stu_id)
    batch=Batch.objects.all()
    listofbatch=loads(stu.batch_array)
    return render(request,"HOD/edit_student.html",{"student":stu,"batches":batch,"listofbatch":listofbatch})


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


def deleteBatch(request,bat_id):
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
            dir=os.path.join(BASE_DIR,"ImageData")
            path=os.path.join(dir,str(bat_id))
            shutil.rmtree(path)

            messages.success(request,"Batch "+name+" deleted successfully")
            return redirect('manageb')
        except:
            messages.error(request,"Something went wrong! Could not delete batch")
            return redirect('manageb')
    batch=Batch.objects.get(id=bat_id)
    return render(request,"HOD/delete_batch.html",{"batch":batch})

def studentBatchReset(student):
    batches=student.batch_id.all()
    ba=[]
    for b in batches:
        ba.append(b.batch_name)
    batch_arr=dumps(ba)
    student.batch_array=batch_arr
    student.save()

def deleteCourse(request,cou_id):
    if request.method=="POST":
        try:
            courseid=request.POST.get("courseid")
            course=Course.objects.get(id=courseid)
            course.delete()
            students=Students.objects.all()
            for student in students:
                studentBatchReset(student)
            messages.success(request,"Course Deleted")
            return redirect('managec')
        except:
            messages.error(request,"Something Went Wrong")
            return redirect('managec')
    course=Course.objects.get(id=cou_id)
    return render(request,"HOD/delete_course.html",{"course":course})

def deleteInstructor(request,ins_id):
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
                if len(facesCurFrame)>1 or len(facesCurFrame)==0:
                    raise MultipleFaceException("Multiple faces or No face detected in the frame")
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
        except:
            messages.error(request,"Something went wrong! Try Again")

            
    return render(request,"HOD/createdataset.html",{"userid":us_id})


def deleteFace(request,us_id):
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
    # if request.method=="POST":
    #     id = request.POST.get("userid")
    #     #try:
    #     user=CustomUser.objects.get(id=id)
    #     cap=cv2.VideoCapture(0)
    #     success,img=cap.read()

    #     img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #     img=recognizeFace(img)
    #     img, status = detection(img)
    #     if status:
    #             #change path here 
    #         cv2.imwrite(os.path.join(BASE_DIR,'ImagesAttendance/') + user.username + '.jpg', img)
    #         with open('users.csv', mode='a', newline='') as employee_file:
    #             employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #             employee_writer.writerow([user.id, user.username,user.students.batch_id,user.email])
    #         doEncoding()
    #     widthi = int(img.shape[1] * 60/100)
    #     heighti = int(img.shape[0] * 70/100)
    #     dim = (widthi, heighti)
    #     img=cv2.resize(img,dim,interpolation=cv2.INTER_AREA)
    #     height,width,channel=img.shape
    #     step=channel*width
    #     cv2.imshow("Image",img)
    #     cv2.waitKey(100)
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     #To make faceTaken to True in database
    #     user=CustomUser.objects.get(id=us_id)
    #     stuid=user.students.id
    #     stu_obj=Students.objects.get(id=stuid)
    #     stu_obj.faceTaken=True
    #     stu_obj.save()
    #     messages.success(request,"Face data added successfully")
    #     return HttpResponseRedirect(reverse("createdataset",kwargs={"us_id":id}))
    #     '''except:
    #         messages.error(request,"Error occured while adding data")
    #         return HttpResponseRedirect(reverse("createdataset",kwargs={"us_id":id}))'''
    # return render(request,"HOD/createdataset.html",{"userid":us_id})



'''def registerFace(request,us_id):
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



def trainSet(request):
    if request.method=="POST":
        training_dir='face_data/dataset'
        count=0
        for student_id in os.listdir(training_dir):
            curr_directory=os.path.join(training_dir,student_id)
            if not os.path.isdir(curr_directory):
                continue
            for imagefile in image_files_in_folder(curr_directory):
                count+=1

        X=[]
        y=[]
        i=0

        for student_id in os.listdir(training_dir):
            print(str(student_id))
            curr_directory=os.path.join(training_dir,student_id)
            if not os.path.isdir(curr_directory):
                continue
            for imagefile in image_files_in_folder(curr_directory):
                print(str(imagefile))
                image=cv2.imread(imagefile)
                try:
                    X.append((face_encodings(image)[0]).tolist())
                    y.append(student_id)
                    i+=1
                except:
                    print("removed")
                    os.remove(imagefile)

        encoder = LabelEncoder()
        encoder.fit(y)
        y=encoder.transform(y)
        X1=np.array(X)
        print("shape: "+ str(X1.shape))
        np.save('face_data/classes.npy', encoder.classes_)
        svc = SVC(kernel='linear',probability=True)
        svc.fit(X1,y)
        svc_save_path="face_data/svc.sav"
        with open(svc_save_path, 'wb') as f:
            pickle.dump(svc,f)
        
        messages.success(request,'Training Complete.')
        return redirect('train')
    return render(request,"HOD/train.html")

'''