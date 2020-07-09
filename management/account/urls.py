


from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginpage,name="loginpage"),
    path('adm',views.dash,name="dashboard"),
    path('logout',views.logoutUser,name="logout"),
    path('addInstructor',views.registerInstructor,name="addInstructor"),
    path('addCourse',views.addCourse,name="addCourses"),
    path('addBatch',views.addBatch,name="addBatch"),
    path('addStudent',views.registerStudent,name="addStudent"),
    path('register',views.registerStudent,name="register")
]