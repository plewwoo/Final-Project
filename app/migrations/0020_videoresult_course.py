# Generated by Django 3.2.8 on 2022-03-27 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_videoresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoresult',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.allcourse'),
        ),
    ]