# Generated by Django 3.2.8 on 2022-04-04 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_allcourse_courserating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allcourse',
            name='courseRating',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=19, null=True),
        ),
    ]