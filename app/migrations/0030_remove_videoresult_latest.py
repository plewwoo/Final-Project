# Generated by Django 3.2.8 on 2022-04-11 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_videoresult_latest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoresult',
            name='latest',
        ),
    ]
