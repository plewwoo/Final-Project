# Generated by Django 3.2.8 on 2022-04-04 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_videoresult_currenttime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allcourse',
            name='courseRating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=19),
        ),
    ]
