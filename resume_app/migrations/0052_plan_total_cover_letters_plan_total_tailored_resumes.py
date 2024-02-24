# Generated by Django 4.2.7 on 2024-02-24 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resume_app", "0051_alter_account_resume_links"),
    ]

    operations = [
        migrations.AddField(
            model_name="plan",
            name="total_cover_letters",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="plan",
            name="total_tailored_resumes",
            field=models.IntegerField(default=0),
        ),
    ]
