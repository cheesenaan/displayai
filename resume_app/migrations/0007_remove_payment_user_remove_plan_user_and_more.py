# Generated by Django 4.2.7 on 2024-03-25 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("resume_app", "0006_payment_user_plan_user_project_user_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="payment", name="user",),
        migrations.RemoveField(model_name="plan", name="user",),
        migrations.RemoveField(model_name="project", name="user",),
        migrations.RemoveField(model_name="workexperience", name="user",),
    ]
