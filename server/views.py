from django.shortcuts import render
from django.http import HttpResponse
from account.models import User
from api.models import Course, PPT, Exercise, Classroom, ClassroomStudent
import json
import traceback
import random
from django.utils import timezone

# Create your views here.

def index(request):
    return HttpResponse("you're in the server index.")


def get_ppt_list(request):
    try:
        data = json.loads(request.body)
        teacher_username = data["username"]
        teacher = User.objects.get(username=teacher_username)
        ppts = PPT.objects.filter(uploader=teacher).all()
        data = []
        for i, ppt in enumerate(ppts):
            ppt_info = {"ppt_id": ppt.id,
                        "ppt_name": ppt.ppt_name,
                        "page1_url": ppt.file.url.split('.')[0] + "/" + "page0.jpg",
                        "pub_time": str(ppt.pub_time)}
            data.append(ppt_info)
        return HttpResponse(json.dumps({
            'code': 0,
            'data': data,
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "get failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def get_exercise_list(request):
    try:
        data = json.loads(request.body)
        teacher_username = data["username"]
        teacher = User.objects.get(username=teacher_username)
        exercises = Exercise.objects.filter(uploader=teacher).all()
        data = []
        for i, exercise in enumerate(exercises):
            if exercise.exercise_type == Exercise.COMMON_EXERCISE:
                exercise_info = {"exercise_id": exercise.id,
                                 "exercise_type": exercise.exercise_type,
                                 "content": exercise.content,
                                 "pub_time": str(exercise.pub_time)}
            else:
                exercise_info = {"exercise_id": exercise.id,
                                 "exercise_type": exercise.exercise_type,
                                 "content": exercise.content,
                                 "pub_time": str(exercise.pub_time),
                                 "choice_num": exercise.choice_num,
                                 "choice_A": exercise.choice_A,
                                 "choice_B": exercise.choice_B,
                                 "choice_C": exercise.choice_C,
                                 "choice_D": exercise.choice_D,
                                 "correct_ans": exercise.correct_ans}
            data.append(exercise_info)
        return HttpResponse(json.dumps({
            'code': 0,
            'data': data,
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "get failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def create_course(request):
    try:
        data = json.loads(request.body)
        creator_username = data["username"]
        creator = User.objects.get(username=creator_username)
        course_name = data["course_name"]
        credit = data["credit"]
        length = data["length"]
        include_class = data["class"]
        code = "".join(random.sample('qwertyuiopasdfghjklzxcvbnm1234567890', 6))
        while Course.objects.filter(code=code):
            code = "".join(random.sample('qwertyuiopasdfghjklzxcvbnm1234567890', 6))
        Course.objects.create(code=code,
                              course_name=course_name,
                              credit=credit,
                              length=length,
                              include_class=include_class,
                              creator=creator)
        return HttpResponse(json.dumps({
            'code': 0,
            'course_code': code,
            'msg': "create success"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "create failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def delete_course(request):
    try:
        data = json.loads(request.body)
        username = data["username"]
        course_code = data["course_code"]
        course = Course.objects.get(code=course_code)
        user = User.objects.get(username=username)
        if course.creator == user:
            course.delete()
        return HttpResponse(json.dumps({
            'code': 0,
            'msg': "delete success"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "delete failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def start_class(request):
    try:
        data = json.loads(request.body)
        course_code = data['course_code']
        course = Course.objects.get(code=course_code)
        course.status = Course.INCLASS
        course.save()
        classroom = Classroom.objects.create(belong_to_course=course,
                                             create_time=timezone.localtime(),
                                             end_time=timezone.localtime())
        course.now_class = classroom.id
        course.save()
        return HttpResponse(json.dumps({
            'code': 0,
            'classroom_id': classroom.id,
            'msg': "start success"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "start failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def end_class(request):
    try:
        data = json.loads(request.body)
        course_code = data['course_code']
        course = Course.objects.get(code=course_code)
        course.status = Course.OUTCLASS
        course.save()
        class_id = course.now_class
        classroom = Classroom.objects.get(id=class_id)
        classroom.end_time = timezone.localtime()
        classroom.save()
        students = classroom.students.all()
        for i, student in enumerate(students):
            classroom_student = ClassroomStudent.objects.filter(student=student,
                                                                classroom=classroom).first()
            classroom_student.end_time = timezone.localtime()
            classroom_student.save()
        return HttpResponse(json.dumps({
            'code': 0,
            'msg': "end success"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "end failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def add_ppt(request):
    try:
        data = json.loads(request.body)
        ppt_id = data["ppt_id"]
        class_id = data["class_id"]
        ppt = PPT.objects.get(id=ppt_id)
        classroom = Classroom.objects.get(id=class_id)
        course = classroom.belong_to_course
        course.ppts.add(ppt)
        classroom.pushed_ppt = ppt
        classroom.save()
        return HttpResponse(json.dumps({
            'code': 0,
            'msg': "add success"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "add failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def add_exercise(request):
    try:
        data = json.loads(request.body)
        exercise_id = data["exercise_id"]
        class_id = data["class_id"]
        exercise = Exercise.objects.get(id=exercise_id)
        classroom = Classroom.objects.get(id=class_id)
        course = classroom.belong_to_course
        course.exercises.add(exercise)
        classroom.exercises.add(exercise)
        return HttpResponse(json.dumps({
            'code': 0,
            'msg': "add success"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "add failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def delete_member(request):
    try:
        data = json.loads(request.body)
        username = data["username"]
        course_code = data["course_code"]
        student = User.objects.get(username=username)
        course = Course.objects.get(code=course_code)
        course.students.remove(student)
        return HttpResponse(json.dumps({
            'code': 0,
            'msg': "add success"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "add failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def get_course_class(request):
    try:
        data = json.loads(request.body)
        course_code = data["course_code"]
        course = Course.objects.get(code=course_code)
        classrooms = course.classrooms.all()
        data = []
        for i, classroom in enumerate(classrooms):
            classroom_info = {"class_id": classroom.id,
                              "create_time": timezone.localtime(classroom.create_time).strftime("%Y-%m-%d %H:%M:%S"),
                              "end_time": timezone.localtime(classroom.end_time).strftime("%Y-%m-%d %H:%M:%S")}
            data.append(classroom_info)
        return HttpResponse(json.dumps({
            'code': 0,
            'data': data,
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "get failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def get_signup_table(request):
    try:
        data = json.loads(request.body)
        class_id = data["class_id"]
        classroom = Classroom.objects.get(id=class_id)
        students = classroom.students.all()
        data = []
        for i, student in enumerate(students):
            student_classroom = ClassroomStudent.objects.filter(student=student,
                                                                classroom=classroom).first()
            signup_info = {"nickname": student.nickname,
                           "username": student.username,
                           "enter_time": timezone.localtime(student_classroom.in_time).strftime("%Y-%m_%d %H:%M:%S"),
                           "leave_time": timezone.localtime(student_classroom.out_time).strftime("%Y-%m_%d %H:%M:%S"),
                           "delta_time": str(student_classroom.out_time - student_classroom.in_time).split('.')[0]}
            data.append(signup_info)
        return HttpResponse(json.dumps({
            'code': 0,
            'data': data,
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "get failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")