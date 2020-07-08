from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('join_course_code/', join_course_code, name="join_course_throuth_code"),
    path('get_course_ppts/', get_course_ppts, name="get_course_related_ppts"),
    path('get_course_exercises/', get_course_exercises, name="get_course_related_exercises"),
    path('quit_course/', quit_course, name="student_quit_course"),
    path('enter_class/', enter_class, name="student_enter_class"),
    path('leave_class/', leave_class, name="student_leave_class"),
]