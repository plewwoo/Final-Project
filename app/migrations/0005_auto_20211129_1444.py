# Generated by Django 3.2.8 on 2021-11-29 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20211129_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacherpending',
            name='email',
        ),
        migrations.RemoveField(
            model_name='teacherpending',
            name='major',
        ),
        migrations.RemoveField(
            model_name='teacherpending',
            name='name',
        ),
        migrations.RemoveField(
            model_name='teacherpending',
            name='tel',
        ),
        migrations.RemoveField(
            model_name='teacherpending',
            name='year',
        ),
    ]
