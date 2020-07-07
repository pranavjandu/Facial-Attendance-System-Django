from .models import Admin, Batch, Course, Instructor, Students, User
from django.contrib import admin

# Register your models here.

admin.site.register(Instructor)
admin.site.register(Admin)
admin.site.register(Students)
admin.site.register(Course)
admin.site.register(Batch)