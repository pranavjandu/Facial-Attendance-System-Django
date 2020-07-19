from .models import Attendance, Batch, Mark, MarkReport, Notification,Students   # Models Import
from django.shortcuts import redirect, render
from django.contrib import messages  # For success and error messages display

def studentDashboard(request):
    '''
    For displaying notifications recieved on dashboard
    '''
    if request.method=="POST":      # If user press clear notifications
        try:
            x=request.POST.get("delete")
            notifics=Notification.objects.filter(recieveN=request.user)    #getting notifications from DB
            for n in notifics:
                n.delete()         #deleting all objects
            messages.success(request,"Successfully Cleared")
            return redirect('studashboard')
        except:
            messages.error(request,"Something went wrong")
            return redirect('studashboard')
    notifics=Notification.objects.filter(recieveN=request.user)   #getting notifications from DB
    return render(request,"Student/dashboard.html",{"notification":notifics})


def stuCourses(request):
    '''
    For displaying all enrolled batches for logined student
    '''
    student=Students.objects.get(user=request.user)   
    batches=student.batch_id.all()   #getting batches for which student is enrolled
    return render(request,"Student/batches.html",{"batches":batches})

def seeAttendance(request,bat_id):
    '''
    For students to view the dates they were present for a particular batch
    '''
    batch=Batch.objects.get(id=bat_id)
    atten=Attendance.objects.filter(subject_id=batch)   #filtering all attendance objects by batch
    user=request.user
    student=Students.objects.get(user=user)   #getting student object of logged in user
    attreps=student.attendancereports.all() 
    attendanceObjects=[]     #getting attendance objects for days present 
    for attrep in attreps:
        atten=attrep.attendance_id
        if atten.subject_id==batch:      
            attendanceObjects.append(atten)
    return render(request,"Student/seeatten.html",{"attendances":attendanceObjects,"batch":batch})


def seeMarks(request,bat_id):
    '''
    For students to view the marks they were given for a particular batch
    '''
    batch=Batch.objects.get(id=bat_id)
    user=request.user
    student=Students.objects.get(user=user)   #getting student object of logged in user
    markobjs=Mark.objects.filter(batch_id=batch)
    mreports=[]     #for getting marksreport objects of the student
    for markobj in markobjs:
        stat=MarkReport.objects.filter(mark_id=markobj,student_id=student).exists()   #checking if markreport object exists 
        if stat==True: 
            markrep=MarkReport.objects.get(mark_id=markobj,student_id=student)
            mreports.append(markrep)
    return render(request,"Student/seemark.html",{"marks":mreports,"batch":batch})