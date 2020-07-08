from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('get_course_list/', get_course_list, name="user_get_courses"),
    path('get_course_members/', get_course_members, name="user_get_course_members"),
    path('get_ppt_detail/', get_ppt_detail, name="user_get_ppt_detail"),
    path('get_discuss_list/', get_discuss_list, name="user_get_discuss_list"),
    path('get_comment_list/', get_comment_list, name="user_get_comment_list"),
    path('add_comment/', add_comment, name="user_add_comment"),
    path('add_discuss/', add_discuss, name="user_add_discuss"),
    path('modify_star_num/', modify_star_num, name="comment_modify_star_num"),
    path('get_class_ppt/', get_class_ppt, name="user_get_class_ppt"),
    path('get_class_exercises/', get_class_exercises, name="user_get_class_exercises"),
]