from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email=models.EmailField(max_length=255)

class Instructor(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email=models.EmailField(max_length=255)
    
class Student(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email=models.EmailField(max_length=255)

class Course(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    course_instructor=models.ForeignKey(Instructor,on_delete=models.CASCADE)
    students=models.ManyToManyField(Student)
    session_start_date=models.DateField()
    session_end_date=models.DateField()

class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    course_id=models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    attendance_date=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)

class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)

class Marks(models.Model):
    id=models.AutoField(primary_key=True)
    course_id=models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    marks_date=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)

class MarksReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    marks_id=models.ForeignKey(Marks,on_delete=models.CASCADE)
    mark=models.IntegerField(max_length=200)


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()


class NotificationInstructor(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    message = models.TextField()


    
    