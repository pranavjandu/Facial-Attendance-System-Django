from django.contrib import admin
from .models import Admin, Attendance, AttendanceReport, Course,Instructor, Marks, MarksReport, NotificationInstructor, NotificationStudent, Student

admin.site.register(Admin)
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(NotificationStudent)
admin.site.register(NotificationInstructor)
admin.site.register(Marks)
admin.site.register(MarksReport)

