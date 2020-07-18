from .models import Admin, Attendance, AttendanceReport, Batch, Course, Instructor, Mark, MarkReport, Notification, Students, CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)
admin.site.register(Instructor)
admin.site.register(Admin)
admin.site.register(Students)
admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(Mark)
admin.site.register(MarkReport)
admin.site.register(Notification)