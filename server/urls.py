from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('get_ppt_list/', get_ppt_list, name="teacher_get_ppts"),
    path('get_exercise_list/', get_exercise_list, name="teacher_get_exercises"),
    path('create_course/', create_course, name="teacher_create_course"),
    path('delete_course/', delete_course, name='teacher_delete_course'),
    path('start_class/', start_class, name="teacher_start_class"),
    path('end_class/', end_class, name='teacher_end_class'),
    path('add_ppt/', add_ppt, name="teacher_add_ppt"),
    path('add_exercise/', add_exercise, name="teacher_add_exercise"),
    path('delete_member/', delete_member, name="teacher_delete_course_member"),
    path('get_course_class/', get_course_class, name="teacher_get_course_class"),
    path('get_signup_table/', get_signup_table, name="teacher_get_signup_table"),
]