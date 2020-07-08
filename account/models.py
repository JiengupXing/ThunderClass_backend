from django.db import models
from system.storage import ImageStorage

# Create your models here.
class Class(models.Model):
    class_name = models.CharField(max_length=15, verbose_name=u"班级名称")

    def __str__(self):
        return self.class_name


class User(models.Model):
    TEACHER = "Teacher"
    STUDENT = "Student"
    USER_TYPE_CHOICE = [
        (TEACHER, "老师"),
        (STUDENT, "学生"),
    ]
    username = models.CharField(max_length=20,
                                primary_key=True,
                                verbose_name="用户名")
    password = models.CharField(max_length=20, verbose_name="密码")
    nickname = models.CharField(max_length=20,
                                default="null",
                                verbose_name="昵称")
    portrait = models.ImageField(verbose_name='头像',
                                 upload_to='portraits',
                                 default='portraits/no_portrait.png',
                                 storage=ImageStorage())
    user_type = models.CharField(max_length=10,
                                 choices=USER_TYPE_CHOICE,
                                 default=STUDENT,
                                 verbose_name="用户类别")
    school = models.CharField(max_length=15,
                              verbose_name="所在院校",
                              null=True,
                              blank=True)
    email = models.EmailField(verbose_name="电子邮件",
                              null=True,
                              blank=True)
    belong_to_class = models.ForeignKey(Class,
                                        on_delete=models.PROTECT,
                                        verbose_name="所在班级",
                                        related_name="user_to_class",
                                        null=True,
                                        blank=True)
    def __str__(self):
        return self.nickname

    class Meta:
        ordering = ['-user_type']