# Generated by Django 3.2.8 on 2021-11-27 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_homework_homeworktitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycourse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile'),
        ),
    ]
