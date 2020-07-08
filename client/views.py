from django.shortcuts import render
from django.http import HttpResponse
from api.models import Course, Exercise, Classroom, ClassroomStudent
from account.models import User
from django.utils import timezone
import json
import traceback


# Create your views here.

def index(request):
    return HttpResponse("You're at the client index")


def join_course_code(request):
    try:
        data = json.loads(request.body)
        course_code = data["code"]
        student_username = data["username"]
        course = Course.objects.filter(code=course_code).first()
        if not course:
            return HttpResponse(json.dumps({
                'code': 1,
                'msg': "no such course"
            }, ensure_ascii=False), content_type="application/json, charset=utf-8")
        else:
            student = User.objects.filter(username=student_username).first()
            course.students.add(student)
            return HttpResponse(json.dumps({
                'code': 0,
                'msg': "join success"
            }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 2,
            'msg': "join failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def get_course_ppts(request):
    try:
        data = json.loads(request.body)
        course_code = data["course_code"]
        course = Course.objects.get(code=course_code)
        ppts = course.ppts.all()
        data = []
        for i, ppt in enumerate(ppts):
            ppt_info = {"ppt_id": ppt.id,
                        "page1_url": ppt.file.url.split('.')[0] + "/" + "page0.jpg",
                        "ppt_name": ppt.ppt_name,
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


def get_course_exercises(request):
    try:
        data = json.loads(request.body)
        print("receive: " + str(data))
        course_code = data["course_code"]
        course = Course.objects.get(code=course_code)
        exercises = course.exercises.all()
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


def quit_course(request):
    try:
        data = json.loads(request.body)
        course_code = data["course_code"]
        username = data["username"]
        student = User.objects.get(username=username)
        course = Course.objects.get(code=course_code)
        course.students.remove(student)
        return HttpResponse(json.dumps({
            'code': 0,
            'msg': "quit success",
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "quit failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def enter_class(request):
    try:
        data = json.loads(request.body)
        course_code = data["course_code"]
        username = data["username"]
        print(username)
        student = User.objects.get(username=username)
        course = Course.objects.get(code=course_code)
        classroom = Classroom.objects.get(id=course.now_class)
        ClassroomStudent.objects.create(student=student,
                                        classroom=classroom,
                                        in_time=timezone.localtime(),
                                        out_time=timezone.localtime())
        return HttpResponse(json.dumps({
            'code': 0,
            "classroom_id": classroom.id,
            'msg': "quit success",
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "quit failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def leave_class(request):
    try:
        data = json.loads(request.body)
        class_id = data["class_id"]
        username = data["username"]
        classroom = Classroom.objects.get(id=class_id)
        user = User.objects.get(username=username)
        classroom_student = ClassroomStudent.objects.filter(student=user,
                                                            classroom=classroom).first()
        classroom_student.end_time = timezone.localtime()
        classroom_student.save()
        return HttpResponse(json.dumps({
            'code': 0,
            'msg': "leave success",
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "leave failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
