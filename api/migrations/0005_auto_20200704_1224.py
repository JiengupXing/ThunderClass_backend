# Generated by Django 3.0.8 on 2020-07-04 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200704_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='exercises',
            field=models.ManyToManyField(blank=True, related_name='courses', to='api.Exercise'),
        ),
        migrations.AddField(
            model_name='course',
            name='ppts',
            field=models.ManyToManyField(blank=True, related_name='courses', to='api.PPT'),
        ),
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.CharField(max_length=6, primary_key=True, serialize=False, verbose_name='课程暗号'),
        ),
    ]