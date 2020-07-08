import django
from django.shortcuts import render
from django.http import HttpResponse
from api.models import Course, Exercise, PPT, Discuss, Comment, Classroom, ClassroomStudent
from account.models import User
import json
import traceback
import os
from django.conf import settings


# Create your views here.
def index(request):
    return HttpResponse("You're at the account index")


def get_course_list(request):
    try:
        data = json.loads(request.body)
        print("received: " + str(data))
        username = data["username"]
        user = User.objects.get(username=username)
        data = []
        if user.user_type == user.TEACHER:
            courses = Course.objects.filter(creator=user)
        else:
            courses = user.courses.all()
        for i, course in enumerate(courses):
            course_data = {"course_code": course.code,
                           "course_name": course.course_name,
                           "credit": str(course.credit),
                           "length": course.length,
                           "status": course.status,
                           "class": course.include_class,
                           "pub_time": str(course.pub_time),
                           "creator": course.creator.nickname}
            data.append(course_data)
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


def get_course_members(request):
    try:
        data = json.loads(request.body)
        course_code = data["course_code"]
        course = Course.objects.get(code=course_code)
        students = course.students.all()
        data = []
        for i, student in enumerate(students):
            student_data = {"username": student.username,
                            "portrait_url": student.portrait.url,
                            "nickname": student.nickname,
                            "class": student.belong_to_class.class_name if student.belong_to_class else ""}
            data.append(student_data)
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


def get_ppt_detail(request):
    try:
        data = json.loads(request.body)
        ppt_id = data["ppt_id"]
        ppt = PPT.objects.get(id=ppt_id)
        img_root = ppt.file.url.split('.')[0] + '/'
        img_url = os.path.abspath(os.path.join(settings.PROJECT_ROOT, "..")) + ppt.file.url.split('.')[0].replace('/',
                                                                                                                  '\\') + '\\'
        ret = []
        for i, file in enumerate(os.listdir(img_url)):
            file_info = {"page_num: ": str(i),
                         "page_url": os.path.join(img_root, file)}
            ret.append(file_info)
        return HttpResponse(json.dumps({
            'code': 0,
            'data': ret,
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "get failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def get_discuss_list(request):
    try:
        data = json.loads(request.body)
        course_code = data["course_code"]
        course = Course.objects.get(code=course_code)
        discusses = Discuss.objects.filter(belong_to_course=course)
        ret = []
        for i, discuss in enumerate(discusses):
            discuss_info = {"discuss_id": discuss.id,
                            "discuss_title": discuss.title,
                            "discuss_content": discuss.content,
                            "discuss_release_time": str(discuss.pub_time), }
            ret.append(discuss_info)
        return HttpResponse(json.dumps({
            'code': 0,
            'data': ret,
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "get failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def get_comment_list(request):
    try:
        data = json.loads(request.body)
        discuss_id = data["discuss_id"]
        discuss = Discuss.objects.get(id=discuss_id)
        comments = Comment.objects.filter(belong_to_discuss=discuss)
        ret = []
        for i, comment in enumerate(comments):
            comment_info = {"comment_id": comment.id,
                            "comment_content": comment.content,
                            "comment_username": comment.publisher.username,
                            "comment_nickname": comment.publisher.nickname,
                            "portrait_url": comment.publisher.portrait.url,
                            "comment_time": str(comment.pub_time),
                            "comment_star_number": comment.star_num}
            ret.append(comment_info)
        return HttpResponse(json.dumps({
            'code': 0,
            'data': ret,
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "get failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def add_comment(request):
    try:
        data = json.loads(request.body)
        username = data["username"]
        user = User.objects.get(username=username)
        discuss_id = data["discuss_id"]
        discuss = Discuss.objects.get(id=discuss_id)
        content = data["comment_content"]
        Comment.objects.create(content=content,
                               publisher=user,
                               belong_to_discuss=discuss)
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


def add_discuss(request):
    try:
        data = json.loads(request.body)
        discuss_title = data["discuss_title"]
        discuss_content = data["discuss_content"]
        course_code = data["course_code"]
        course = Course.objects.get(code=course_code)
        Discuss.objects.create(title=discuss_title,
                               content=discuss_content,
                               belong_to_course=course)
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


def modify_star_num(request):
    try:
        data = json.loads(request.body)
        comment_id = data["comment_id"]
        comment_star_num = data["comment_star_num"]
        comment = Comment.objects.get(id=comment_id)
        comment.star_num = comment_star_num
        comment.save()
        return HttpResponse(json.dumps({
            'code': 0,
            'msg': "modify success"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "modify failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def get_class_ppt(request):
    try:
        data = json.loads(request.body)
        class_id = data["class_id"]
        classroom = Classroom.objects.get(id=class_id)
        ppt = classroom.pushed_ppt

        if not ppt:
            return HttpResponse(json.dumps({
            'code': 1,
            'msg': "ppt not pushed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
        else:
            img_root = ppt.file.url.split('.')[0] + '/'
            img_url = os.path.abspath(os.path.join(settings.PROJECT_ROOT, "..")) + ppt.file.url.split('.')[0].replace(
                '/',
                '\\') + '\\'
            ret = []
            for i, file in enumerate(os.listdir(img_url)):
                file_info = {"page_num: ": str(i),
                             "page_url": os.path.join(img_root, file)}
                ret.append(file_info)
            return HttpResponse(json.dumps({
                'code': 0,
                'ppt_name': ppt.ppt_name,
                'data': ret
            }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 2,
            'msg': "modify failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def get_class_exercises(request):
    try:
        data = json.loads(request.body)
        class_id = data["class_id"]
        classroom = Classroom.objects.get(id=class_id)
        exercises = classroom.exercises.all()
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
            'exercise_num': len(data),
            'data': data,
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 2,
            'msg': "modify failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
