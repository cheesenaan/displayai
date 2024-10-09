# Generated by Django 4.2.7 on 2024-07-23 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("resume_app", "0014_remove_userprofile_degree_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="education",
            name="user_profile",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="education",
                to="resume_app.userprofile",
            ),
        ),
    ]