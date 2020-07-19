from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver



class CustomUser(AbstractUser):
    user_type_data=((1,"Admin"),(2,"Instructor"),(3,"Students"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)


class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    objects=models.Manager()

    def __str__(self):
        return self.name

class Instructor(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    objects=models.Manager()
    def __str__(self):
        return self.name

class Course(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    objects=models.Manager()

    def __str__(self):
        return self.course_name

class Batch(models.Model):
    id=models.AutoField(primary_key=True)
    batch_name=models.CharField(max_length=255)
    course_id=models.ForeignKey(Course,on_delete=models.CASCADE,default=1)
    instructor_id=models.ForeignKey(Instructor,on_delete=models.SET_NULL,null=True)
    start_time=models.TimeField(null=True,blank=True)
    end_time=models.TimeField(null=True,blank=True)
    days = models.CharField(max_length=100)
    objects=models.Manager()
    def __str__(self):
        return self.batch_name

class Students(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    batch_id=models.ManyToManyField(Batch,related_name="studentss")
    batch_array=models.CharField(max_length=255)
    faceTaken=models.BooleanField(default=False) 
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
    student_id=models.ManyToManyField(Students,related_name="attendancereports")
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    objects=models.Manager()

class Mark(models.Model):
    id=models.AutoField(primary_key=True)
    batch_id=models.ForeignKey(Batch,on_delete=models.DO_NOTHING,default=1)
    test_date=models.DateField(auto_now_add=True,blank=True)
    objects = models.Manager()

class MarkReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING,related_name="markrep")
    mark_id=models.ForeignKey(Mark,on_delete=models.CASCADE)
    mark=models.IntegerField(default=0)
    objects=models.Manager()


class Notification(models.Model):
    id=models.AutoField(primary_key=True)
    sendN = models.ForeignKey(Instructor,on_delete=models.CASCADE,related_name="senders")
    recieveN = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="recievers")
    msg_content = models.TextField()
    created_at = models.TimeField(auto_now_add=True)
    objects=models.Manager()



@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    '''
    For creating objects of user type from CustomUser object using django signals
    '''
    if created:
        if instance.user_type==1:
            Admin.objects.create(user=instance,name="admin")
        if instance.user_type==2:
            Instructor.objects.create(user=instance)
        if instance.user_type==3:
            Students.objects.create(user=instance)

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    '''
    For saving objects of user type from CustomUser object using django signals
    '''
    if instance.user_type==1:
        instance.admin.save()
    if instance.user_type==2:
        instance.instructor.save()
    if instance.user_type==3:
        instance.students.save()