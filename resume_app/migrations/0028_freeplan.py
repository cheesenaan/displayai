# Generated by Django 4.2.7 on 2024-02-10 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("resume_app", "0027_alter_account_tier"),
    ]

    operations = [
        migrations.CreateModel(
            name="FreePlan",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("forms_filled", models.IntegerField(default=0)),
                ("form_fill_date", models.DateTimeField()),
                ("number_of_resumes", models.IntegerField(default=0)),
                ("number_of_websites", models.IntegerField(default=0)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resume_app.account",
                    ),
                ),
                (
                    "user_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resume_app.userprofile",
                    ),
                ),
            ],
        ),
    ]
