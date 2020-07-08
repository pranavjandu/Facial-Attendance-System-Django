

from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginpage,name="loginpage"),
    path('adm',views.dash,name="dashboard"),
    path('managecourse',views.manageCourse,name="mcourses"),
    path('logout',views.logoutUser,name="logout"),
    path('addInstructor/',views.registerInstructor,name="addInstructor"),
    path('register',views.registerStudent,name="register")
]