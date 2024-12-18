# Generated by Django 4.2.7 on 2024-08-09 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("resume_app", "0023_education_coursework"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="educations",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="education_account",
                to="resume_app.education",
            ),
        ),
    ]
