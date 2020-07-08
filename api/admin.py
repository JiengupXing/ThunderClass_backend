from django.contrib import admin
from .models import Course, PPT, Exercise, Discuss, Comment, Classroom, ClassroomStudent
# Register your models here.

admin.site.register(Course)
admin.site.register(PPT)
admin.site.register(Exercise)
admin.site.register(Discuss)
admin.site.register(Comment)
admin.site.register(Classroom)
admin.site.register(ClassroomStudent)