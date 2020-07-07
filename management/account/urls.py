
from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginpage),
    path('adm',views.dash,name="dashboard"),
    path('managecourse',views.manageCourse,name="mcourses")
]