


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
    path('managei',views.manageInstructor,name="managei"),
    path('manages',views.manageStudent,name="manages"),
    path('managec',views.manageCourse,name="managec"),
    path('manageb',views.manageBatch,name="manageb"),
    path('edit_instructor/<str:ins_id>',views.editInstructor,name="editi"),
    path('edit_student/<str:stu_id>',views.editStudent,name='edits'),
    path('edit_course/<str:cou_id>',views.editCourse,name='editc')
]