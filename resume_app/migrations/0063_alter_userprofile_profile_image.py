# Generated by Django 4.2.7 on 2024-02-28 14:10

from django.db import migrations, models
import resume_app.models


class Migration(migrations.Migration):

    dependencies = [
        ("resume_app", "0062_alter_userprofile_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="profile_image",
            field=models.ImageField(
                upload_to=resume_app.models.UserProfile.profile_image_upload_to
            ),
        ),
    ]
