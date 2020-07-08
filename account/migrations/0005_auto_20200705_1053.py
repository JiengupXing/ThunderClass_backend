# Generated by Django 3.0.8 on 2020-07-05 02:53

from django.db import migrations, models
import system.storage


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200704_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='portrait',
            field=models.ImageField(default='portraits/no_portrait.png', storage=system.storage.ImageStorage(), upload_to='portraits', verbose_name='头像'),
        ),
    ]