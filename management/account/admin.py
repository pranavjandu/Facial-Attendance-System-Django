from .models import Admin, Batch, Course, Instructor, Students, CustomUser
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