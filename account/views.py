from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Class
from api.models import Course
import json
import traceback
# Create your views here.


def index(request):
    return HttpResponse("You're at the account index")


def login(request):
    try:
        data = json.loads(request.body)
        print("receive: " + str(data))
        username = data["username"]
        password = data["password"]
        user = User.objects.filter(username=username).first()
        if user.user_type == user.TEACHER:
            courses = Course.objects.filter(creator=user)
        else:
            courses = user.courses.all()
        if not user:
            ret = {"code": 1, "msg": "user not exist"}
        else:
            if password == user.password:
                if user.user_type == user.STUDENT:
                    ret = {"code": 0,
                           "data": {"username": user.username,
                                    "user_type": user.user_type,
                                    "portrait_url": user.portrait.url,
                                    "nickname": user.nickname,
                                    "school": user.school,
                                    "email": user.email,
                                    "class": user.belong_to_class.class_name if user.belong_to_class else "null",
                                    "course_num": len(courses)}}
                else:
                    ret = {"code": 0,
                           "data": {"username": user.username,
                                    "user_type": user.user_type,
                                    "portrait_url": user.portrait.url,
                                    "nickname": user.nickname,
                                    "school": user.school,
                                    "email": user.email,
                                    "course_num": len(courses)}}

            else:
                ret = {"code": 2,
                       "msg": "password incorrect"}
            return HttpResponse(json.dumps(ret, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 3,
            'msg': "login failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")


def register(request):
    try:
        data = json.loads(request.body)
        print("receive: " + str(data))
        username = data["username"]
        password = data["password"]
        nickname = data["nickname"]
        user_type = data["user_type"]
        school = data["school"]
        email = data["email"]
        belong_to_class_id = data["belong_to_class"]
        belong_to_class = Class.objects.filter(id=belong_to_class_id).first()
        #TODU 处理头像
        User.objects.create(username=username,
                            password=password,
                            nickname=nickname,
                            user_type=User.TEACHER if user_type == "Teacher" else User.STUDENT,
                            school=school,
                            email=email,
                            belong_to_class=belong_to_class)
        return HttpResponse(json.dumps({
            'code': 0,
            'msg': "register success"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(json.dumps({
            'code': 1,
            'msg': "register failed"
        }, ensure_ascii=False), content_type="application/json, charset=utf-8")