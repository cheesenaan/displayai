# Generated by Django 4.2.7 on 2024-07-23 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume_app', '0015_education_user_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='education',
            name='user_profile',
        ),
    ]
