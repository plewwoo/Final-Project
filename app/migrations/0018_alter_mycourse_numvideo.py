# Generated by Django 3.2.8 on 2022-03-22 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20220322_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycourse',
            name='numVideo',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
