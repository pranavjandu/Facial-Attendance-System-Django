
from django.urls import path
from . import views,adminviews,instructorviews,studentviews

urlpatterns = [
    path('',views.loginpage,name="loginpage"),
    path('adm',adminviews.dash,name="dashboard"),
    path('logout',views.logoutUser,name="logout"),
    path('addInstructor',adminviews.registerInstructor,name="addInstructor"),
    path('addCourse',adminviews.addCourse,name="addCourses"),
    path('addBatch',adminviews.addBatch,name="addBatch"),
    path('addStudent',adminviews.registerStudent,name="addStudent"),
    path('managei',adminviews.manageInstructor,name="managei"),
    path('manages',adminviews.manageStudent,name="manages"),
    path('managec',adminviews.manageCourse,name="managec"),
    path('manageb',adminviews.manageBatch,name="manageb"),
    path('edit_instructor/<str:ins_id>',adminviews.editInstructor,name="editi"),
    path('edit_student/<str:us_id>',adminviews.editStudent,name='edits'),
    path('edit_course/<str:cou_id>',adminviews.editCourse,name='editc'),
    path('edit_batch/<str:bat_id>',adminviews.editBatch,name='editb'),
    path('createdataset/<str:us_id>',adminviews.registerFace,name='createdataset'),
    path('delete_batch/<str:bat_id>',adminviews.deleteBatch,name='deleteb'),
    path('delete_course/<str:cou_id>',adminviews.deleteCourse,name='deletec'),
    path('delete_instructor/<str:ins_id>',adminviews.deleteInstructor,name='deletei'),
    path('delete_student/<str:stu_id>',adminviews.deleteStudent,name="deletes"),
    path('delete_face/<str:us_id>',adminviews.deleteFace,name="deletef"),


    #student paths
    path('studashboard',studentviews.studentDashboard,name="studashboard"),
    path('stucourses',studentviews.stuCourses,name="stucourses"),
    path('see_atten/<str:bat_id>',studentviews.seeAttendance),
    path('see_marks/<str:bat_id>',studentviews.seeMarks),


    #instructor paths
    path('insdashboard',instructorviews.instructorDashboard,name="insdashboard"),
    path('insbatch',instructorviews.viewbatch,name="insbatch"),
    path('check_students/<str:bat_id>',instructorviews.viewstudents,name="checkstudents"),
    path('attendance/<str:bat_id>',instructorviews.attendance,name="takeattendance"),
    path('viewAttendance/<str:bat_id>',instructorviews.viewAttendance,name="viewatt"),
    path('viewAttendance/delete_att/<str:att_id>',instructorviews.deleteatt),
    path('viewAttendance/att_students/<str:att_id>/<str:bat_id>',instructorviews.attStudents),
    path('check_students/send_notification/<str:stu_id>',instructorviews.sendNotification),
    path('viewAttendance/att_students/<str:att_id>/send_notification/<str:stu_id>',instructorviews.sendNotification2),
    path('marks',instructorviews.marks,name="insmarks"),
    path('list_marks/create_marks/<str:bat_id>',instructorviews.createMarks),
    path('add_marks/<str:mark_id>',instructorviews.addMarks,name="addmarks"),
    path('add_marks/put_marks/<str:stu_id>/<str:mark_id>',instructorviews.putMarks),
    path('list_marks/<str:bat_id>',instructorviews.listMark,name="listmarks"),
    path('report',instructorviews.reportPage,name="insreport"),
    path('generate_report/<str:bat_id>',instructorviews.reportGenerate)
]