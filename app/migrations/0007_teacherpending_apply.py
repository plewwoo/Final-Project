# Generated by Django 3.2.8 on 2021-11-29 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_history_teacherpending_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherpending',
            name='apply',
            field=models.BooleanField(default=False),
        ),
    ]
