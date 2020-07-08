import pythoncom
from django.db import models
from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from system.storage import ImageStorage, PPTStorage
from system.ppt_to_jpg import ppt_to_jpg
import os
import django.conf
from django.utils import timezone


# Create your models here.


class PPT(models.Model):
    ppt_name = models.CharField(max_length=20,
                                verbose_name="课件名称")
    file = models.FileField(upload_to="ppts",
                            verbose_name="课件文件",
                            default="/ppts/no_ppt.ppt",
                            null=True,
                            blank=True,
                            storage=PPTStorage())
    pub_time = models.DateTimeField(auto_now=True, verbose_name="上传时间")
    uploader = models.ForeignKey(User,
                                 on_delete=models.PROTECT,
                                 verbose_name="上传者",
                                 related_name="user_upload_ppt",
                                 null=True,
                                 blank=True)

    def save(self):
        super(PPT, self).save()
        ppt_name = os.path.abspath(os.path.join(django.conf.settings.PROJECT_ROOT, "..")) + self.file.url.replace('/',
                                                                                                                  '\\')
        ppt_dir_path = ppt_name.split('.')[0]
        if not os.path.exists(ppt_dir_path):
            pythoncom.CoInitialize()
            os.mkdir(ppt_dir_path)
            ppt_to_jpg(ppt_name, ppt_dir_path)
            file_list = os.listdir(ppt_dir_path)
            for i, file in enumerate(file_list):
                os.rename(os.path.join(ppt_dir_path, file),
                          os.path.join(ppt_dir_path, "page" + str(i) + '.' + file.split('.')[1]))

    def __str__(self):
        return self.ppt_name

    class Meta:
        ordering = ['-pub_time']


class Exercise(models.Model):
    CHOICE_EXERCISE = 1
    COMMON_EXERCISE = 0
    EXERCISE_TYPE_CHOICE = [
        (CHOICE_EXERCISE, "选择题"),
        (COMMON_EXERCISE, "简答题"),
    ]
    content = models.TextField(default="", verbose_name="试题内容")
    exercise_type = models.SmallIntegerField(choices=EXERCISE_TYPE_CHOICE,
                                             default=COMMON_EXERCISE,
                                             verbose_name="试题类型")
    pub_time = models.DateTimeField(auto_now=True,
                                    verbose_name="上传时间")
    upload_file = models.FileField(upload_to="exercise",
                                   verbose_name="试题文件",
                                   null=True,
                                   blank=True)
    choice_num = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)],
                                             default=0,
                                             verbose_name="选项个数")
    choice_A = models.CharField(max_length=50,
                                verbose_name="选项A",
                                default="",
                                blank=True)
    choice_B = models.CharField(max_length=50,
                                verbose_name="选项B",
                                default="",
                                blank=True)
    choice_C = models.CharField(max_length=50,
                                verbose_name="选项C",
                                default="",
                                blank=True)
    choice_D = models.CharField(max_length=50,
                                verbose_name="选项D",
                                default="",
                                blank=True)
    NO_ANS = 0
    A_CORRECT = 1
    B_CORRECT = 2
    C_CORRECT = 3
    D_CORRECT = 4
    CORRECT_ANS_CHOICE = [
        (NO_ANS, "null"),
        (A_CORRECT, "A"),
        (B_CORRECT, "B"),
        (C_CORRECT, "C"),
        (D_CORRECT, "D"),
    ]
    correct_ans = models.SmallIntegerField(choices=CORRECT_ANS_CHOICE,
                                           verbose_name="正确选项",
                                           default=NO_ANS)
    uploader = models.ForeignKey(User,
                                 on_delete=models.PROTECT,
                                 verbose_name="上传者",
                                 related_name="user_upload_exercise",
                                 null=True,
                                 blank=True)

    class Meta:
        ordering = ["-pub_time"]


class Course(models.Model):
    INCLASS = 1
    OUTCLASS = 0
    COURSE_STATUS_CHOICE = [
        (INCLASS, "正在上课"),
        (OUTCLASS, "未上课")
    ]
    course_name = models.CharField(max_length=20,
                                   default="null",
                                   verbose_name="课程名称")
    credit = models.DecimalField(decimal_places=1,
                                 max_digits=2,
                                 default=0.0,
                                 verbose_name="学分")
    length = models.SmallIntegerField(default=0,
                                      verbose_name="学时")
    include_class = models.CharField(max_length=50,
                                     default="",
                                     verbose_name="所含班级")
    status = models.SmallIntegerField(choices=COURSE_STATUS_CHOICE,
                                      default=OUTCLASS,
                                      verbose_name="课堂状态")
    code = models.CharField(max_length=6,
                            verbose_name="课程暗号",
                            primary_key=True)

    pub_time = models.DateTimeField(auto_now=True, verbose_name="发布时间")

    now_class = models.IntegerField(null=True,
                                    blank=True,
                                    default=0)

    creator = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                verbose_name="创建老师",
                                related_name="user_create_course",
                                default="admin")

    students = models.ManyToManyField(User,
                                      related_name="courses",
                                      verbose_name="课堂学生",
                                      blank=True)
    ppts = models.ManyToManyField(PPT,
                                  related_name="courses",
                                  verbose_name="课堂课件",
                                  blank=True)
    exercises = models.ManyToManyField(Exercise,
                                       related_name="courses",
                                       verbose_name="课堂练习",
                                       blank=True)

    def __str__(self):
        return self.course_name

    class Meta:
        ordering = ['-status']


class Discuss(models.Model):
    content = models.TextField(default="",
                               verbose_name="讨论内容")
    pub_time = models.DateTimeField(auto_now=True,
                                    verbose_name="发表时间")
    title = models.CharField(max_length=30,
                             verbose_name="讨论主题",
                             null=True,
                             blank=True)
    belong_to_course = models.ForeignKey(Course,
                                         on_delete=models.CASCADE,
                                         verbose_name="所属课程",
                                         related_name="course_related_discuss",
                                         null=True,
                                         blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-pub_time"]


class Comment(models.Model):
    content = models.TextField(default="",
                               verbose_name="跟帖内容")
    pub_time = models.DateTimeField(auto_now=True,
                                    verbose_name="发表时间")
    star_num = models.IntegerField(default=0,
                                   verbose_name="点赞数")
    publisher = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  verbose_name="发表用户",
                                  related_name="user_pubish_comment",
                                  null=True,
                                  blank=True)
    belong_to_discuss = models.ForeignKey(Discuss,
                                          on_delete=models.CASCADE,
                                          verbose_name="跟帖",
                                          related_name="comment_after_discuss",
                                          null=True,
                                          blank=True)

    class Meta:
        ordering = ["-publisher"]


class Classroom(models.Model):
    belong_to_course = models.ForeignKey(Course,
                                         on_delete=models.CASCADE,
                                         verbose_name="所属课程",
                                         related_name="classrooms",
                                         null=True,
                                         blank=True)
    create_time = models.DateTimeField(auto_now_add=False,
                                       auto_now=False,
                                       blank=True,
                                       verbose_name="创建时间")
    end_time = models.DateTimeField(auto_now_add=False,
                                    auto_now=False,
                                    blank=True,
                                    verbose_name="结束时间")
    pushed_ppt = models.ForeignKey(PPT,
                                   on_delete=models.PROTECT,
                                   verbose_name="推送的课件",
                                   related_name="classrooms_push_to",
                                   null=True,
                                   blank=True)
    exercises = models.ManyToManyField(Exercise,
                                       related_name="exercises_push_to",
                                       verbose_name="推送的习题",
                                       blank=True,
                                       null=True)
    students = models.ManyToManyField(User,
                                      verbose_name="上课学生",
                                      through="ClassroomStudent",
                                      related_name="students_have_classrooms",
                                      blank=True)

    class Meta:
        ordering = ['-create_time']


class ClassroomStudent(models.Model):
    student = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                verbose_name="学生")
    classroom = models.ForeignKey(Classroom,
                                  on_delete=models.CASCADE,
                                  verbose_name="课堂")
    in_time = models.DateTimeField(verbose_name="加入时间",
                                   blank=True,
                                   auto_now_add=False,
                                   auto_now=False, )
    out_time = models.DateTimeField(verbose_name="退出时间",
                                    blank=True,
                                    auto_now_add=False,
                                    auto_now=False)

    class Meta:
        ordering = ['-classroom']
