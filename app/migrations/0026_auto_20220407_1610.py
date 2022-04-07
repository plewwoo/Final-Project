# Generated by Django 3.2.8 on 2022-04-07 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_quiz_difficulty'),
    ]

    operations = [
        migrations.AddField(
            model_name='mycourse',
            name='passedQuiz',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='passed',
            field=models.BooleanField(default=False),
        ),
    ]