# Generated by Django 3.0.8 on 2020-07-04 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200704_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('Teacher', '老师'), ('Student', '学生')], default='Student', max_length=10, verbose_name='用户类别'),
        ),
    ]
