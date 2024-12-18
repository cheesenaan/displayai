# Generated by Django 4.2.7 on 2024-10-08 01:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "resume_app",
            "0025_remove_project_user_profile_remove_userprofile_user_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="account",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="projects",
                to="resume_app.account",
            ),
        ),
    ]
