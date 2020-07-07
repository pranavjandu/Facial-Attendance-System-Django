from django.db import models
# Create your models here.
from django.contrib.auth.models import User


class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    objects=models.Manager()

    def __str__(self):
        return self.name

class Instructor(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    objects=models.Manager()
    def __str__(self):
        return self.name

class Course(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    objects=models.Manager()

class Batch(models.Model):
    id=models.AutoField(primary_key=True)
    batch_name=models.CharField(max_length=255)
    course_id=models.ForeignKey(Course,on_delete=models.CASCADE,default=1)
    instructor_id=models.ForeignKey(Instructor,on_delete=models.CASCADE)
    objects=models.Manager()

class Students(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    course_id=models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    objects = models.Manager()
    def __str__(self):
        return self.name

class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Batch,on_delete=models.DO_NOTHING)
    attendance_date=models.DateField(auto_now_add=True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    objects=models.Manager()

class Mark(models.Model):
    id=models.AutoField(primary_key=True)
    batch_id=models.ForeignKey(Batch,on_delete=models.DO_NOTHING)
    test_date=models.DateField(auto_now_add=True)
    objects = models.Manager()

class MarkReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    mark_id=models.ForeignKey(Mark,on_delete=models.CASCADE)
    mark=models.IntegerField()
    objects=models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationInstructor(models.Model):
    id = models.AutoField(primary_key=True)
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


