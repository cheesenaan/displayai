# Generated by Django 4.2.7 on 2024-07-24 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resume_app", "0022_remove_education_coursework"),
    ]

    operations = [
        migrations.AddField(
            model_name="education",
            name="coursework",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]